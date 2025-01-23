from flask import Flask
from flask_cors import CORS
from routes.search import search_blueprint

app = Flask(__name__)
CORS(app)  # CORS'i etkinleştir

# Arama rotasını ekle
app.register_blueprint(search_blueprint)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
