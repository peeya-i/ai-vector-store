import logging
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
import os
import uuid
import requests
from typing import Dict, List
import shutil
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configuration
VECTOR_STORE_URL = os.getenv("VECTOR_STORE_URL", "http://localhost:8001")
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
MAX_RETRIES = 5
RETRY_DELAY = 2  # seconds

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

def check_vector_store_connection():
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(f"{VECTOR_STORE_URL}/search?query=test")
            if response.status_code == 200:
                logger.info("Successfully connected to vector store service")
                return True
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1}/{MAX_RETRIES}: Could not connect to vector store service: {str(e)}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
    return False

@app.on_event("startup")
async def startup_event():
    logger.info("Starting API backend service")
    if not check_vector_store_connection():
        logger.warning("Could not establish connection to vector store service, but continuing startup")

@app.post("/upload-document")
async def upload_document(file: UploadFile = File(...)) -> Dict:
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        # Generate unique document ID
        doc_id = str(uuid.uuid4())
        logger.info(f"Processing upload for document ID: {doc_id}")
        
        # Save the uploaded file
        file_path = os.path.join(UPLOAD_DIR, f"{doc_id}.pdf")
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        logger.info(f"File saved successfully at: {file_path}")
        
        # Send to vector store service
        params = {
            'file_path': file_path,
            'doc_id': doc_id
        }
        
        response = requests.post(f"{VECTOR_STORE_URL}/process-document", params=params)
        response.raise_for_status()
        
        # Send to vector store service
        response = requests.post(
            f"{VECTOR_STORE_URL}/process-document",
            params={"file_path": file_path, "doc_id": doc_id}
        )
        response.raise_for_status()
        
        return {
            "message": "Document uploaded and processed successfully",
            "doc_id": doc_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search-doc")
async def search_doc(query: str, limit: int = 5) -> List[Dict]:
    try:
        response = requests.get(
            f"{VECTOR_STORE_URL}/search",
            params={"query": query, "limit": limit}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)