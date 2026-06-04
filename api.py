from fastapi import FastAPI
from pydantic import BaseModel
from src.generator import generate_answer

app = FastAPI(title="Legal AI - Supreme Court Assistant")

class Query(BaseModel):
    question: str

@app.get("/")
def root():
    return {"message": "Legal AI API is running"}

@app.post("/ask")
def ask(query: Query):
    answer, sources = generate_answer(query.question)
    return {
        "question": query.question,
        "answer": answer,
        "sources": [
            {
                "content": doc.page_content[:300],
                "source": doc.metadata.get("source", "Unknown")
            }
            for doc in sources
        ]
    }