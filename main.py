from fastapi import FastAPI, UploadFile, File, HTTPException
from services.pdf_service import handle_upload, handle_process
from services.query_service import handle_query

app = FastAPI()                                         # Initializing FastAPI app instance

@app.post("/upload/")                                   # Defining POST endpoint to upload PDF
async def upload_pdf(pdf: UploadFile = File(...)):      # accepting PDF file as form-data
    return await handle_upload(pdf)                     # importing handler function for querying

@app.post("/process/")                                  # defining POST endpoint to process uploaded PDF
async def process_pdf(pdf_name: str):                   # accepting PDF name as form-data       
    return await handle_process(pdf_name)               # importing handler function for processing     
    
@app.get("/query/")                                     # defining GET endpoint to query the PDF    
async def query_pdf(question: str, pdf_name: str):      # accepting question and PDF name as query parameters
    return await handle_query(question, pdf_name)
