import weaviate
from weaviate.classes.query import Filter

client = weaviate.connect_to_local()
collection = client.collections.get("MedicalChunk")

# Hapus semua objek dengan properti "text" yang berisi string apapun
result = collection.data.delete_many(
    where=Filter.by_property("text").like("*"),
    verbose=True
)

print("✅ Jumlah objek yang dihapus:", result.count)
client.close()
