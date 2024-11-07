from chromadb import Client, PersistentSettings

settings = PersistentSettings(
    path="chromadb_storage"  # Path for persistent storage
)
chroma_client = Client(settings)
