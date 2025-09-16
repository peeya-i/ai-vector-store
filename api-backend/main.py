from fastapi import FastAPI, UploadFile, File, HTTPException
import os
import uuid
import requests
from typing import Dict, List

app = FastAPI()

# Configuration
VECTOR_STORE_URL = "http://localhost:8001"
UPLOAD_DIR = "uploads"

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-document")
async def upload_document(file: UploadFile = File(...)) -> Dict:
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        # Generate unique document ID
        doc_id = str(uuid.uuid4())
        
        # Save the uploaded file
        file_path = os.path.join(UPLOAD_DIR, f"{doc_id}.pdf")
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
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