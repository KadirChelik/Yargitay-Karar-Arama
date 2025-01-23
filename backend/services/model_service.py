# services/model_service.py

from sentence_transformers import SentenceTransformer
from config import Config

# SBERT modeli yükleniyor
model = SentenceTransformer(Config.MODEL_NAME)

def encode_query(query):
    # Kullanıcı sorgusunu SBERT ile encode et
    return model.encode(query).tolist()
