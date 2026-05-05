from typing import Annotated, List
from fastapi import *
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from contextlib import asynccontextmanager
from database import *
from models import *

SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield

app = FastAPI(lifespan=lifespan)


@app.post("/usuarios", response_model=UsuarioRead)
def criar_usuario(usuario: UsuarioBase, session: SessionDep):
    db_usuario = Usuario.model_validate(usuario)
    session.add(db_usuario)
    session.commit()
    session.refresh(db_usuario)
    return db_usuario

@app.get("/usuarios", response_model=List[UsuarioRead])
def listar_usuarios(session: SessionDep):
    statement = select(Usuario).options(selectinload(Usuario.papeis))
    return session.exec(statement).all()

@app.put("/usuarios/{usuario_id}", response_model=UsuarioRead)
def atualizar_usuario(usuario_id: int, dados: UsuarioBase, session: SessionDep):
    usuario_db = session.get(Usuario, usuario_id)
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    dados_dict = dados.model_dump(exclude_unset=True)
    for key, value in dados_dict.items():
        setattr(usuario_db, key, value)
    
    session.add(usuario_db)
    session.commit()
    session.refresh(usuario_db)
    return usuario_db

@app.delete("/usuarios/{usuario_id}")
def deletar_usuario(usuario_id: int, session: SessionDep):
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    session.delete(usuario)
    session.commit()
    return {"message": "Usuário deletado"}

@app.post("/papeis", response_model=PapelRead)
def criar_papel(papel: PapelBase, session: SessionDep):
    db_papel = Papel.model_validate(papel)
    session.add(db_papel)
    session.commit()
    session.refresh(db_papel)
    return db_papel

@app.get("/papeis", response_model=List[PapelRead])
def listar_papeis(session: SessionDep):
    return session.exec(select(Papel)).all()

@app.put("/papeis/{papel_id}", response_model=PapelRead)
def atualizar_papel(papel_id: int, dados: PapelBase, session: SessionDep):

    papel_db = session.get(Papel, papel_id)
    if not papel_db:
        raise HTTPException(status_code=404, detail="Papel não encontrado")
    statement = select(Papel).where(Papel.nome == dados.nome, Papel.id != papel_id)
    resultado = session.exec(statement).first()
    
    if resultado:
        raise HTTPException(
            status_code=400, 
            detail=f"O nome '{dados.nome}' já está em uso por outro papel."
        )

    papel_db.nome = dados.nome
    
    session.add(papel_db)
    session.commit()
    session.refresh(papel_db)
    
    return papel_db

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

    return {"message": f"Papel '{papel.nome}' atribuído a '{usuario.nome}'"}