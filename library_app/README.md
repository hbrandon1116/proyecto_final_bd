# Biblioteca

Requisitos:

## 
```bash
pip install - requirements.txt

docker run -d \
  --name postgres-biblioteca \
  -e POSTGRES_USER=usuario \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=biblioteca_demo \
  -p 5433:5432 \
  postgres:15

python seed_database.py

python app.py

