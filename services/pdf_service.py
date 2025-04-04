import os
from fastapi import UploadFile, HTTPException
from pypdf import PdfReader
from logger_config import logger
from utils.embedding_utils import get_embeddings
from utils.chromadb_utils import collection
from config import UPLOAD_DIR

# Creating the upload directory
os.makedirs(UPLOAD_DIR, exist_ok=True)


# Function to handle PDF uploads
async def handle_upload(pdf: UploadFile):
    pdf_path = os.path.join(UPLOAD_DIR, pdf.filename)       # Save path for the uploaded PDF
    try:
        with open(pdf_path, "wb") as f:
            f.write(await pdf.read())
        logger.info(f" PDF '{pdf.filename}' uploaded successfully.")
        return {"message": "PDF uploaded successfully.", "pdf_name": pdf.filename, "pdf_path": pdf_path}
    except Exception as e:
        logger.error(f" File upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

# Function to process the uploaded PDF and store embeddings
async def handle_process(pdf_name: str):
    pdf_path = os.path.join(UPLOAD_DIR, pdf_name)

# Checking if the file actually exists
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF not found.")

# Check if this PDF is already stored in ChromaDB
    existing = collection.get(ids=[f"{pdf_name}_0"])
    if existing and existing["documents"]:
        return {"message": f" PDF '{pdf_name}' is already stored in ChromaDB."}

    try:
        logger.info(f" Processing PDF: {pdf_name}")
        reader = PdfReader(pdf_path)
        text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="No extractable text found.")

        text_chunks = [text[i:i+500] for i in range(0, len(text), 500)]
        logger.info(f"🔹 Segmented into {len(text_chunks)} chunks.")

        embeddings = get_embeddings(text_chunks)

        for i, emb in enumerate(embeddings):
            collection.add(
                ids=[f"{pdf_name}_{i}"],
                embeddings=[emb],
                documents=[text_chunks[i]]
            )

        logger.info(f"PDF '{pdf_name}' processed and stored in ChromaDB.")
        return {"message": f"PDF '{pdf_name}' processed successfully, embeddings stored."}

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
