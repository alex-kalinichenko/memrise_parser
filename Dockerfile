FROM python:3.8-slim

WORKDIR /app

COPY . .

RUN pip install requests beautifulsoup4 schedule pandas matplotlib

CMD ["python", "memrise_parser.py"]