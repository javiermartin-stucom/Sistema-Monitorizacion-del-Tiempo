FROM python:3.11-slim

WORKDIR /app

RUN pip install flask requests

COPY exporter.py .

EXPOSE 8000

CMD ["python", "exporter.py"]
