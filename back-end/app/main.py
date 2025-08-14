

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from databases import Database
from dotenv import load_dotenv
import os
import sqlalchemy

from app.models.db import items, metadata

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")

DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
database = Database(DATABASE_URL)

engine = sqlalchemy.create_engine(
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

app = FastAPI(title="Backend Python com FastAPI")

# Adiciona o middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos os domínios. Troque por uma lista específica se necessário.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def run_migrations():
    from alembic.config import Config
    from alembic import command
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), '..', 'alembic.ini'))
    command.upgrade(alembic_cfg, "head")

@app.on_event("startup")
async def startup():
    run_migrations()
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Importa e inclui as rotas
from app.routes.item_routes import router as item_router
from app.routes.valor_routes import router as valor_router
app.include_router(item_router)
app.include_router(valor_router)
