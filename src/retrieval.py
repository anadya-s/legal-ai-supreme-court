from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

CHROMA_DIR = "chroma_db"

def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    vectorstore = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )
    return vectorstore

def retrieve(query, k=3):
    vectorstore = load_vectorstore()
    results = vectorstore.similarity_search(query, k=k)
    return results

if __name__ == "__main__":
    query = "What are the fundamental rights related to personal liberty?"
    results = retrieve(query)
    
    print(f"\nQuery: {query}\n")
    print("="*50)
    for i, doc in enumerate(results):
        print(f"\nChunk {i+1}:")
        print(doc.page_content)
        print("-"*50)