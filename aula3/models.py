from pydantic import BaseModel
from pydantic import EmailStr

class Usuario(BaseModel):
    id: int
    nome: str
    cpf: str
    email: EmailStr

class Livros(BaseModel):
    id: int
    titulo: str
    autor: str
    quantidade: int

class Emprestimos(BaseModel):
    usuario_id: int
    livro_id: int