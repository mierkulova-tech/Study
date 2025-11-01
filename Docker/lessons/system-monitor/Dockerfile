FROM python:latest

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY memory_info.py .

RUN mkdir -p /app/data

ENTRYPOINT ["python3", "memory_info.py"]