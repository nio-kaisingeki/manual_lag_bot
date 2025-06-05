FROM python:3.12-slim

WORKDIR /app

# 必要なビルドツールを追加
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]





# # Python 3.12（M1/M2 Macでも問題なし）
# FROM python:3.12-slim

# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1


# WORKDIR /app

# # 必要なビルドツールをインストール
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     gcc \
#     libffi-dev \
#     libxml2-dev \
#     libxslt1-dev \
#     libjpeg-dev \
#     zlib1g-dev \
#     && rm -rf /var/lib/apt/lists/*

# COPY requirements.txt .
# RUN pip install --upgrade pip && pip install -r requirements.txt

# COPY . .

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
