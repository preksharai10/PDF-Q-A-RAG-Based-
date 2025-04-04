# **PDF Question-and-Answer App**
## **Overview**
A robust and scalable PDF Question-Answering System built with FastAPI, designed to process unstructured PDF documents into searchable knowledge bases. The application enables users to upload PDFs, extract and chunk textual content, generate semantic embeddings using HuggingFace Transformers, and persist them in Chroma Vector Database for efficient similarity search. Natural language queries are answered using Google’s Gemini Large Language Model, delivering structured, context-aware responses
# **Features**
1. Upload PDF files through a simple API

2. Extract and segment PDF text

3. Generate semantic embeddings using HuggingFace models

4. Store and retrieve embeddings with ChromaDB

5. Use Google Gemini API for precise, context-aware answers

6. Structured JSON output
## **Installation**

### 1. Clone the repository

```bash
git clone https://github.com/your-username/<repository-name>.git

cd <repository-name>
```
### 2. Install Dependencies

Run the following command to install all required Python packages:

```bash
pip install -r requirements.txt
```
### 3. Set up your environment

Create a `.env` file in the root directory and add your Google API key:

```env
GOOGLE_API_KEY=your_gemini_api_key
```
### 4. Run the App

Use the following command to start the FastAPI application:

```bash
uvicorn app.main:app --reload
```

## API Endpoints

### 1. Upload PDF

**Endpoint:**  `POST /upload/`

**Request:**  
- Content-Type: `multipart/form-data`
- Body Parameter: `pdf` (The PDF file to upload)
  <br>
**Response:**
```json
{
  "message": "PDF uploaded successfully.",
  "pdf_name": "sample.pdf",
  "pdf_path": "uploads/sample.pdf"
}
```
### 2. Process PDF

**Endpoint:**  `POST /process/`

**Request Body:**
```json
{
  "pdf_name": "sample.pdf"
}
```
**Response:**
```
json
{
  "message": "PDF 'sample.pdf' processed successfully, embeddings stored."
}
```
### 3. Query PDF

**Endpoint:**  
`GET /query/?question=What is the summary?&pdf_name=sample.pdf`

**Response:**
```json
{
  "question": "What is the summary?",
  "answer": "This document explains the overall goals and system architecture..."
}
```
## **Technologies Used**
1. FastAPI – For building APIs

2. PyPDF – For extracting text from PDFs

3. LangChain + HuggingFace – For text embeddings

4. ChromaDB – Vector store for fast retrieval

5. Gemini API (Google Generative AI) – For AI-generated answers

6. Uvicorn – ASGI server for FastAPI
