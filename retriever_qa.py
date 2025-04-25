from langchain_weaviate import WeaviateVectorStore
import weaviate
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

client = weaviate.connect_to_local()
embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")

vectorstore = WeaviateVectorStore(
    client=client,
    index_name="MedicalChunk",
    text_key="text",
    embedding=embedding_model
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# --- 4. Setup Groq LLM ---
llm = ChatGroq(
    groq_api_key="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",  # ⛔ Ganti dengan API Key milikmu
    model_name="llama-3.3-70b-versatile",   # ✅ Groq LLM yang mendukung context panjang
    temperature=0.1
)

# --- 5. Prompt Template (opsional, bisa pakai default juga) ---
template = """Berikut adalah informasi dari dokumen medis:
{context}

Berdasarkan informasi di atas, jawab pertanyaan berikut dengan singkat dan jelas tanpa menambahkan keterangan lain:
{question}
"""
QA_PROMPT = PromptTemplate(input_variables=["context", "question"], template=template)

# --- 6. Buat QA Chain ---
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": QA_PROMPT},
    return_source_documents=True
)
# --- 7. Tes Pertanyaan ---
query = "Apa manfaat dan cakupan pemeriksaan syndromic testing/multiplex PCR untuk pneumonia komunitas?"

try:
    result = qa_chain.invoke(query)

    print("🧠 Jawaban:\n", result["result"])
    for doc in result["source_documents"]:
        print("-", doc.metadata.get("text", "")[:120], "...")
except Exception as e:
    print("❌ Terjadi error saat menjalankan QA Chain:")
    print(e)

# --- Tutup koneksi Weaviate ---
client.close()
