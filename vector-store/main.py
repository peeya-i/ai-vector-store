from fastapi import FastAPI, HTTPException
from vector_store import VectorStore
from typing import List, Dict

app = FastAPI()
vector_store = VectorStore()

@app.post("/process-document")
async def process_document(file_path: str, doc_id: str):
    success = vector_store.process_pdf(file_path, doc_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to process document")
    return {"message": "Document processed successfully", "doc_id": doc_id}

@app.get("/search")
async def search(query: str, limit: int = 5) -> List[Dict]:
    results = vector_store.search(query, limit)
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)