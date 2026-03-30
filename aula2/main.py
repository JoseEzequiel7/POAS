from fastapi import FastAPI
from models import Usuario
from typing import List

usuarios:List[Usuario] = []
app = FastAPI()

@app.get('/usuarios' , response_model=List[Usuario])
def listar()->List[Usuario]:
    return usuarios

@app.post('/usuarios')
def cadastrar(usuario:Usuario):
    if usuario:
        usuarios.append(usuario)
