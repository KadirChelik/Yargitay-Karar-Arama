from opensearchpy import OpenSearch
from config import Config

# OpenSearch bağlantısı
client = OpenSearch(
    hosts=[Config.OPENSEARCH_URL],
    http_auth=(Config.OPENSEARCH_USERNAME, Config.OPENSEARCH_PASSWORD),
    use_ssl=True,
    verify_certs=True
)

def search_elasticsearch(query_vector):
    # OpenSearch k-NN arama sorgusu
    os_query = {
        "size": 10,  # En yakın 10 sonucu getir
        "query": {
            "knn": {
                "vektor": {
                    "vector": query_vector,
                    "k": 10  # En yakın 10 komşuyu al
                }
            }
        }
    }

    try:
        # OpenSearch sorgusunu çalıştırma
        response = client.search(index="yargitay-kararlari", body=os_query)

        # Eğer hit bulunmazsa boş döndür
        if response['hits']['total']['value'] == 0:
            print("No results found.")
            return []

        # Hit'lerden sonuçları çıkarma
        results = [
            {
                "baslik": hit["_source"]["baslik"],
                "metin": hit["_source"]["metin"],
                "skor": hit["_score"]
            }
            for hit in response['hits']['hits']
        ]
        return results
    except Exception as e:
        # Hata durumunda açıklama yazdır
        print(f"OpenSearch Query Error: {e}")
        return []
