# AI Vector Store

A simple document search solution using LanceDB for vector storage and similarity search. The solution consists of two services:

1. API Backend (Port 8000): Handles document uploads and search requests
2. Vector Store (Port 8001): Manages document storage and vector search using LanceDB

## Quick Start with Docker

The easiest way to run the services is using Docker Compose:

```bash
# Build and start the services
docker-compose up --build

# The services will be available at:
# - API Backend: http://localhost:8000
# - Vector Store: http://localhost:8001
```

Both services will start, and the API backend will wait for the vector store to be healthy before starting.

## Setup

### Using Docker (Recommended)

1. Make sure you have Docker and Docker Compose installed
2. Build and start the services:
```bash
docker-compose up --build
```

### Manual Setup (Alternative)

1. Create and activate a Python virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies for both services:
```bash
cd api-backend
pip install -r requirements.txt
cd ../vector-store
pip install -r requirements.txt
```

## Running the Services

### Using Docker (Recommended)

1. Start both services:
```bash
docker-compose up
```

The services will be available at:
- API Backend: http://localhost:8000
- Vector Store: http://localhost:8001

### Manual Setup (Alternative)

1. Start the Vector Store service:
```bash
cd vector-store
python main.py
```

2. In a new terminal, start the API Backend service:
```bash
cd api-backend
python main.py
```

## API Usage

### 1. Upload a Document

```bash
curl -X POST -F "file=@path/to/your/document.pdf" http://localhost:8000/upload-document
```

Response:
```json
{
    "message": "Document uploaded and processed successfully",
    "doc_id": "generated-uuid"
}
```

### 2. Search Documents

```bash
curl "http://localhost:8000/search-doc?query=your search query&limit=5"
```

Response:
```json
[
    {
        "text": "matching text snippet",
        "doc_id": "document-uuid",
        "page_num": 1,
        "line_num": 0
    }
]
```

## Features

- PDF document processing
- Vector-based similarity search
- Contextual text chunks for better search results
- Unique document IDs for reference
- Page and line number tracking for precise location reference