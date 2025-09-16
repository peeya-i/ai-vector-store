import os
import logging
import lancedb
import numpy as np
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
from typing import List, Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        try:
            self.db = lancedb.connect('data/lancedb')
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.chunk_size = 3  # Number of lines to combine for context
            logger.info("VectorStore initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing VectorStore: {str(e)}")
            raise

    def create_table_if_not_exists(self):
        schema = {
            "vector": "vector[384]",
            "text": "string",
            "doc_id": "string",
            "page_num": "int",
            "line_num": "int"
        }
        
        if "documents" not in self.db.table_names():
            self.db.create_table("documents", schema=schema)
        return self.db.open_table("documents")

    def process_pdf(self, file_path: str, doc_id: str) -> bool:
        try:
            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                return False

            logger.info(f"Processing PDF: {file_path} with ID: {doc_id}")
            reader = PdfReader(file_path)
            table = self.create_table_if_not_exists()
            
            total_chunks = 0
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                lines = text.split('\n')
                
                # Process lines in chunks for better context
                for i in range(0, len(lines), self.chunk_size):
                    chunk = ' '.join(lines[i:i + self.chunk_size])
                    if not chunk.strip():
                        continue
                        
                    vector = self.model.encode(chunk)
                    
                    table.add([{
                        "vector": vector.tolist(),
                        "text": chunk,
                        "doc_id": doc_id,
                        "page_num": page_num + 1,
                        "line_num": i
                    }])
                    total_chunks += 1
            
            logger.info(f"Successfully processed document {doc_id}: {total_chunks} chunks created")
            return True
        except Exception as e:
            logger.error(f"Error processing document {doc_id}: {str(e)}")
            return False

    def search(self, query: str, limit: int = 5) -> List[Dict]:
        try:
            table = self.create_table_if_not_exists()
            query_vector = self.model.encode(query)
            
            results = (
                table.search(query_vector)
                .limit(limit)
                .select(["text", "doc_id", "page_num", "line_num"])
                .to_list()
            )
            
            return results
        except Exception as e:
            print(f"Error searching documents: {e}")
            return []