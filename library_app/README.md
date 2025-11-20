# Biblioteca GUI (Tkinter) - Demo

Requisitos:
- Python 3.10+ (recomendado)
- PostgreSQL en funcionamiento
- El archivo SQL original con DDL y datos (tu archivo): talller 8.txt

## 1) Crear la base de datos
Asumiendo que tienes PostgreSQL y psql:
```bash
createdb biblioteca_demo

docker run -d \
  --name postgres-biblioteca \
  -e POSTGRES_USER=usuario \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=biblioteca_demo \
  -p 5433:5432 \
  postgres:15

# o con usuario:
# createdb -U tu_usuario biblioteca_demo
