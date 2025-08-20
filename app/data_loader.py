import pandas as pd

def load_annonces(csv_path: str):
    """
    Charge les annonces depuis un CSV et les formate en textes exploitables.
    """
    df = pd.read_csv(csv_path)

    annonces = []
    for _, row in df.iterrows():
        # Construire un texte descriptif pour l’index
        texte = f"Type: {row['annonce_type']} | " \
                f"Description: {row['annonce_description']} | " \
                f"Ville: {row.get('ville', '')} | " \
                f"Départ: {row.get('depart', '')} | " \
                f"Arrivée: {row.get('arrivee', '')} | " \
                f"Date: {row.get('date', '')} | " \
                f"Capacité: {row.get('capaciteKg', '')} kg | " \
                f"Prix: {row.get('prixParKg', '')} /kg | " \
                f"Téléphone: {row.get('telephone', '')}"
        
        annonces.append({"text": texte, "raw": row.to_dict()})

    return annonces
