from fastapi import APIRouter, HTTPException
from typing import List
from databases import Database

from app.models.item import Item, ItemIn
from app.models.db import items

router = APIRouter()

def get_database():
    from app.main import database
    return database

@router.post("/itens/", response_model=Item, tags=["Itens"])
async def criar_item(item: ItemIn):
    database = get_database()
    try:
        query = items.insert().values(nome=item.nome, descricao=item.descricao)
        last_id = await database.execute(query)
        return {"id": last_id, **item.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/itens/", response_model=List[Item], tags=["Itens"])
async def listar_itens():
    database = get_database()
    try:
        query = items.select()
        result = await database.fetch_all(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/itens/{item_id}", response_model=Item, tags=["Itens"])
async def obter_item(item_id: int):
    database = get_database()
    try:
        query = items.select().where(items.c.id == item_id)
        item = await database.fetch_one(query)
        if item is None:
            raise HTTPException(status_code=404, detail="Item não encontrado")
        return item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/itens/{item_id}", response_model=Item, tags=["Itens"])
async def atualizar_item(item_id: int, item: ItemIn):
    database = get_database()
    try:
        query = items.update().where(items.c.id == item_id).values(nome=item.nome, descricao=item.descricao)
        await database.execute(query)
        return {"id": item_id, **item.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/itens/{item_id}", tags=["Itens"])
async def deletar_item(item_id: int):
    database = get_database()
    try:
        query = items.delete().where(items.c.id == item_id)
        item = await database.fetch_one(items.select().where(items.c.id == item_id))
        if not item:
            raise HTTPException(status_code=404, detail="Item não encontrado")
        await database.execute(query)
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
