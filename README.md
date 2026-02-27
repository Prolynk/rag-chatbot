# RAG-Powered Chatbot

A production-grade retrieval-augmented generation (RAG) chatbot built with LangChain, ChromaDB, and OpenAI. The chatbot answers questions strictly from a custom knowledge base, with built-in hallucination prevention and feedback logging to drive continuous improvement.

## Features

- **Context-aware answers** — Retrieves relevant document chunks from ChromaDB before generating responses
- **Hallucination prevention** — Prompt engineering strictly grounds the LLM in retrieved context only
- **Feedback logging** — Every query and response is logged to SQLite with thumbs up/down tracking
- **Low solve rate analysis** — Negative feedback is stored to identify knowledge base gaps
- **Clean chat UI** — Built with Streamlit for non-technical users to validate response quality

## Tech Stack

| Tool | Purpose |
|---|---|
| LangChain v0.3+ | RAG pipeline and LCEL chain |
| ChromaDB | Vector database for document embeddings |
| OpenAI GPT-4o-mini | Response generation |
| OpenAI text-embedding-3-small | Document and query embeddings |
| Streamlit | Frontend chat interface |
| SQLite | Feedback and query logging |

## Project Structure
```
rag-chatbot/
├── docs/                   # Knowledge base documents
├── vectorstore/            # ChromaDB persistent storage
├── logs/                   # SQLite feedback database
├── src/
│   ├── ingest.py           # Document loading and embedding pipeline
│   ├── chain.py            # RAG chain logic
│   └── logger.py           # Query and feedback logging
├── .streamlit/
│   └── config.toml         # Streamlit theme configuration
├── app.py                  # Streamlit frontend
├── .env                    # API keys (not committed to Git)
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

### Prerequisites
- Python 3.10+
- An OpenAI API key from [platform.openai.com](https://platform.openai.com/api-keys)

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/Prolynk/rag-chatbot.git
cd rag-chatbot
```

**2. Create and activate virtual environment**
```bash
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add your API key**

Create a `.env` file in the root folder:
```
OPENAI_API_KEY=sk-your-key-here
```

**5. Ingest your knowledge base**
```bash
python src/ingest.py
```

**6. Run the app**
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

## How It Works

1. Documents in the `docs/` folder are loaded, chunked and embedded using OpenAI's `text-embedding-3-small` model
2. Embeddings are stored persistently in ChromaDB for fast similarity search
3. When a user submits a query, the top 3 most relevant chunks are retrieved
4. The chunks and query are passed to GPT-4o-mini with a strict system prompt that prevents hallucination
5. The response and user feedback are logged to SQLite for continuous improvement

## Feedback & Improvement Loop

Every query is logged with its response. Users can mark responses as helpful 👍 or unhelpful 👎. Negative feedback is stored separately and can be reviewed to identify gaps in the knowledge base and improve the system over time.

## Roadmap

- [ ] Expand knowledge base with scraped professional documentation
- [ ] Add web search fallback for out-of-knowledge-base queries
- [ ] Build analytics dashboard for feedback and low solve rate analysis
- [ ] Add conversation memory for multi-turn context awareness
- [ ] Deploy to Streamlit Cloud

## License

MIT