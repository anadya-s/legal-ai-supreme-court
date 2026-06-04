import streamlit as st
import requests

API_URL = "http://localhost:8000/ask"

st.set_page_config(page_title="Legal AI", page_icon="⚖️")
st.title("⚖️ Indian Supreme Court Legal Assistant")
st.write("Ask any question about landmark Supreme Court judgments.")

query = st.text_input("Enter your legal question:")

if st.button("Ask") and query:
    with st.spinner("Searching through judgments..."):
        response = requests.post(API_URL, json={"question": query})
        data = response.json()
    
    st.subheader("Answer")
    st.write(data["answer"])
    
    st.subheader("Sources")
    for i, source in enumerate(data["sources"]):
        with st.expander(f"Source {i+1} — {source['source'].split('/')[-1]}"):
            st.write(source["content"])