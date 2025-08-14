from pydantic import BaseModel
from typing import Optional

class ItemIn(BaseModel):
    nome: str
    descricao: Optional[str] = None

class Item(BaseModel):
    id: int
    nome: str
    descricao: Optional[str] = None

# Model para Valor
from datetime import datetime

class ValorIn(BaseModel):
    item_id: int
    valor: float

class Valor(BaseModel):
    id: int
    item_id: int
    data_cadastro: datetime
    valor: float
