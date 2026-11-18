from pydantic import BaseModel

class LivroCriacao(BaseModel):
    titulo: str
    autor: str