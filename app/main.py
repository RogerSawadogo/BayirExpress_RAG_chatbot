from fastapi import FastAPI
from pydantic import BaseModel
from app.rag import RAGPipeline

# Initialiser l'application FastAPI
app = FastAPI(title="BayirExpress RAG API")

# Initialiser le pipeline RAG
rag = RAGPipeline(csv_path="app/data/annonces.csv")

# Modèle pour la requête
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    """
    Endpoint principal du chatbot.
    """
    response = rag.answer(request.message)
    return {"question": request.message, "response": response}
