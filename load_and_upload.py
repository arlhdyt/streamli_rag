# upload_with_nodeparser_manual.py
import os
from pathlib import Path
import uuid
import weaviate
import weaviate.classes as wvc
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceWindowNodeParser
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# 1. Aktifkan GPU
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# 2. Load markdown file
documents = SimpleDirectoryReader(input_files=["docs/hasil_pneumonia_parsing6.md"]).load_data()

# 3. Connect ke Weaviate
client = weaviate.connect_to_local()
collection = client.collections.get("MedicalChunk")

# 4. Load model HuggingFace + GPU
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

# 5. SentenceWindow chunking
parser = SentenceWindowNodeParser.from_defaults(window_size=3)
nodes = parser.get_nodes_from_documents(documents)

texts = [node.get_content() for node in nodes]
vectors = embed_model.get_text_embedding_batch(texts)  # ✅ FIXED LINE

# 6. Upload manual
for text, vector in zip(texts, vectors):
    collection.data.insert(
        properties={
            "text": text,
            "source": "hasil_pneumonia_parsing6.md"
        },
        vector=vector,
        uuid=str(uuid.uuid4())
    )

print(f"✅ Uploaded {len(texts)} chunks with embedding.")
client.close()
