from fastapi import APIRouter, HTTPException
from typing import List
import datetime
from databases import Database

from app.models.item import Valor, ValorIn
from app.models.db import valores

router = APIRouter()

def get_database():
    from app.main import database
    return database

@router.post("/valores/", response_model=Valor, tags=["Valores"])
async def criar_valor(valor: ValorIn):
    database = get_database()
    now = datetime.datetime.now()
    try:
        query = valores.insert().values(
            item_id=valor.item_id,
            valor=valor.valor,
            data_cadastro=now
        )
        last_id = await database.execute(query)
        return Valor(id=last_id, item_id=valor.item_id, valor=valor.valor, data_cadastro=now)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/valores/{item_id}", response_model=List[Valor], tags=["Valores"])
async def listar_valores_por_item(item_id: int):
    database = get_database()
    try:
        query = valores.select().where(valores.c.item_id == item_id)
        result = await database.fetch_all(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
