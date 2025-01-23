from opensearchpy import OpenSearch
from config import Config

# OpenSearch bağlantısı
client = OpenSearch(
    hosts=[Config.OPENSEARCH_URL],
    http_auth=(Config.OPENSEARCH_USERNAME, Config.OPENSEARCH_PASSWORD),
    use_ssl=True,
    verify_certs=True
)

def search_opensearch(query_vector):
    # OpenSearch sorgusu
    os_query = {
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'vektor') + 1.0",
                    "params": {"query_vector": query_vector}
                }
            }
        },
        "size": 10  # En iyi eşleşen 10 sonucu getir
    }
    
    # OpenSearch'ten sonuçları al
    response = client.search(index="yargitay-kararlari", body=os_query)
    results = [
        {
            "baslik": hit["_source"]["baslik"],
            "metin": hit["_source"]["metin"],
            "skor": hit["_score"]
        }
        for hit in response['hits']['hits']
    ]
    return results
