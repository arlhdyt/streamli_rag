import weaviate

client = weaviate.connect_to_local()

print(client.is_ready())  # Output: True, berarti sudah connect

# ... operasi kamu (misalnya membuat schema, upload data, dll)

client.close()  # ✅ Tambahkan ini untuk menghindari warning dan memory leak
