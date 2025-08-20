import streamlit as st
import pandas as pd
import requests
from PIL import Image
from streamlit_extras.colored_header import colored_header
from dotenv import load_dotenv
import os


load_dotenv()
API_URL = "http://localhost:8000/chat"  

st.set_page_config(page_title="BayirExpress RAG", layout="wide")

colored_header(
    label="BayirExpress RAG Chatbot",
    description="Pose tes questions sur les annonces et obtiens une réponse instantanée.",
    color_name="blue-70"
)

question = st.text_input("Pose ta question ici", placeholder="Ex: Je cherche des kilos dispo de Rabat à Fès")


if st.button("Chercher") and question:
    with st.spinner("Recherche en cours..."):
        try:
            
            response = requests.post(API_URL, json={"message": question, "history": []}, timeout=30)
            response.raise_for_status()
            data = response.json()
            answer = data.get("response", "")
            

            st.markdown(f"**Réponse générée :**\n\n{answer}")
            
            st.markdown("---")
            st.subheader("Annonces correspondantes")
            
            
            df = pd.read_csv("app/data/annonces.csv")
            

            for _, ann in df.iterrows():
                if (str(ann.get('depart','')).lower() in question.lower() or
                    str(ann.get('arrivee','')).lower() in question.lower()):
                    st.markdown(f"""
                        **Type :** {ann['annonce_type']}  
                        **Départ :** {ann['depart']}  
                        **Arrivée :** {ann['arrivee']}  
                        **Date :** {ann['date']}  
                        **Capacité :** {ann['capaciteKg']} kg  
                        **Prix :** {ann['prixParKg']} /kg  
                        **Téléphone :** {ann['telephone']}  
                        **Description :** {ann['annonce_description']}
                    """)

                    if pd.notna(ann['photos']):
                        try:
                            photos = eval(ann['photos'])
                            for url in photos:
                                st.image(url, width=200)
                        except:
                            pass
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur API : {e}")
