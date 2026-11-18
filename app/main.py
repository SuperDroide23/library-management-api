from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class LivroCriacao(BaseModel):
    titulo: str
    autor: str

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "library-management-api"}

livros = [
    {"id": 1, "titulo": "Dom Casmurro", "autor": "Machado de Assis"},
    {"id": 2, "titulo": "O Cortiço", "autor": "Aluísio Azevedo"}
]

@app.get("/books")
def listar_livros():
    return livros

@app.get("/books/{id}")
def buscar_livro(id: int):
    for livro in livros:
        if livro["id"] == id:
            return livro
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/books", status_code=201)
def cadastrar_livro(livro: LivroCriacao):
    novo_livro = livro.model_dump() # Transforma aquilo em um novo dicionario
    maior_id = 0 # Guarda o id de maior valor

    for livro_atual in livros:
        if livro_atual["id"] > maior_id:
            maior_id = livro_atual["id"]
    new_id = maior_id + 1
    novo_livro["id"] = new_id
    livros.append(novo_livro)
    return novo_livro

@app.put("/books/{id}")
def atualizar_livro(id: int, dados: LivroCriacao):
    for livro in livros:
        if livro["id"] == id:
            livro["titulo"] = dados.titulo
            livro["autor"] = dados.autor
            return {"id": id, "titulo": dados.titulo, "autor": dados.autor}

    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/books/{id}")
def excluir_livro(id: int):
    for livro in livros:
        if livro["id"] == id:
            livros.remove(livro)
            return {"mensagem": "Livro excluído com sucesso"} 
    raise HTTPException(status_code=404, detail="Item not found")