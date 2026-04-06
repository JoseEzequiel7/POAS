from fastapi import FastAPI
from models import *

app = FastAPI()

livros = []
usuarios = []
emprestimos = []

@app.post("/livros")
def criar_livro(livro: Livros):
    livros.append(livro)
    return livro

@app.get("/livros")
def listar_livros():
    return livros

@app.get("/livros/{id}")
def buscar_livro(id: int):
    for livro in livros:
        if livro.id == id:
            return livro
    return {"erro": "Livro não encontrado"}

@app.put("/livros/{id}")
def atualizar_livro(id: int, livro_atualizado: Livros):

    for i, livro in enumerate(livros):
        if livro.id == id:
            livro_atualizado.id = id
            livros[i] = livro_atualizado
            return livro_atualizado

    return {"erro": "Livro não encontrado"}

@app.delete("/livros/{id}")
def deletar_livro(id: int):
    for livro in livros:
        if livro.id == id:
            livros.remove(livro)
            return {"mensagem": "Livro removido"}
    return {"erro": "Livro não encontrado"}

@app.post("/usuarios")
def criar_usuario(usuario: Usuario):
    usuarios.append(usuario)
    return usuario


@app.get("/usuarios")
def listar_usuarios():
    return usuarios


@app.get("/usuarios/{id}")
def buscar_usuario(id: int):
    for usuario in usuarios:
        if usuario.id == id:
            return usuario
    return {"erro": "Usuário não encontrado"}


@app.put("/usuarios/{id}")
def atualizar_usuario(id: int, usuario_atualizado: Usuario):
    for i, usuario in enumerate(usuarios):
        if usuario.id == id:
            usuarios[i] = usuario_atualizado
            return usuario_atualizado
    return {"erro": "Usuário não encontrado"}


@app.delete("/usuarios/{id}")
def deletar_usuario(id: int):
    for usuario in usuarios:
        if usuario.id == id:
            usuarios.remove(usuario)
            return {"mensagem": "Usuário removido"}
    return {"erro": "Usuário não encontrado"}

@app.post("/emprestimos")
def emprestar_livro(emprestimo: Emprestimos):

    livro_encontrado = None
    usuario_encontrado = None

    for livro in livros:
        if livro.id == emprestimo.livro_id:
            livro_encontrado = livro

    for usuario in usuarios:
        if usuario.id == emprestimo.usuario_id:
            usuario_encontrado = usuario

    if not livro_encontrado:
        return {"erro": "Livro não encontrado"}

    if not usuario_encontrado:
        return {"erro": "Usuário não encontrado"}

    if livro_encontrado.quantidade <= 0:
        return {"erro": "Livro indisponível"}

    livro_encontrado.quantidade -= 1
    emprestimos.append(emprestimo)

    return {"mensagem": "Empréstimo realizado com sucesso"}


@app.get("/emprestimos")
def listar_emprestimos():
    return emprestimos
