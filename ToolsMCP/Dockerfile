FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 9000

CMD ["fastmcp", "run", "server.py:mcp", "--transport", "http", "--port", "9000"]