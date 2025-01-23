# routes/search.py

from flask import Blueprint, request, jsonify
from services.elastic_service import search_elasticsearch
from services.model_service import encode_query

search_blueprint = Blueprint('search', __name__)

@search_blueprint.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('query', '')  # Kullanıcının sorgusu
    if not query:
        return jsonify({"error": "Sorgu gerekli"}), 400
    
    # Sorguyu modelle encode et
    query_vector = encode_query(query)

    # Elasticsearch'te ara
    results = search_elasticsearch(query_vector)

    return jsonify(results)
