import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_weaviate import WeaviateVectorStore
import weaviate
import os
import sys
import torch

# 🛡️ Patch PyTorch to bypass Streamlit inspection
sys.modules["torch._classes"] = None

# --- Konfigurasi halaman ---
st.set_page_config(page_title="RAG Medis QA", layout="wide")
st.title("🧠 Medical QA dari Dokumen")

# --- Sidebar: API Key dan Pertanyaan ---
st.sidebar.subheader("🔐 API Settings")
groq_api_key = st.sidebar.text_input("Groq API Key", type="password", value=os.getenv("GROQ_API_KEY", ""))

st.sidebar.subheader("💬 Pertanyaan")
user_question = st.sidebar.text_area("Masukkan pertanyaan medis Anda:", height=100, placeholder="Contoh: Apa itu pneumonia komunitas?")

run_button = st.sidebar.button("🔎 Jalankan QA")

# --- Setup Vector Store dan Embedding ---
@st.cache_resource
def load_retriever():
    client = weaviate.connect_to_local()
    embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")

    vectorstore = WeaviateVectorStore(
        client=client,
        index_name="MedicalChunk",
        text_key="text",
        embedding=embedding_model
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    return retriever, client

retriever, client = load_retriever()

# --- Setup LLM dan Prompt ---
@st.cache_resource
def get_qa_chain():
    if not client.is_connected():
        client.connect()
    
    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model_name="llama-3.3-70b-versatile",
        temperature=0.1
    )
    
    template = """Berikut adalah informasi dari dokumen medis:
{context}

Berdasarkan informasi di atas, jawab pertanyaan berikut dengan singkat dan jelas tanpa menambahkan keterangan lain:
{question}
"""
    QA_PROMPT = PromptTemplate(input_variables=["context", "question"], template=template)

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": QA_PROMPT},
        return_source_documents=True
    )


# --- Eksekusi QA ---
if run_button and user_question:
    qa_chain = get_qa_chain()
    with st.spinner("Memproses pertanyaan Anda..."):
        try:
            result = qa_chain.invoke(user_question)
            st.success("✅ Jawaban ditemukan:")
            st.markdown(f"**🧠 Jawaban:**\n\n{result['result']}")

            st.markdown("\n---\n")
            st.markdown("**📚 Dokumen Sumber:**")
            for i, doc in enumerate(result["source_documents"], 1):
                st.markdown(f"{i}. {doc.page_content[:300]}...")

        except Exception as e:
            st.error(f"Terjadi kesalahan saat menjalankan QA Chain:\n{e}")

