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

@app.post("/enderecos", response_model=EnderecoBase)
def criar_endereco(endereco: EnderecoBase, session: SessionDep):
    usuario = session.get(Usuario, endereco.usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    db_endereco = Endereco.model_validate(endereco)
    session.add(db_endereco)
    session.commit()
    session.refresh(db_endereco)
    return db_endereco

@app.get("/enderecos", response_model=List[EnderecoBase])
def listar_enderecos(session: SessionDep):
    return session.exec(select(Endereco)).all()

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

@app.post("/produtos", response_model=ProdutoRead)
def criar_produto(produto: ProdutoBase, session: SessionDep):
    db_prod = Produto.model_validate(produto)
    session.add(db_prod)
    session.commit()
    session.refresh(db_prod)
    return db_prod

@app.get("/produtos", response_model=List[ProdutoReadCompleto]) 
def listar_produtos(session: SessionDep):
    statement = select(Produto).options(
        selectinload(Produto.categorias),
        selectinload(Produto.estoque)
    )
    return session.exec(statement).all()

@app.put("/produtos/{produto_id}", response_model=ProdutoRead)
def atualizar_produto(produto_id: int, dados: ProdutoBase, session: SessionDep):
    produto_db = session.get(Produto, produto_id)
    if not produto_db:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    dados_dict = dados.model_dump(exclude_unset=True)
    for key, value in dados_dict.items():
        setattr(produto_db, key, value)
    
    session.add(produto_db)
    session.commit()
    session.refresh(produto_db)
    return produto_db

@app.delete("/produtos/{produto_id}")
def deletar_produto(produto_id: int, session: SessionDep):
    produto = session.get(Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    session.delete(produto)
    session.commit()
    return {"message": "Produto removido com sucesso"}

@app.get("/categorias" , response_model=List[CategoriaRead])
def listar_categorias(session: SessionDep):
    return session.exec(select(Categoria)).all()

@app.post("/categorias", response_model=CategoriaRead)
def criar_categoria(categoria: CategoriaBase, session: SessionDep):
    db_cat = Categoria.model_validate(categoria)
    session.add(db_cat)
    session.commit()
    session.refresh(db_cat)
    return db_cat

@app.put("/categorias/{categoria_id}", response_model=CategoriaRead)
def atualizar_categoria(categoria_id: int, dados: CategoriaBase, session: SessionDep):
    categoria_db = session.get(Categoria, categoria_id)
    if not categoria_db:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    categoria_db.nome = dados.nome
    session.add(categoria_db)
    session.commit()
    session.refresh(categoria_db)
    return categoria_db

@app.delete("/categorias/{categoria_id}")
def deletar_categoria(categoria_id: int, session: SessionDep):
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    session.delete(categoria)
    session.commit()
    return {"message": "Categoria removida com sucesso"}

@app.post("/produtos/{produto_id}/categorias/{categoria_id}", response_model=ProdutoReadComCategorias)
def vincular_categoria(produto_id: int, categoria_id: int, session: SessionDep):
    statement = select(Produto).where(Produto.id == produto_id).options(selectinload(Produto.categorias))
    produto = session.exec(statement).first()
    categoria = session.get(Categoria, categoria_id)
    
    if not produto or not categoria:
        raise HTTPException(status_code=404, detail="Produto ou Categoria não encontrado")
    
    if categoria in produto.categorias:
        raise HTTPException(status_code=400, detail="Produto já possui esta categoria")

    produto.categorias.append(categoria)
    session.add(produto)
    session.commit()
    
    session.refresh(produto)
    return produto

@app.put("/estoque/{produto_id}")
def atualizar_estoque(produto_id: int, quantidade: int, session: SessionDep):
    estoque = session.exec(select(Estoque).where(Estoque.produto_id == produto_id)).first()
    if not estoque:
        estoque = Estoque(produto_id=produto_id, quantidade=quantidade)
    else:
        estoque.quantidade = quantidade
    session.add(estoque)
    session.commit()
    return {"message": "Estoque atualizado"}

@app.get("/estoque", response_model=List[EstoqueReadComProduto])
def listar_estoque(session: SessionDep):
    statement = select(Estoque).options(selectinload(Estoque.produto))
    estoque_total = session.exec(statement).all()
    return estoque_total

@app.post("/pedidos", response_model=PedidoRead)
def criar_pedido_com_produto(dados: PedidoCreate, session: SessionDep):
    usuario = session.get(Usuario, dados.usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    produto = session.get(Produto, dados.produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    total_pedido = produto.preco * dados.quantidade

    novo_pedido = Pedido(
        usuario_id=dados.usuario_id,
        total=total_pedido,
        status=dados.status
    )
    session.add(novo_pedido)
    session.commit() 
    session.refresh(novo_pedido)

    novo_item = ItemPedido(
        pedido_id=novo_pedido.id,
        produto_id=dados.produto_id,
        quantidade=dados.quantidade,
        preco=produto.preco 
    )
    session.add(novo_item)
    
    estoque = session.exec(select(Estoque).where(Estoque.produto_id == dados.produto_id)).first()
    if estoque:
        if estoque.quantidade < dados.quantidade:
            session.rollback() 
            raise HTTPException(status_code=400, detail="Estoque insuficiente")
        estoque.quantidade -= dados.quantidade
        session.add(estoque)

    session.commit()
    session.refresh(novo_pedido)
    
    return novo_pedido

@app.get("/pedidos", response_model=List[PedidoRead])
def listar_pedidos(session: SessionDep):
    statement = select(Pedido)
    return session.exec(statement).all()

@app.get("/pedidos/{pedido_id}", response_model=PedidoRead)
def obter_pedido(pedido_id: int, session: SessionDep):
    pedido = session.get(Pedido, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido

@app.delete("/pedidos/{pedido_id}")
def deletar_pedido(pedido_id: int, session: SessionDep):
    pedido = session.get(Pedido, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    session.delete(pedido)
    session.commit()
    return {"message": "Pedido removido com sucesso"}

@app.post("/pagamentos", response_model=PagamentoBase)
def criar_pagamento(dados: PagamentoBase, session: SessionDep):
    pedido = session.get(Pedido, dados.pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    db_pagamento = Pagamento.model_validate(dados)
    db_pagamento.status = "Confirmado" 
    db_pagamento.pago_em = datetime.now()

    pedido.status = "Pago" 
    
    session.add(db_pagamento)
    session.add(pedido)
    session.commit()
    
    session.refresh(db_pagamento)
    return db_pagamento