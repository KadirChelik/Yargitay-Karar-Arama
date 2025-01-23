import requests
import time
import json

# Temel URL'yi tanımla
base_url = "https://karararama.yargitay.gov.tr/getDokuman?id="

# 60000000'dan başlayarak 100'er artışlarla 1000000000'e kadar çekilecek
for id_num in range(60000000,70000000 , 10):
    url = f"{base_url}{id_num}"  

    try:
        # İstek gönder ve yanıtı al
        response = requests.get(url, timeout=5)
        
        # Yanıtı JSON olarak ayrıştır
        data = json.loads(response.text)
        
        # Yanıt içeriğini kontrol et
        if data.get("data") is None or data.get("metadata", {}).get("FMTY") == "ERROR":
            print(f"ID {id_num} için veri yok: False")
        else:
            print(f"ID {id_num} için veri mevcut: True")

    except requests.exceptions.RequestException as e:
        # İstek sırasında bir hata oluşursa
        print(f"ID {id_num} için istek hatası: {e}")

    # Her isteğin arasında 1 saniye bekle
    time.sleep(1)
