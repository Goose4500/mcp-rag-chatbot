# Model Context Protocol RAG Chatbot

A simple RAG (Retrieval-Augmented Generation) chatbot for understanding the Model Context Protocol (MCP). This project creates a simple web interface where users can ask questions about MCP and get responses based on the official documentation.

## Features

- Fetches MCP documentation directly from GitHub repositories
- Processes markdown files to create embeddings
- Uses a vector database (FAISS) for efficient retrieval
- Implements the RAG pattern for accurate, contextual responses
- Simple, clean web interface for interacting with the chatbot

## Project Structure

```
mcp-rag-chatbot/
│
├── data/                  # Directory to store downloaded MCP documentation
├── static/                # Static files for the web interface
│   └── style.css          # Simple CSS for styling
├── templates/             # HTML templates
│   └── index.html         # Main interface template
├── app.py                 # Main application file (Flask web server)
├── fetch_docs.py          # Script to fetch MCP documentation from GitHub
├── process_docs.py        # Script to process and embed documents
├── rag_engine.py          # RAG implementation for retrieval and generation
├── .env.example           # Template for environment variables
└── requirements.txt       # Project dependencies
```