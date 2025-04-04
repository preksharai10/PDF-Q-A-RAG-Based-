from langchain_huggingface import HuggingFaceEmbeddings

# Load a pre-trained model to convert text into embeddings 
embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def get_embeddings(text_chunks):                        # Converting chunks of text from the PDF into embeddings
    return embeddings_model.embed_documents(text_chunks)

def get_query_embedding(question):                      # Converting the user question into an embedding 
    return embeddings_model.embed_query(question)
