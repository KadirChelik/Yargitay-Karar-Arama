from opensearchpy import OpenSearch
from sentence_transformers import SentenceTransformer
import pandas as pd
from opensearchpy.exceptions import NotFoundError, TransportError

# OpenSearch bağlantısı
host = "https://search-yargitay-karar-arama-search-l7mql3maj2ujdb6sbrqkizyr5y.eu-central-1.es.amazonaws.com"
username = "admin"
password = "201675K.c"

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

# İndeksi varsa sil
if client.indices.exists(index=index_name):
    try:
        client.indices.delete(index=index_name)
        print(f"Index '{index_name}' silindi.")
    except Exception as e:
        print(f"Index silinirken hata oluştu: {e}")
else:
    print(f"Index '{index_name}' zaten yok.")

# Yeni index oluşturuluyor (knn_vector destekli)
try:
    index_body = {
        "settings": {
            "index": {
                "knn": True, # k-NN desteğini aktif et
                "number_of_shards": 1,  # Shard sayısı
                "number_of_replicas": 0  # Replica sayısı
            }
        },
        "mappings": {
            "properties": {
                "baslik": { "type": "text" },
                "metin": { "type": "text" },
                "vektor": {
                    "type": "knn_vector",
                    "dimension": 384
                }
            }
        }
    }

    client.indices.create(index=index_name, body=index_body)
    print(f"Index '{index_name}' oluşturuldu.")
except TransportError as e:
    print(f"Index oluşturulurken OpenSearch hatası: {e}")
except Exception as e:
    print(f"Index oluşturulurken hata oluştu: {e}")

# Verileri OpenSearch'e gönderme
for idx, row in veri.iterrows():
    try:
        vektor = model.encode(row["metin"]).tolist()
        doc = {
            "baslik": row["baslik"],
            "metin": row["metin"],
            "vektor": vektor
        }
        res = client.index(index=index_name, id=row["id"], body=doc)
        print(f"Veri eklendi (ID: {row['id']}): {res['result']}")

    except Exception as e:
        print(f"Metin işlenirken hata oluştu (ID: {row['id']}): {e}")
