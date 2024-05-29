# DocuMate

DocuMate is a tool that allows users to interactively query information from multiple documents using natural language. It leverages advanced language models and document processing techniques to provide efficient and accurate responses to user queries.

## Features

- **Document Upload**: Users can upload documents (PDFs) containing textual information.
- **Natural Language Query**: Users can ask questions in natural language.
- **Interactive Chat Interface**: Responses to user queries are displayed in an interactive chat interface.
- **Reset Functionality**: Users can reset the uploaded documents and conversation history.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/hlw-aryan/DocuMate.git
    ```

2. Create a virtual environment in the project directory:

    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On macOS and Linux:

        ```bash
        source venv/bin/activate
        ```

4. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Set up environment variables:

    - Create a `.env` file in the root directory.
    - Add the following variables:

        ```
        GOOGLE_API_KEY=your_google_api_key
        ```

## Usage

1. Run the FastAPI server:

    ```bash
    uvicorn main:app --reload
    ```

2. Access the application backend in your browser at `http://localhost:8000`.

3. Run the Streamlit app:

    ```bash
    streamlit run app.py
    ```

3. Access the application in your browser at the provided URL (usually `http://localhost:8501`).

4. Upload PDF documents using the provided interface and click on the button 'Process'.

5. Enter your query in the text input field and press enter.

6. View the responses in the chat interface.

7. Use the "Reset" button to clear uploaded documents and conversation history.

## API Endpoints

- **POST /upload/**: Uploads a PDF document.
- **GET /query/**: Retrieves responses to user queries.
- **POST /reset/**: Resets uploaded documents and conversation history.

## Technologies Used

- [Streamlit](https://streamlit.io/): For building the user interface.
- [FastAPI](https://fastapi.tiangolo.com/): For creating the backend API.
- [Google Generative AI](https://github.com/microsoft/GENAI): For natural language processing.
- [pdfplumber](https://github.com/jsvine/pdfplumber): For extracting text from PDF documents.
- [FAISS](https://github.com/facebookresearch/faiss): For efficient text similarity search.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the Apache License - see the [LICENSE](https://github.com/hlw-aryan/DocuMate?tab=Apache-2.0-1-ov-file#) file for details.
