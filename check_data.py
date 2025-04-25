import weaviate

# 1. Koneksi ke Weaviate lokal
client = weaviate.connect_to_local()

# 2. Ambil koleksi MedicalChunk
collection = client.collections.get("MedicalChunk")

# 3. Ambil beberapa data pertama
results = collection.query.fetch_objects(limit=5)

# 4. Tampilkan hasil
print("=== Sample data in 'MedicalChunk' ===")
for item in results.objects:
    print("-", item.properties["text"])

# 5. Jumlah total data
total = collection.aggregate.over_all(total_count=True).total_count
print(f"\nTotal chunks in collection: {total}")

client.close()
