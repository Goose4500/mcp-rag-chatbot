# MCP RAG Chatbot

A domain-specific retrieval-augmented chatbot for the Model Context Protocol (MCP). Ground your AI interactions in facts, not hallucinations.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-brightgreen)

## Project Overview

This chatbot leverages Retrieval-Augmented Generation (RAG) to provide accurate, contextual responses about the Model Context Protocol. Unlike generic LLMs, it grounds all answers in official MCP documentation, eliminating hallucinations while maintaining conversational fluidity.

## Key Features

- **Real-time GitHub Synchronization**: Automatically fetches and indexes the latest MCP documentation
- **Semantic Search**: Uses FAISS vector search for high-precision document retrieval
- **Context-Aware Responses**: Intelligently combines retrieved documentation with LLM capabilities
- **Clean Web Interface**: Intuitive chat UI requiring zero training
- **Single-File Architecture**: Each component lives in one file for rapid comprehension and modification

## Architecture

```
┌─────────────┐    ┌──────────────┐    ┌───────────────┐    ┌──────────────┐
│ User Query  │───►│  Web Server  │───►│ Query Encoder │───►│ FAISS Search │
└─────────────┘    │    (Flask)   │    └───────────────┘    └──────┬───────┘
                   └──────┬───────┘                                │
┌─────────────┐          │           ┌───────────────┐    ┌────────▼───────┐
│   Response  │◄─────────┴───────────┤  LLM Service  │◄───┤ Context Builder│
└─────────────┘                      │   (OpenAI)    │    └────────▲───────┘
                                     └───────────────┘            │
                           ┌───────────────────────────────┐      │
                           │ Document Processing Pipeline  │──────┘
                           └─┬─────────────────────────┬──┘
                             │                         │
               ┌─────────────▼───┐             ┌───────▼───────┐
               │  GitHub Repos   │             │ Local Storage │
               └─────────────────┘             └───────────────┘
```

## Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key
- GitHub token (optional)

### Installation

```bash
# Clone this repository (if using git)
git clone https://your-repo-url/mcp-rag-chatbot.git
cd mcp-rag-chatbot

# OR navigate to the downloaded directory
cd /Users/goose/Downloads/mcp-rag-chatbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env to add your API keys
```

### Running the Application

```bash
python app.py
```

Access the chatbot at [http://localhost:5000](http://localhost:5000)

## Advanced Configuration

### Customizing the Retrieval Engine

Edit `rag_engine.py` to modify these parameters:

```python
# Number of chunks to retrieve per query
TOP_K = 5  

# Embedding model (smaller = faster, larger = more accurate)
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# LLM model and parameters
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",  # Change to gpt-4 for higher accuracy
    temperature=0.2,             # Decrease for more factual responses
    api_key=OPENAI_API_KEY
)
```

### Document Processing Options

In `process_docs.py`, customize:

```python
# Chunk size for document splitting
CHUNK_SIZE = 500  # Characters per chunk

# Overlap between chunks prevents context loss
CHUNK_OVERLAP = 100
```

### Adding Custom Data Sources

Modify `fetch_docs.py` to include additional GitHub repositories:

```python
REPOS = [
    ('modelcontextprotocol', 'docs'),
    ('modelcontextprotocol', 'specification'),
    # Add your repos here:
    ('your-username', 'your-repo'),
]
```

## API Reference

### Web Interface

- `GET /`: Main chat interface
- `POST /chat`: Submit queries and receive responses
  - Request body: `{"message": "Your question here"}`
  - Response: `{"response": "AI-generated answer"}`

### Core Components

- `fetch_docs.py`: GitHub documentation retrieval
  - `fetch_documentation()`: Main entry point
- `process_docs.py`: Document processing pipeline
  - `process_documents()`: Creates embeddings and FAISS index
- `rag_engine.py`: Retrieval and generation
  - `retrieve(query, k)`: Get relevant documents
  - `generate(query)`: Create RAG-enhanced response

## Performance Optimization

### Vector Search

- Use `faiss-gpu` instead of `faiss-cpu` for 10x faster search on compatible hardware
- Increase `CHUNK_SIZE` for faster indexing (at the cost of retrieval precision)

### Embedding Generation

- Batch document processing for faster throughput
- Use smaller embedding models for speed, larger for accuracy

### Web Server

- Switch to Gunicorn for production deployments:
  ```bash
  pip install gunicorn
  gunicorn -w 4 -b 0.0.0.0:5000 app:app
  ```

## Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| "No module named 'faiss'" | Run `pip install faiss-cpu` (or `faiss-gpu`) separately |
| Slow initial startup | Normal: first run downloads and processes docs |
| GitHub API rate limiting | Create a token with `public_repo` scope |
| "Invalid API key" | Ensure OPENAI_API_KEY is set in .env |
| High memory usage | Reduce `TOP_K` or use smaller embedding model |

### Debugging

Enable debug logging in any component:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin new-feature`
5. Submit a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add tests for new functionality
- Update documentation for API changes

## License

MIT License - See LICENSE file for details

## Acknowledgments

- [LangChain](https://github.com/langchain-ai/langchain) for RAG components
- [FAISS](https://github.com/facebookresearch/faiss) for vector search
- [SentenceTransformers](https://github.com/UKPLab/sentence-transformers) for embeddings
- [Model Context Protocol](https://github.com/modelcontextprotocol) for documentation

---

## Roadmap

- [ ] Multi-model support (Llama, Mistral, etc.)
- [ ] Streaming responses
- [ ] Document feedback mechanism
- [ ] Automated testing
- [ ] Docker containerization