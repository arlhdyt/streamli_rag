import weaviate
import weaviate.classes as wvc
from weaviate.classes.config import DataType

client = weaviate.connect_to_local()

class_name = "MedicalChunk"

if class_name in client.collections.list_all():
    print(f"✅ Class '{class_name}' already exists.")
else:
    client.collections.create(
        name=class_name,
        vectorizer_config=wvc.config.Configure.Vectorizer.none(),
        properties=[
            wvc.config.Property(name="text", data_type=DataType.TEXT),
            wvc.config.Property(name="source", data_type=DataType.TEXT),
            wvc.config.Property(name="tag", data_type=DataType.TEXT),
        ]
    )
    print(f"✅ Class '{class_name}' successfully created.")

client.close()
