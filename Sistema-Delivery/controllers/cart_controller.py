from controllers.auth_controller import AuthController
from models.order_model import CartItem, validate_quantity
from models.product_model import Product


class CartController:
    """Gerencia os itens do carrinho da sessao autenticada."""

    def __init__(self, auth_controller: AuthController) -> None:
        self._auth = auth_controller
        self._items: dict[str, CartItem] = {}

    def _guard_session(self) -> bool:
        if not self._auth.is_authenticated():
            self._items.clear()
            return False
        return True

    def add_item(self, product: Product, quantidade: int = 1) -> tuple[bool, str]:
        """Adiciona um produto ao carrinho validando sessao, disponibilidade e quantidade."""
        if not self._guard_session():
            return False, "Faça login para adicionar itens ao carrinho."

        if not product.disponivel:
            return False, "Este produto está indisponível no momento."

        ok, msg, qty = validate_quantity(quantidade)
        if not ok or qty is None:
            return False, msg

        if product.id in self._items:
            nova_qtd = self._items[product.id].quantidade + qty
            if nova_qtd > 100:
                return False, "Quantidade máxima por item no carrinho é 100."
            self._items[product.id].quantidade = nova_qtd
            self._items[product.id].product = product
        else:
            self._items[product.id] = CartItem(product=product, quantidade=qty)

        return True, f"'{product.nome}' adicionado ao carrinho!"

    def update_quantity(self, product_id: str, new_qty: int) -> tuple[bool, str]:
        """Atualiza a quantidade de um item no carrinho (remove se <= 0)."""
        if not self._guard_session():
            return False, "Faça login para alterar o carrinho."

        if product_id not in self._items:
            return False, "Item não encontrado no carrinho."

        if new_qty <= 0:
            del self._items[product_id]
            return True, "Item removido do carrinho."

        ok, msg, qty = validate_quantity(new_qty)
        if not ok or qty is None:
            return False, msg

        self._items[product_id].quantidade = qty
        return True, "Quantidade atualizada."

    def remove_item(self, product_id: str) -> tuple[bool, str]:
        """Remove um item especifico do carrinho."""
        if not self._guard_session():
            return False, "Faça login para alterar o carrinho."

        if product_id in self._items:
            del self._items[product_id]
            return True, "Item removido do carrinho."
        return False, "Item não encontrado no carrinho."

    def clear(self) -> None:
        """Limpa todos os itens do carrinho."""
        self._items.clear()

    def get_items(self) -> list[CartItem]:
        """Retorna os itens atuais do carrinho."""
        if not self._guard_session():
            return []
        return list(self._items.values())

    def get_total(self) -> float:
        """Calcula o valor total do carrinho."""
        if not self._guard_session():
            return 0.0
        return round(sum(item.subtotal for item in self._items.values()), 2)

    def get_total_count(self) -> int:
        """Retorna a soma das quantidades no carrinho."""
        if not self._guard_session():
            return 0
        return sum(item.quantidade for item in self._items.values())
