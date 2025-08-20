import os
import requests
from dotenv import load_dotenv

load_dotenv()


API_KEY = os.getenv("API_KEY_LLAMA")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def generate_answer(query: str, context: str) -> str:
    """
    Génère une réponse finale à partir du contexte et de la question.
    """
    if not API_KEY:
        return "⚠️ API_KEY_LLAMA manquante dans .env"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "meta-llama/llama-3.3-70b-instruct:free",
        "messages": [
            {"role": "system", "content": "Tu es un assistant qui aide à trouver des annonces sur BayirExpress."},
            {"role": "user", "content": f"Question: {query}\n\nContexte (annonces trouvées):\n{context}\n\nDonne une réponse claire et utile à l'utilisateur."}
        ],
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"⚠️ Erreur API: {response.text}"
