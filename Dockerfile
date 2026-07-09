FROM python:3.12-slim

# Çalışma dizinini ayarla
WORKDIR /code

# Gerekli sistem paketlerini yükle
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Bağımlılık dosyasını kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Uygulama kodlarını kopyala
COPY . .

# FastAPI (8000) ve AudioSocket Ses Sunucusu (8010) portları
EXPOSE 8000 8010

# Uygulamayı başlat
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
