from bs4 import BeautifulSoup
import requests
import json
import re
import pandas as pd
import time
import os

# Veri çekme fonksiyonu
def karar_verisini_cek(url, id):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("URL isteği sırasında hata oluştu:", e)
        return None

    # JSON olarak veriyi al
    try:
        data_json = response.json()
    except json.JSONDecodeError:
        print("JSON verisi parse edilemedi.")
        return None

    # JSON'dan HTML içeriği alma
    html_content = data_json.get("data")
    if not html_content:
        print("HTML içeriği bulunamadı.")
        return None

    # HTML içeriğini BeautifulSoup ile parse et
    soup = BeautifulSoup(html_content, 'html.parser')

    # Başlık kısmını yalnızca <b> etiketinden alıyoruz
    baslik_tag = soup.find('b')
    başlık = baslik_tag.get_text(strip=True) if baslik_tag else 'Başlık bulunamadı'

    # Metin kısmını "İçtihat Metni" ifadesiyle 'b' etiketinden alıyoruz
    metin_tag = soup.find('b', string=lambda x: x and 'İçtihat Metni' in x)

    # Metni bulma ve <br/> etiketlerini boşlukla değiştirme
    if metin_tag:
        metin = metin_tag.find_next('p')
        if metin:
            düzenlenmiş_metin = metin.get_text(separator=" ", strip=True)
            düzenlenmiş_metin = re.sub(r"(suç|hüküm)\s+", r"\1 ", düzenlenmiş_metin)
            düzenlenmiş_metin = re.sub(r"\s+", " ", düzenlenmiş_metin)
        else:
            düzenlenmiş_metin = 'Metin kısmı bulunamadı'
    else:
        düzenlenmiş_metin = 'Metin etiketi bulunamadı'

    # Fazla boşlukları temizle
    başlık = re.sub(r"\s+", " ", başlık)

    # ID'yi ekleyerek veriyi döndür
    return {"id": id, "baslik": başlık, "metin": düzenlenmiş_metin}

# Belirli bir id aralığında veri çekme ve CSV'ye ekleme
baslangic_id = 70000000  # Başlangıç id'si
kac_tane = 20  # Çekilecek karar sayısı
csv_dosyasi = "yargitay_kararlari.csv"  # CSV dosya adı

# Eğer CSV dosyası varsa, mevcut id'leri oku
mevcut_idler = set()
if os.path.exists(csv_dosyasi):
    try:
        mevcut_df = pd.read_csv(csv_dosyasi, usecols=["id"])
        mevcut_idler = set(mevcut_df["id"].astype(int).tolist())
    except pd.errors.EmptyDataError:
        print("CSV dosyası boş.")

for i in range(kac_tane):
    karar_id = baslangic_id + (i * 100)  # ID her adımda 100 artacak
    # ID kontrolü
    if karar_id in mevcut_idler:
        print(f"{karar_id} zaten mevcut, atlanıyor.")
        continue
    
    url = f"https://karararama.yargitay.gov.tr/getDokuman?id={karar_id}"
    karar_verisi = karar_verisini_cek(url, karar_id)
    
    if karar_verisi:
        # Yeni veriyi DataFrame olarak oluşturup CSV'ye ekle
        yeni_veri_df = pd.DataFrame([karar_verisi])
        yeni_veri_df.to_csv(csv_dosyasi, mode='a', index=False, header=not os.path.exists(csv_dosyasi), encoding='utf-8')
        print(f"{karar_id} için veri eklendi.")
    else:
        print(f"{karar_id} için veri bulunamadı veya işlenemedi.")
    
    time.sleep(1)  # Sunucuyu zorlamamak için kısa bir gecikme
