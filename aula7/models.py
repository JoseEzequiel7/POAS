from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

# Rotas de linkagem
class UsuarioPapelLink(SQLModel, table=True):
    __tablename__ = "usuario_papeis"
    usuario_id: int = Field(foreign_key="usuarios.id", primary_key=True)
    papel_id: int = Field(foreign_key="papeis.id", primary_key=True)

class ProdutoCategoriaLink(SQLModel, table=True):
    __tablename__ = "produto_categorias"
    produto_id: int = Field(foreign_key="produtos.id", primary_key=True)
    categoria_id: int = Field(foreign_key="categorias.id", primary_key=True)

# Classes normais

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

class CategoriaBase(SQLModel):
    nome: str = Field(max_length=100)

class Categoria(CategoriaBase, table=True):
    __tablename__ = "categorias"
    id: Optional[int] = Field(default=None, primary_key=True)
    produtos: List["Produto"] = Relationship(back_populates="categorias", link_model=ProdutoCategoriaLink)

class CategoriaRead(CategoriaBase):
    id: int

# --- Produtos ---

class ProdutoBase(SQLModel):
    nome: str = Field(max_length=150)
    descricao: Optional[str] = None
    preco: Decimal = Field(max_digits=10, decimal_places=2)

class Produto(ProdutoBase, table=True):
    __tablename__ = "produtos"
    id: Optional[int] = Field(default=None, primary_key=True)
    criado_em: datetime = Field(default_factory=datetime.now)
    
    categorias: List[Categoria] = Relationship(back_populates="produtos", link_model=ProdutoCategoriaLink)
    estoque: Optional["Estoque"] = Relationship(back_populates="produto")
    avaliacoes: List["Avaliacao"] = Relationship(back_populates="produto")

class ProdutoRead(ProdutoBase):
    id: int
    criado_em: datetime
    
class ProdutoReadComCategorias(ProdutoRead):
    categorias: List[CategoriaRead] = []

# --- Estoque ---

class EstoqueBase(SQLModel):
    produto_id: int = Field(foreign_key="produtos.id", unique=True)
    quantidade: int

class Estoque(EstoqueBase, table=True):
    __tablename__ = "estoque"
    id: Optional[int] = Field(default=None, primary_key=True)
    atualizado_em: datetime = Field(default_factory=datetime.now)
    produto: Produto = Relationship(back_populates="estoque")

class EstoqueRead(SQLModel):
    id: int
    produto_id: int
    quantidade: int
    atualizado_em: datetime

class EstoqueReadComProduto(EstoqueRead):
    produto: ProdutoRead

class ProdutoReadCompleto(ProdutoRead):
    categorias: List[CategoriaRead] = []
    estoque: Optional[Estoque] = None

# --- Endereços ---

class EnderecoBase(SQLModel):
    rua: str = Field(max_length=150)
    cidade: str = Field(max_length=100)
    estado: str = Field(max_length=100)
    cep: str = Field(max_length=20)
    usuario_id: int = Field(foreign_key="usuarios.id")

class Endereco(EnderecoBase, table=True):
    __tablename__ = "enderecos"
    id: Optional[int] = Field(default=None, primary_key=True)

# --- Pedidos e Itens ---

class ItemPedidoBase(SQLModel):
    produto_id: int = Field(foreign_key="produtos.id")
    quantidade: int
    preco: Decimal = Field(max_digits=10, decimal_places=2)

class ItemPedido(ItemPedidoBase, table=True):
    __tablename__ = "itens_pedido"
    id: Optional[int] = Field(default=None, primary_key=True)
    pedido_id: int = Field(foreign_key="pedidos.id")

class PedidoBase(SQLModel):
    usuario_id: int = Field(foreign_key="usuarios.id")
    total: Decimal = Field(max_digits=10, decimal_places=2)
    status: str = Field(max_length=50)

class Pedido(PedidoBase, table=True):
    __tablename__ = "pedidos"
    id: Optional[int] = Field(default=None, primary_key=True)
    criado_em: datetime = Field(default_factory=datetime.now)
    pagamento: Optional["Pagamento"] = Relationship(back_populates="pedido")

class ItemPedidoRead(ItemPedidoBase):
    id: int

class PedidoRead(PedidoBase):
    id: int
    criado_em: datetime

class PedidoCreate(SQLModel):
    usuario_id: int
    produto_id: int  
    quantidade: int  
    status: str = "Pendente"

# --- Pagamentos ---

class PagamentoBase(SQLModel):
    pedido_id: int = Field(foreign_key="pedidos.id")
    valor: Decimal = Field(max_digits=10, decimal_places=2)
    metodo: str = Field(max_length=50)
    status: str = Field(max_length=50)

class Pagamento(PagamentoBase, table=True):
    __tablename__ = "pagamentos"
    id: Optional[int] = Field(default=None, primary_key=True)
    pago_em: Optional[datetime] = None
    pedido: Pedido = Relationship(back_populates="pagamento")

# --- Avaliações ---

class AvaliacaoBase(SQLModel):
    usuario_id: int = Field(foreign_key="usuarios.id")
    produto_id: int = Field(foreign_key="produtos.id")
    nota: int
    comentario: Optional[str] = None

class Avaliacao(AvaliacaoBase, table=True):
    __tablename__ = "avaliacoes"
    id: Optional[int] = Field(default=None, primary_key=True)
    criado_em: datetime = Field(default_factory=datetime.now)
    produto: Produto = Relationship(back_populates="avaliacoes")