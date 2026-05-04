from models import *
from database import create_db, get_session
from fastapi import *
from typing import Annotated
from pydantic import *
from contextlib import asynccontextmanager
from sqlalchemy.orm import selectinload

from sqlmodel import Session, select

SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/usuarios", response_model=UsuarioRead)
def criar_usuario(usuario: UsuarioCreate, session: SessionDep):
    db_usuario = Usuario(**usuario.dict())

    session.add(db_usuario)
    session.commit()
    session.refresh(db_usuario)

    return db_usuario

@app.get("/usuarios", response_model=List[UsuarioRead])
def listar_usuarios(session: SessionDep):
    statement = select(Usuario).options(selectinload(Usuario.papeis))
    return session.exec(statement).all()

@app.put("/usuarios/{usuario_id}", response_model=UsuarioRead)
def atualizar_usuario(usuario_id: int, dados: UsuarioUpdate, session: SessionDep):
    usuario = session.get(Usuario, usuario_id)

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    for key, value in dados.dict().items():
        setattr(usuario, key, value)

    session.commit()
    session.refresh(usuario)

    return usuario

@app.delete("/usuarios/{usuario_id}")
def deletar_usuario(usuario_id: int, session: SessionDep):
    usuario = session.get(Usuario, usuario_id)

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    session.delete(usuario)
    session.commit()

    return {"message": "Usuário deletado"}

@app.post("/papeis", response_model=PapelRead)
def criar_papel(papel: PapelCreate, session: SessionDep):
    db_papel = Papel(**papel.dict())

    session.add(db_papel)
    session.commit()
    session.refresh(db_papel)

    return db_papel

@app.get("/papeis", response_model=List[PapelRead])
def listar_papeis(session: SessionDep):
    return session.exec(select(Papel)).all()

@app.put("/papeis/{papel_id}", response_model=PapelRead)
def atualizar_papel(papel_id: int, dados: PapelUpdate, session: SessionDep):
    papel = session.get(Papel, papel_id)

    if not papel:
        raise HTTPException(status_code=404, detail="Papel não encontrado")

    papel.nome = dados.nome

    session.commit()
    session.refresh(papel)

    return papel

@app.delete("/papeis/{papel_id}")
def deletar_papel(papel_id: int, session: SessionDep):
    papel = session.get(Papel, papel_id)

    if not papel:
        raise HTTPException(status_code=404, detail="Papel não encontrado")

    session.delete(papel)
    session.commit()

    return {"message": "Papel deletado com sucesso"}

@app.post("/usuarios/{usuario_id}/papeis/{papel_id}")
def atribuir_papel(usuario_id: int, papel_id: int, session: SessionDep):
    usuario = session.get(Usuario, usuario_id)
    papel = session.get(Papel, papel_id)

    if not usuario or not papel:
        raise HTTPException(status_code=404, detail="Usuário ou Papel não encontrado")

    if papel in usuario.papeis:
        raise HTTPException(status_code=400, detail="Usuário já possui esse papel")

    usuario.papeis.append(papel)

    session.add(usuario)
    session.commit()

    return {"message": "Papel atribuído com sucesso"}