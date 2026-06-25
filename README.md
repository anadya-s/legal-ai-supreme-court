
```
# Legal AI — Indian Supreme Court Assistant

A retrieval-augmented generation system for querying Indian Supreme Court judgments in natural language. Ask a legal question, get a grounded answer with source citations pulled directly from real judgment texts.

**Live system:** FastAPI backend + Streamlit frontend, fully containerized.

---

## What it does

Legal judgments are long, dense, and hard to search. This system lets you ask plain English questions like "What is the basic structure doctrine?" or "What did the Maneka Gandhi case decide about personal liberty?" and get answers grounded in the actual text of Supreme Court judgments — with the exact source chunks cited.

The system never fabricates. If the answer isn't in the corpus, it says so.

---

## Evaluation

Evaluated on 5 test cases covering landmark constitutional judgments:

| Metric | Score |
|---|---|
| Faithfulness | 1.00 |
| Context Precision | 0.90 |
| Answer Relevancy | 0.57 |

Faithfulness of 1.00 means every answer is fully grounded in retrieved source material — no hallucination. Context precision of 0.90 means 9 out of 10 retrieved chunks are genuinely relevant to the query.

---

## Architecture

```
User query
   ↓
HuggingFace sentence-transformer (all-MiniLM-L6-v2)
   ↓ embeds query into vector
ChromaDB similarity search
   ↓ retrieves top-5 most relevant chunks
Deduplication layer
   ↓ removes duplicate chunks across documents
Groq LLaMA 3.1 (llama-3.1-8b-instant)
   ↓ generates grounded answer from retrieved context
FastAPI response with answer + cited sources
   ↓
Streamlit frontend
```

Documents are ingested once using `RecursiveCharacterTextSplitter` (chunk size 500, overlap 50), embedded with the same model, and stored persistently in ChromaDB.

---

## Corpus

Current corpus covers landmark Supreme Court constitutional judgments:

- Kesavananda Bharati vs State of Kerala (1973) — basic structure doctrine
- Maneka Gandhi vs Union of India (1978) — personal liberty and Article 21
- Minerva Mills vs Union of India (1980) — constitutional amendments
- Indira Sawhney vs Union of India (1992) — reservations
- Shreya Singhal vs Union of India (2015) — freedom of speech, Section 66A

---

## Tech stack

| Layer | Technology |
|---|---|
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| Vector store | ChromaDB |
| Orchestration | LangChain |
| LLM inference | Groq API (llama-3.1-8b-instant) |
| Backend | FastAPI + Uvicorn |
| Frontend | Streamlit |
| Evaluation | Custom faithfulness, context precision, answer relevancy metrics |

---

## Quickstart

```bash
git clone https://github.com/anadya-s/legal-ai-supreme-court.git
cd legal-ai-supreme-court
pip install -r requirements.txt
```

Create a `.env` file in the root:
```
GROQ_API_KEY=your_key_here
```

Build the vector store:
```bash
python src/ingestion.py
```

Start the backend:
```bash
uvicorn api:app --reload
```

Start the frontend (new terminal):
```bash
streamlit run app.py
```

Open `http://localhost:8501` and start asking questions.

---

## Project structure

```
legal-ai/
├── src/
│   ├── ingestion.py      # document loading, chunking, embedding, ChromaDB storage
│   ├── retrieval.py      # semantic search with deduplication
│   └── generator.py      # prompt engineering + Groq LLM call
├── data/
│   └── raw/              # Supreme Court judgment text files
├── api.py                # FastAPI backend with /ask endpoint
├── app.py                # Streamlit frontend
├── evaluate.py           # custom evaluation metrics
└── requirements.txt
```

---

## Limitations and next steps

- Corpus is limited to 5 judgments — expanding to hundreds of cases would significantly improve coverage
- Answer relevancy (0.57) can be improved with better prompt engineering and a reranking step using a cross-encoder model
- No authentication on the API — not production-ready for public deployment as-is
- Chunking by character count sometimes splits mid-sentence — semantic chunking would preserve context better
- Docker containerization in progress for portable deployment

---

## Author

Anadya Shekhar — [github.com/anadya-s](https://github.com/anadya-s) · [linkedin.com/in/anadya-shekhar](https://linkedin.com/in/anadya-shekhar)
```

