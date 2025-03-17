"""
app.py - Main application file for MCP RAG Chatbot
"""

import os
import logging
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Import our modules
from fetch_docs import fetch_documentation
from process_docs import process_documents
from rag_engine import RAGEngine

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Global RAG engine instance
rag_engine = None

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests"""
    global rag_engine
    
    # Ensure RAG engine is initialized
    if rag_engine is None:
        logger.error("RAG engine not initialized")
        return jsonify({
            'response': "I'm sorry, the system is still initializing. Please try again in a moment."
        })
    
    # Get user message
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({
            'response': "I didn't receive your message. Please try again."
        })
    
    # Generate response using RAG
    try:
        response = rag_engine.generate(user_message)
        return jsonify({'response': response})
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return jsonify({
            'response': "I encountered an error while processing your request. Please try again."
        })

def initialize_system():
    """Initialize the system by fetching docs, processing them, and setting up the RAG engine"""
    global rag_engine
    
    # Check if we already have the processed data
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    index_file = os.path.join(data_dir, 'embeddings.faiss')
    docs_file = os.path.join(data_dir, 'documents.pkl')
    
    if not os.path.exists(index_file) or not os.path.exists(docs_file):
        logger.info("Processed data not found. Starting data processing pipeline...")
        
        # Fetch documentation from GitHub
        fetch_documentation()
        
        # Process documents and create embeddings
        process_documents()
    
    # Initialize RAG engine
    logger.info("Initializing RAG engine...")
    rag_engine = RAGEngine()
    
    logger.info("System initialization complete.")

if __name__ == '__main__':
    # Initialize system before starting the server
    logger.info("Starting system initialization...")
    initialize_system()
    
    # Start Flask server
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)