import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from app.data_loader import load_annonces
from app.generator import generate_answer

class RAGPipeline:
    def __init__(self, csv_path: str):
        # Charger modèle d'embedding
        self.model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        
        # Charger annonces depuis CSV
        self.annonces = load_annonces(csv_path)

        # Construire index FAISS
        embeddings = [self.model.encode(a["text"]) for a in self.annonces]
        dim = embeddings[0].shape[0]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(embeddings, dtype="float32"))

    def search(self, query: str, top_k: int = 3):
        """
        Recherche les annonces les plus pertinentes pour une requête.
        """
        query_vec = self.model.encode(query)
        query_vec = np.array([query_vec], dtype="float32")
        distances, indices = self.index.search(query_vec, top_k)
        results = [self.annonces[i] for i in indices[0]]
        return results

    def answer(self, query: str) -> str:
        """
        Génère une réponse basée sur les annonces trouvées.
        """
        results = self.search(query)
        context = "\n".join([r["text"] for r in results])
        return generate_answer(query, context)
