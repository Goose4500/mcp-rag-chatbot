"""
process_docs.py - Script to process and embed MCP documentation
"""

import os
import glob
import pickle
import logging
from typing import List, Dict, Any

import markdown
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
INDEX_FILE = os.path.join(DATA_DIR, 'embeddings.faiss')
DOCS_FILE = os.path.join(DATA_DIR, 'documents.pkl')
CHUNK_SIZE = 500  # Characters per chunk
CHUNK_OVERLAP = 100  # Character overlap between chunks

# Initialize SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')  # Small efficient model for embeddings

def read_markdown_file(file_path: str) -> str:
    """Read and convert markdown to plain text"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Convert markdown to HTML
        html = markdown.markdown(content)
        
        # Convert HTML to plain text
        soup = BeautifulSoup(html, features="html.parser")
        text = soup.get_text()
        
        return text
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return ""

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Split text into overlapping chunks"""
    if not text:
        return []
        
    chunks = []
    start = 0
    
    while start < len(text):
        end = min(start + chunk_size, len(text))
        
        # If not at the end, try to find a good breaking point
        if end < len(text):
            # Try to find the last sentence ending or space
            last_period = text.rfind('. ', start, end)
            last_space = text.rfind(' ', start, end)
            
            if last_period > start + chunk_size // 2:
                end = last_period + 1
            elif last_space > start + chunk_size // 2:
                end = last_space
        
        chunk = text[start:end].strip()
        if chunk:  # Only append non-empty chunks
            chunks.append(chunk)
        
        # Move start with overlap
        start = end - overlap if end - overlap > start else end
    
    return chunks

def process_documents() -> tuple:
    """Process all documents in the data directory and create embeddings"""
    logger.info("Starting document processing...")
    
    # Get all markdown files in the data directory and subdirectories
    md_files = []
    for root, _, _ in os.walk(DATA_DIR):
        md_files.extend(glob.glob(os.path.join(root, "*.md")))
    
    logger.info(f"Found {len(md_files)} markdown files to process")
    
    # Process each file and create chunks
    all_chunks = []
    chunk_metadata = []
    
    for file_path in md_files:
        logger.info(f"Processing {file_path}")
        
        # Get file metadata
        rel_path = os.path.relpath(file_path, DATA_DIR)
        file_name = os.path.basename(file_path)
        
        # Read and process text
        text = read_markdown_file(file_path)
        chunks = chunk_text(text)
        
        # Store chunks and their metadata
        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            chunk_metadata.append({
                'file': file_name,
                'path': rel_path,
                'chunk_index': i,
                'text': chunk
            })
    
    logger.info(f"Created {len(all_chunks)} chunks from {len(md_files)} files")
    
    # Generate embeddings for all chunks
    logger.info("Generating embeddings...")
    embeddings = model.encode(all_chunks, show_progress_bar=True)
    
    # Normalize embeddings for cosine similarity
    faiss.normalize_L2(embeddings)
    
    # Create a FAISS index
    logger.info("Creating FAISS index...")
    dimension = embeddings.shape[1]  # Get the embedding dimension
    index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity with normalized vectors
    index.add(embeddings)
    
    # Save the index and document chunks
    logger.info(f"Saving FAISS index to {INDEX_FILE}")
    faiss.write_index(index, INDEX_FILE)
    
    logger.info(f"Saving document chunks to {DOCS_FILE}")
    with open(DOCS_FILE, 'wb') as f:
        pickle.dump(chunk_metadata, f)
    
    logger.info("Document processing completed.")
    return index, chunk_metadata

if __name__ == "__main__":
    process_documents()