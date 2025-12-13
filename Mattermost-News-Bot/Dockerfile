FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir requests feedparser
COPY mm_news.py /app/mm_news.py
ENTRYPOINT ["python", "/app/mm_news.py"]
