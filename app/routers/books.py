from fastapi import APIRouter, HTTPException
from app.schemas.book import LivroCriacao

router = APIRouter(prefix="/books", tags=["Livros"])

livros = [
    {"id": 1, "titulo": "Dom Casmurro", "autor": "Machado de Assis"},
    {"id": 2, "titulo": "O Cortiço", "autor": "Aluísio Azevedo"}
]

@router.get("")
def listar_livros():
    return livros

@router.get("/search")
def pesquisar_livros(titulo: str | None = None, autor: str | None = None):
    resultados = []

    for livro in livros:
        corresponde_titulo = titulo is None or titulo.lower() in livro["titulo"].lower()
        corresponde_autor = autor is None or autor.lower() in livro["autor"].lower()

        # Seu desafio:
        if corresponde_titulo and corresponde_autor:
            resultados.append(livro)
        # Se corresponde_titulo E corresponde_autor forem True,
        # adicione o livro à lista resultados.

    return resultados

@router.get("/{id}")
def buscar_livro(id: int):
    for livro in livros:
        if livro["id"] == id:
            return livro
    raise HTTPException(status_code=404, detail="Item not found")

@router.post("", status_code=201)
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


@router.put("/{id}")
def atualizar_livro(id: int, dados: LivroCriacao):
    for livro in livros:
        if livro["id"] == id:
            livro["titulo"] = dados.titulo
            livro["autor"] = dados.autor
            return {"id": id, "titulo": dados.titulo, "autor": dados.autor}

    raise HTTPException(status_code=404, detail="Item not found")

@router.delete("/{id}")
def excluir_livro(id: int):
    for livro in livros:
        if livro["id"] == id:
            livros.remove(livro)
            return {"mensagem": "Livro excluído com sucesso"} 
    raise HTTPException(status_code=404, detail="Item not found")
