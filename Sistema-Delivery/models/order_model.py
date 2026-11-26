from dataclasses import dataclass, field
from models.product_model import Product

ORDER_STATUSES: tuple[str, ...] = (
    "Recebido",
    "Em preparo",
    "Saiu para entrega",
    "Entregue",
    "Cancelado",
)


@dataclass
class CartItem:
    """Item mantido no carrinho da sessao atual."""

    product: Product
    quantidade: int = 1

    @property
    def subtotal(self) -> float:
        return round(self.product.preco * self.quantidade, 2)


@dataclass
class OrderItem:
    """Item persistido na tabela public.itens_pedido."""

    id: str
    pedido_id: str
    produto_id: str
    nome_produto: str
    quantidade: int
    preco_unitario: float

    @property
    def subtotal(self) -> float:
        return round(self.preco_unitario * self.quantidade, 2)

    @classmethod
    def from_dict(cls, data: dict) -> "OrderItem":
        return cls(
            id=str(data.get("id", "")),
            pedido_id=str(data.get("pedido_id", "")),
            produto_id=str(data.get("produto_id", "")),
            nome_produto=str(data.get("nome_produto", "")),
            quantidade=int(data.get("quantidade", 1)),
            preco_unitario=float(data.get("preco_unitario", 0.0)),
        )


@dataclass
class Order:
    """Representa um pedido na tabela public.pedidos."""

    id: str
    user_id: str
    perfil_id: str | None
    endereco_entrega: str
    observacoes: str
    status: str
    total: float
    criado_em: str = ""
    itens: list[OrderItem] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict, itens: list[OrderItem] | None = None) -> "Order":
        return cls(
            id=str(data.get("id", "")),
            user_id=str(data.get("user_id", "")),
            perfil_id=str(data["perfil_id"]) if data.get("perfil_id") else None,
            endereco_entrega=str(data.get("endereco_entrega", "")),
            observacoes=str(data.get("observacoes", "") or ""),
            status=str(data.get("status", "Recebido")),
            total=float(data.get("total", 0.0)),
            criado_em=str(data.get("criado_em", "") or ""),
            itens=itens or [],
        )


def validate_quantity(qty_value: object) -> tuple[bool, str, int | None]:
    """Valida quantidade inteira entre 1 e 100."""
    try:
        qty = int(str(qty_value).strip())
    except (ValueError, TypeError):
        return False, "A quantidade precisa ser um número inteiro.", None

    if qty <= 0 or qty > 100:
        return False, "A quantidade deve estar entre 1 e 100.", None

    return True, "", qty


def validate_order_data(endereco_entrega: str, observacoes: str) -> tuple[bool, str]:
    """Valida endereco e observacoes antes de finalizar um pedido."""
    endereco_limpo = (endereco_entrega or "").strip()
    obs_limpa = (observacoes or "").strip()

    if len(endereco_limpo) < 5 or len(endereco_limpo) > 200:
        return False, "O endereço de entrega deve ter entre 5 e 200 caracteres."
    if len(obs_limpa) > 300:
        return False, "As observações devem ter no máximo 300 caracteres."
    return True, ""


def validate_order_status(status: str) -> tuple[bool, str]:
    """Garante que o status pertence a lista permitida do sistema."""
    status_limpo = (status or "").strip()
    if status_limpo not in ORDER_STATUSES:
        return False, "Status de pedido inválido."
    return True, ""
