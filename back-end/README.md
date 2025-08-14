# Backend Python com FastAPI

Este projeto é um exemplo de CRUD utilizando FastAPI, acessível via Swagger UI.

## Como executar

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Suba o docker com o banco de dados:
   ```bash
   docker-compose -f docker-compose-postgresql.yml up
   ```
3. Execute o servidor:
   ```bash
   uvicorn app.main:app --reload
   ```
4. Acesse o Swagger em [http://localhost:8000/docs](http://localhost:8000/docs)

5. Para buildar a aplicação:
   ```bash
   docker build --no-cache --pull --rm -f Dockerfile -t fastapi:latest .
   ```

6. Para subir a aplicação no docker:
   ```bash
   docker-compose up -d      
   ```


