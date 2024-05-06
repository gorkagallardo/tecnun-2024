FROM python:3.8-slim
RUN mkdir -p /app
WORKDIR /app
EXPOSE 4000
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
