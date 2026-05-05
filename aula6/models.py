from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime

class UsuarioPapelLink(SQLModel, table=True):
    __tablename__ = "usuario_papeis"
    usuario_id: int = Field(foreign_key="usuarios.id", primary_key=True)
    papel_id: int = Field(foreign_key="papeis.id", primary_key=True)

class PapelBase(SQLModel):
    nome: str = Field(unique=True, max_length=50)

class Papel(PapelBase, table=True):
    __tablename__ = "papeis"
    id: Optional[int] = Field(default=None, primary_key=True)
    usuarios: List["Usuario"] = Relationship(back_populates="papeis", link_model=UsuarioPapelLink)

class UsuarioBase(SQLModel):
    nome: str = Field(max_length=100)
    email: str = Field(unique=True, max_length=150)
    senha_hash: str = Field(max_length=255)

class Usuario(UsuarioBase, table=True):
    __tablename__ = "usuarios"
    id: Optional[int] = Field(default=None, primary_key=True)
    criado_em: datetime = Field(default_factory=datetime.now)
    papeis: List[Papel] = Relationship(back_populates="usuarios", link_model=UsuarioPapelLink)

class PapelRead(PapelBase):
    id: int

class UsuarioRead(UsuarioBase):
    id: int
    criado_em: datetime
    papeis: List[PapelRead] = []