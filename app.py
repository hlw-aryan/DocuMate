import streamlit as st
import requests
import json
from htmlTemplates import css, bot_template, user_template

# Function to upload files to the server
def uploadFile(uploadedFiles):
    for uploadedFile in uploadedFiles:
        fileName = uploadedFile.name[:-4]  # Remove file extension
        files = {"file": uploadedFile.getvalue()}
        data = {"fileName": fileName}
        response = requests.post("https://documate-api.onrender.com/upload/", files=files, data=data)
        if response.status_code == 200:
            st.write(f"File {fileName} uploaded successfully!")
        else:
            st.write(f"Error uploading file {fileName}")

# Function to reset the server environment
def resetEnvironment():
    response = requests.post("https://documate-api.onrender.com/reset/")
    if response.status_code == 200:
        st.session_state.userQuestion = ""
        st.session_state.uploadedFiles = []
        st.write("All files and data have been reset!")
    else:
        st.write("Error resetting files")

# Function to process user queries
def queryProcess(userQuestion):
    params = {"userQuery": userQuestion}
    response = requests.get("https://documate-api.onrender.com/query/", params=params)
    st.session_state.userQuestion = ""

    if response.status_code == 200:
        jsonStr = response.content.decode('utf-8')  # Decode bytes to string
        data = json.loads(jsonStr)  # Parse JSON string to dictionary

        chat_history = data['queryResult']['chat_history']

        # Display chat history in alternate template (user and bot)
        for i, message in enumerate(chat_history):
            if i % 2 == 0:
                st.write(user_template.replace("{{MSG}}", message['content']), unsafe_allow_html=True)
            else:
                st.write(bot_template.replace("{{MSG}}", message['content']), unsafe_allow_html=True)
    else:
        st.write("Query Fetch Failed:", response.status_code)

# Main function
def main():
    st.set_page_config(page_title="DocuMate", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)
    st.header("Chat with multiple Docs :books:")        

    # Check if uploaded files and user questions are stored in session state, if not reset the environment
    if "uploadedFiles" not in st.session_state:
        resetEnvironment()
        st.session_state.uploadedFiles = []
        st.session_state.userQuestion = ""

    userQuestion = st.text_input("Please enter your query")
    
    # Process user query if provided and files are uploaded
    if userQuestion:
        if st.session_state.uploadedFiles == []:
            st.write("Please upload your files first then ask your questions.")
        else:
            st.session_state.userQuestion = userQuestion
            queryProcess(userQuestion)
            st.session_state.userQuestion = ""

    # Sidebar layout
    with st.sidebar:
        st.image("https://i.imgur.com/tL9zCGt.png", width=230)
        st.subheader("About")
        st.write("Unlock your documents with DocuMate's tech, streamlining research and speeding decisions.")
        uploadedFiles = st.file_uploader("Upload your PDFs here and click on 'Process' button", type=['pdf'], accept_multiple_files=True)

        if uploadedFiles:
            st.session_state.uploadedFiles = uploadedFiles

        st.markdown("**Note:** Only PDF files are accepted")
        col1, col2 = st.columns(2)

        # Process uploaded files
        if col1.button("Process"):
            with st.spinner("Processing..."):
                if st.session_state.uploadedFiles:
                    uploadFile(st.session_state.uploadedFiles)
                else:
                    st.write("No files to process")

        # Reset environment
        if col2.button("Reset"):
            if st.session_state.userQuestion != "" or st.session_state.uploadedFiles != []:
                resetEnvironment()
            else:
                st.write("No files to reset")

if __name__ == '__main__':
    main()
