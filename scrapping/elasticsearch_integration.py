from opensearchpy import OpenSearch
from sentence_transformers import SentenceTransformer
import pandas as pd

# OpenSearch bağlantısı
host = "https://search-yargitaykarararama-s6fvvuwuaklfdzljip3tsajrny.aos.eu-north-1.on.aws"
username = "admin"  # Kullanıcı adı (IAM'den alınabilir)
password = "201675K.c"          # Şifre (IAM token veya manuel şifre)

client = OpenSearch(
    hosts=[host],
    http_auth=(username, password),
    use_ssl=True,
    verify_certs=True
)

# SBERT modeli yükleniyor
model = SentenceTransformer('all-MiniLM-L6-v2')

# CSV'den verileri yükleme
csv_dosyasi = "yargitay_kararlari.csv"
veri = pd.read_csv(csv_dosyasi)

# OpenSearch index adı
index_name = "yargitay-kararlari"

# İndex'in varlığını kontrol et ve oluştur
if not client.indices.exists(index=index_name):
    client.indices.create(index=index_name)
    print(f"Index '{index_name}' oluşturuldu.")

# Verileri OpenSearch'e gönderme
for idx, row in veri.iterrows():
    doc = {
        "baslik": row["baslik"],  # Kararın başlığı
        "metin": row["metin"],    # Kararın metni
        "vektor": model.encode(row["metin"]).tolist()  # Metin için SBERT vektörü
    }
    res = client.index(index=index_name, id=row["id"], body=doc)
    print(f"Veri eklendi: {res['result']}")
