from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class UsuarioPapelLink(SQLModel, table=True):
    __tablename__ = "usuario_papeis"
    usuario_id: int = Field(foreign_key="usuarios.id", primary_key=True)
    papel_id: int = Field(foreign_key="papeis.id", primary_key=True)

class Papel(SQLModel, table=True):
    __tablename__ = "papeis"
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(unique=True, max_length=50)
    
    usuarios: List["Usuario"] = Relationship(back_populates="papeis", link_model=UsuarioPapelLink)

class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(max_length=100)
    email: str = Field(unique=True, max_length=150)
    senha_hash: str = Field(max_length=255)
    criado_em: datetime = Field(default_factory=datetime.now)

    papeis: List[Papel] = Relationship(back_populates="usuarios", link_model=UsuarioPapelLink)


class PapelCreate(BaseModel):
    nome: str

class PapelRead(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True

class PapelUpdate(BaseModel):
    nome: str

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha_hash: str

class UsuarioUpdate(BaseModel):
    nome: str
    email: str
    senha_hash: str

class UsuarioRead(BaseModel):
    id: int
    nome: str
    email: str
    criado_em: datetime
    papeis: List[PapelRead] = []

    class Config:
        from_attributes = True