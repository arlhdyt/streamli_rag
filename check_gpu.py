import weaviate
client = weaviate.Client("http://localhost:8080")
print(client.schema.get())
