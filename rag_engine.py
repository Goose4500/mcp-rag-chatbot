"""
rag_engine.py - RAG implementation for retrieval and generation
"""

import os
import pickle
import logging
from typing import List, Dict, Any

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
INDEX_FILE = os.path.join(DATA_DIR, 'embeddings.faiss')
DOCS_FILE = os.path.join(DATA_DIR, 'documents.pkl')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
TOP_K = 5  # Number of chunks to retrieve

# Initialize embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Define RAG prompt template
RAG_TEMPLATE = """You are an AI assistant specialized in the Model Context Protocol (MCP).
Use the following context from the MCP documentation to answer the user's question.
If you don't know the answer based on the context, say so honestly.

### Context:
{context}

### User Question:
{question}

### Response:
"""

class RAGEngine:
    def __init__(self):
        """Initialize the RAG engine"""
        self.load_resources()
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo", 
            temperature=0.2,
            api_key=OPENAI_API_KEY
        )
        self.prompt = PromptTemplate(
            template=RAG_TEMPLATE,
            input_variables=["context", "question"]
        )
    
    def load_resources(self):
        """Load the FAISS index and document chunks"""
        try:
            # Load FAISS index
            self.index = faiss.read_index(INDEX_FILE)
            
            # Load document chunks
            with open(DOCS_FILE, 'rb') as f:
                self.docs = pickle.load(f)
                
            logger.info(f"Loaded {len(self.docs)} document chunks and FAISS index")
            return True
        except Exception as e:
            logger.error(f"Error loading resources: {e}")
            self.index = None
            self.docs = []
            return False
    
    def retrieve(self, query: str, k: int = TOP_K) -> List[Dict[str, Any]]:
        """Retrieve relevant document chunks for a query"""
        if not self.index or not self.docs:
            logger.error("Resources not loaded. Cannot retrieve.")
            return []
        
        # Encode the query
        query_vector = embedding_model.encode([query])[0]
        query_vector = query_vector.reshape(1, -1)
        
        # Normalize the query vector for cosine similarity
        faiss.normalize_L2(query_vector)
        
        # Search the index
        distances, indices = self.index.search(query_vector, k)
        
        # Get the relevant chunks
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.docs):  # Ensure valid index
                doc = self.docs[idx]
                doc['score'] = float(distances[0][i])
                results.append(doc)
        
        logger.info(f"Retrieved {len(results)} chunks for query: {query}")
        return results
    
    def generate(self, query: str) -> str:
        """Generate a response to a query using RAG"""
        # Retrieve relevant chunks
        chunks = self.retrieve(query)
        
        if not chunks:
            return "I'm sorry, but I don't have enough information to answer your question about Model Context Protocol."
        
        # Combine chunks into context
        context = "\n\n".join([f"From {chunk['file']}:\n{chunk['text']}" for chunk in chunks])
        
        # Generate response using LangChain
        formatted_prompt = self.prompt.format(context=context, question=query)
        
        try:
            response = self.llm.invoke(formatted_prompt).content
            return response
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I encountered an error while trying to answer your question. Please try again."