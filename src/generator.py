from groq import Groq
from dotenv import load_dotenv
from src.retrieval import retrieve
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_answer(query):
    
    chunks = retrieve(query, k=3)
    
    
    context = "\n\n".join([
        f"Source {i+1}:\n{chunk.page_content}" 
        for i, chunk in enumerate(chunks)
    ])
    
    
    prompt = f"""You are a legal assistant specializing in Indian Supreme Court judgments.
    
Answer the question using ONLY the context provided below.
Synthesize information from the sources to form a complete answer.
Always cite which source number you used (e.g. "According to Source 1...").
If the answer is truly not present in the context at all, only then say "I cannot find this in the provided documents."
Do NOT use any knowledge outside the provided context.

Always cite which source you used.

Context:
{context}

Question: {query}

Answer:"""

    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    
    answer = response.choices[0].message.content
    return answer, chunks

if __name__ == "__main__":
    query = "What are the fundamental rights related to personal liberty?"
    answer, sources = generate_answer(query)
    
    print(f"\nQuestion: {query}")
    print(f"\nAnswer:\n{answer}")
    print("\nSources used:")
    for i, chunk in enumerate(sources):
        print(f"\nSource {i+1}: {chunk.page_content[:150]}...")