import chromadb                                                                     # Importing ChromaDB

chroma_client = chromadb.PersistentClient(path="./chroma_db")                       ## Connecting to ChromaDB and save data in a local folder

collection = chroma_client.get_or_create_collection(name="pdf_embeddings")
