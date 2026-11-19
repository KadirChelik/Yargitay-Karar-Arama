# Yargıtay Karar Arama — Semantic Legal Precedent Search Engine

**Live Demo:** [yargitay-karar-arama.vercel.app](https://yargitay-karar-arama.vercel.app)

A full-stack legal precedent search engine for Turkish Supreme Court (*Yargıtay*) rulings, combining **Elasticsearch / OpenSearch** full-text indexing with **Sentence-Transformers** vector embeddings for semantic query matching.

---

## Architecture & Features

- **Hybrid & Semantic Search:** Uses `sentence-transformers` embeddings alongside Elasticsearch/OpenSearch queries to retrieve relevant legal precedents beyond exact keyword matches.
- **Data Ingestion & Scraping Pipeline (`scrapping/`):** Collects, cleans, and indexes Supreme Court rulings (`yargitay_kararlari.csv`) into Elasticsearch.
- **Containerized Search Infrastructure:** Pre-configured `docker-compose.yml` running **Elasticsearch 8.17** and **Kibana 8.17** for index inspection and analytics.
- **Modern Search UI (`frontend/`):** Fast React 18 + Vite interface for filtering rulings by chamber, decision number, and natural-language query.

---

## Tech Stack

- **Backend (`backend/`):** Python, Flask, `opensearch-py` / Elasticsearch, `sentence-transformers`
- **Search & Analytics:** Elasticsearch 8.17, Kibana 8.17 (Docker Compose)
- **Frontend (`frontend/`):** React 18, Vite, Axios

---

## Local Development

### 1. Start Elasticsearch & Kibana

```bash
docker compose up -d
```

- Elasticsearch: `http://localhost:9200`
- Kibana: `http://localhost:5601`

### 2. Run the Flask API

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python application.py
```

### 3. Run the React Frontend

```bash
cd frontend
npm install
npm run dev
```
