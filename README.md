# MCP-RAG-Chatbot: Full Stack Implementation Guide

A retrieval-augmented generation chatbot for Model Context Protocol documentation. Questions get answered with precision, grounded in real MCP docs.

## Project Architecture

```
User → Web UI (Flask) → RAG Engine (FAISS + LLM) → MCP Documentation
```

## Stack Overview

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask, LangChain
- **AI**: OpenAI API, SentenceTransformers
- **Data**: FAISS vector store
- **Source**: GitHub API for document fetching

## Quick Setup

```bash
# Clone repository
git clone https://github.com/Goose4500/mcp-rag-chatbot.git
cd mcp-rag-chatbot

# Environment setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env with your OpenAI API key and optional GitHub token

# Run application
python app.py
```

Access at http://localhost:5000

## Project Completion Roadmap

### 1. Setup (Complete)
- ✅ Core files structure
- ✅ Basic dependencies 
- ✅ GitHub repository

### 2. Data Pipeline (Next Steps)
- Connect GitHub API
- Test document fetching
- Implement chunking and embedding
- Verify FAISS index creation

### 3. RAG Implementation
- Test vector search functionality
- Implement prompt engineering
- Connect OpenAI API
- Test basic Q&A capability

### 4. Frontend Enhancement
- Improve chat interface
- Add conversation history
- Implement loading states
- Add citation support

### 5. Deployment
- Containerize with Docker
- Setup CI/CD pipeline
- Deploy to cloud platform
- Configure monitoring

## Development Workflow

1. **Branch Strategy**:
   - `main`: Production-ready code
   - `dev`: Development work
   - Feature branches: `feature/name`

2. **Commit Workflow**:
   ```bash
   git checkout -b feature/new-feature
   # Make changes
   git add .
   git commit -m "Add feature: description"
   git push origin feature/new-feature
   # Create PR to dev branch
   ```

3. **Testing**:
   - Test embedding process: `python process_docs.py`
   - Test document fetching: `python fetch_docs.py`
   - Test full system: `python app.py`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| FAISS import error | `pip install --no-cache-dir faiss-cpu` |
| OpenAI API errors | Check API key, verify credit balance |
| Empty responses | Check vector index creation, verify chunks exist |
| Slow performance | Reduce `TOP_K` value in `rag_engine.py` |

## Optimizations

- Switch to `faiss-gpu` for 10× speed boost on GPU machines
- Reduce embedding dimension for faster but less accurate search
- Implement response caching for common questions
- Use streaming responses for better UX

## Final Deployment Checklist

- [ ] Secure API keys (environment variables)
- [ ] Set debug=False in production
- [ ] Implement rate limiting
- [ ] Add error logging
- [ ] Create backup strategy for vector store
- [ ] Setup monitoring alerts
- [ ] Document API endpoints

## Contribution

1. Fork the repo
2. Create feature branch
3. Commit changes
4. Push to your branch
5. Open pull request

## License

MIT

---

## Resources

- [Model Context Protocol](https://github.com/modelcontextprotocol)
- [LangChain Documentation](https://python.langchain.com/docs/get_started)
- [FAISS Wiki](https://github.com/facebookresearch/faiss/wiki)
- [SentenceTransformers Documentation](https://www.sbert.net/)
