# Biblioteca

Requisitos:

## 
```bash

python3 -m venv venv

source venv/bin/activate

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

#Modo desarrollo 
flet run -r library_app/src/app.py
