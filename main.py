import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
from fastapi import FastAPI, UploadFile, File, Form, Query
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import MessagesPlaceholder
from langchain.chains.history_aware_retriever import create_history_aware_retriever
import pdfplumber
import io

app = FastAPI()

# Initialize variables
chunks = []  # Chunks to be processed efficiently
chat_history = [] # Chat history in current state 
conversation = None # Conversation

load_dotenv()

# Endpoint to handle file upload
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...), fileName: str = Form(...)):
    contents = await file.read()  # Read file content asynchronously
    parsePdf(fileName, contents)
    return {"status": "success", "fileName": fileName}

# Endpoint to handle user queries
@app.get("/query/")
async def getQueryResult(userQuery: str = Query(...)):
    if userQuery:
        global conversation 
        if conversation == None:
            initializeConversation()

        queryResult = handleUserquery(userQuery)
        if queryResult:
            chat_history.append(HumanMessage(content=queryResult["input"]))
            chat_history.append(AIMessage(content=queryResult["answer"])) 

            return {"status": "success","chat_history":chat_history, "queryResult": queryResult}
        else:
            return {"status": "missing","chat_history":chat_history, "queryResult": "Data not found"}
    else:
        return {"status": "error","chat_history":chat_history, "queryResult": "Query processing failed"}

# Endpoint to reset files and data
@app.post("/reset/")
async def resetFiles():
    global chunks, conversation, chat_history
    chunks = []
    conversation = None
    chat_history = []
    return {"status": "success", "message": "All files and data have been reset"}

# Initialize conversation chain
def initializeConversation():
    vectorstore = getVectorStore(chunks)
    global conversation
    conversation = getConversationChain(vectorstore)

# Parse PDF content and store chunks
def parsePdf(fileName: str, contents):
    text = ""
    with pdfplumber.open(io.BytesIO(contents)) as pdf:
        for page in pdf.pages:
            text += page.extract_text(x_tolerance=1, y_tolerance=1)

    cleanedText = cleanText(text)
    splitAndStoreText(fileName, cleanedText)

    return

# Split text into chunks and store
def splitAndStoreText(fileName, cleanedText):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200
    )
    texts = splitter.split_text(cleanedText)

    for textChunk in texts:
        chunks.append(textChunk)
    
# Clean raw text
def cleanText(rawText):
    cleanedText = re.sub(r'\s+', ' ', rawText).replace('\t', ' ').replace('\n', ' ').strip()
    return cleanedText

# Generate vector store from text chunks
def getVectorStore(textChunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001") # type: ignore
    vectorStore = FAISS.from_texts(
        textChunks,
        embedding=embeddings
    )
    return vectorStore

# Initialize conversation chain
def getConversationChain(vectorStore):
    model = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro-latest",
        temperature=0.1
    )  # type: ignore

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer the user's question based on the context and remember your name is DocuMate: {context}"),
        MessagesPlaceholder(variable_name = "chat_history"),
        ("human", "Question: {input}")
    ])

    chain = create_stuff_documents_chain ( 
        prompt=prompt,
        llm = model 
    )

    retriever = vectorStore.as_retriever(
        search_kwargs = { "k" : 3 } 
    )

    retrieverPrompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name = "chat_history"),
        ("human", "Question: {input}"),
        ("human", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
    ])

    historyAwareRetriever = create_history_aware_retriever(
        llm = model,
        retriever = retriever,
        prompt = retrieverPrompt 
    )
    retrievalChain = create_retrieval_chain(
        historyAwareRetriever,
        chain 
    )

    return retrievalChain

# Handle user query
def handleUserquery(userQuery):
    global conversation, chat_history
    if conversation:
        response = conversation.invoke({ 
            "input": userQuery,
            "chat_history": chat_history 
        })       
        return response
    else:
        print("Conversation not initialized. Please upload and parse a file first.")
        return None
