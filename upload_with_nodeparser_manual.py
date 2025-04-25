# upload_with_nodeparser_manual.py
import os
from pathlib import Path
import uuid
import weaviate
import weaviate.classes as wvc
from weaviate.classes.query import Filter
from llama_index.readers.file.markdown import MarkdownReader
from llama_index.core.node_parser import SentenceWindowNodeParser
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# 1. Aktifkan GPU
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# 2. Load markdown file
reader = MarkdownReader()
documents = reader.load_data(Path("docs/hasil_pneumonia_parsing6.md"))

# 3. Connect ke Weaviate dan ambil koleksi
client = weaviate.connect_to_local()
collection = client.collections.get("MedicalChunk")

# 4. Hapus semua isi data sebelumnya
collection.data.delete_many(
    where=Filter.by_property("text").is_not_empty()
)
print("🧹 Semua data lama dalam 'MedicalChunk' telah dihapus.")

# 5. Load model embedding HuggingFace
embed_model = HuggingFaceEmbedding(model_name="indobenchmark/indobert-base-p1")

# 6. SentenceWindow chunking
parser = SentenceWindowNodeParser.from_defaults(window_size=3)
nodes = parser.get_nodes_from_documents(documents)

# 7. Generate vectors dan upload
texts = [node.get_content() for node in nodes]
vectors = embed_model.get_text_embedding_batch(texts)

for text, vector in zip(texts, vectors):
    collection.data.insert(
        properties={
            "text": text,
            "source": "hasil_pneumonia_parsing6.md"
        },
        vector=vector,
        uuid=str(uuid.uuid4())
    )

print(f"✅ Uploaded {len(texts)} chunks with new embeddings.")
client.close()
