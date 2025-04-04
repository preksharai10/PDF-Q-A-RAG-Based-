import json
from fastapi import HTTPException
from config import chat_model                            # Import the configured Gemini chat model
from utils.embedding_utils import get_query_embedding    # For converting the question to an embedding
from utils.chromadb_utils import collection              # Access the ChromaDB collection where PDF data is stored
from logger_config import logger


# Function to handle question-answering for a specific PDF
async def handle_query(question: str, pdf_name: str):
    try:
         # Converting the user question into an embedding vector
        q_emb = get_query_embedding(question)

        # Search for the chunks
        search_results = collection.query(query_embeddings=q_emb, n_results=3)

        if not search_results["documents"] or not search_results["documents"][0]:
            return {"question": question, "answer": "Insufficient information available in the document."}

        retrieved_text = " ".join(search_results["documents"][0])

#prompt with clear instructions for the AI to answer based only on the document
        prompt = f"""
        You are an AI assistant that extracts precise answers from a document.

        Instructions:
        - Use only the information from the provided text.
        - Answer in a structured JSON format with keys: "summary".
        - If there is insufficient information, return: {{"summary": "Insufficient information."}}.

        Document Excerpt:
        "{retrieved_text}"

        Question: "{question}"

        Provide your answer in JSON format.
        """

        response = chat_model.generate_content(prompt)
        answer_text = response.text.strip()

        try:
            answer_json = json.loads(answer_text.strip('```json').strip('```'))
            final_answer = answer_json.get("summary", "No summary available.")
        except json.JSONDecodeError:
            final_answer = "Failed to parse AI response."

        logger.info(f"Answer generated for question: {question}")
        return {"question": question, "answer": final_answer}

    except Exception as e:
        logger.error(f"Query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")
