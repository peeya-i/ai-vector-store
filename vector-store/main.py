import logging
import os
from fastapi import FastAPI, HTTPException, Form
from vector_store import VectorStore
from typing import List, Dict
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Initialize vector store with retries
MAX_RETRIES = 5
RETRY_DELAY = 2

def init_vector_store():
    for attempt in range(MAX_RETRIES):
        try:
            return VectorStore()
        except Exception as e:
            logger.error(f"Attempt {attempt + 1}/{MAX_RETRIES} to initialize VectorStore failed: {str(e)}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
            else:
                raise

vector_store = init_vector_store()
logger.info("Vector store service initialized successfully")

from fastapi import Form

@app.post("/process-document")
async def process_document(file_path: str, doc_id: str):
    logger.info(f"Processing document: {file_path} with ID: {doc_id}")
    try:
        if not os.path.exists(file_path):
            error_msg = f"File not found at path: {file_path}"
            logger.error(error_msg)
            raise HTTPException(status_code=400, detail=error_msg)
            
        success = vector_store.process_pdf(file_path, doc_id)
        if not success:
            raise HTTPException(status_code=400, detail="Failed to process document")
        
        logger.info(f"Successfully processed document: {doc_id}")
        return {"message": "Document processed successfully", "doc_id": doc_id}
    except Exception as e:
        error_msg = f"Error processing document: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

@app.get("/search")
async def search(query: str, limit: int = 5) -> List[Dict]:
    results = vector_store.search(query, limit)
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)