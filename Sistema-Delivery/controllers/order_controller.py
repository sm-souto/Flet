from controllers.auth_controller import AuthController
from controllers.cart_controller import CartController
from models.order_model import (
    Order,
    OrderItem,
    validate_order_data,
    validate_order_status,
)
from models.product_model import (
    Category,
    Product,
    validate_category_data,
    validate_product_data,
)


class OrderController:
    """Controller principal de Delivery: CRUD de categorias, produtos e pedidos."""

    def __init__(self, auth_controller: AuthController) -> None:
        self._auth = auth_controller

    def list_categories(self) -> tuple[bool, str, list[Category]]:
        """Lista todas as categorias do usuario autenticado."""
        if not self._auth.is_authenticated():
            return False, "Faça login para continuar.", []

        try:
            user_id = self._auth.require_auth()
            res = (
                self._auth.client.table("categorias")
                .select("*")
                .eq("user_id", user_id)
                .order("nome")
                .execute()
            )
            categories = [Category.from_dict(row) for row in (res.data or [])]
            return True, "", categories
        except Exception:
            return False, "Não foi possível carregar as categorias no momento.", []

    def create_category(self, nome: str, descricao: str = "") -> tuple[bool, str]:
        """Cria uma nova categoria vinculada ao usuario autenticado."""
        if not self._auth.is_authenticated():
            return False, "Faça login para continuar."

        ok, msg = validate_category_data(nome, descricao)
        if not ok:
            return False, msg

        try:
            user_id = self._auth.require_auth()
            payload = {
                "user_id": user_id,
                "nome": nome.strip(),
                "descricao": (descricao or "").strip(),
            }
            self._auth.client.table("categorias").insert(payload).execute()
            return True, "Categoria cadastrada com sucesso!"
        except Exception:
            return False, "Não foi possível salvar a categoria no momento. Tente novamente."

    def update_category(self, category_id: str, nome: str, descricao: str = "") -> tuple[bool, str]:
        """Edita uma categoria existente do usuario autenticado."""
        if not self._auth.is_authenticated():
            return False, "Faça login para continuar."

        if not (category_id or "").strip():
            return False, "Categoria inválida."

        ok, msg = validate_category_data(nome, descricao)
        if not ok:
            return False, msg

        try:
            user_id = self._auth.require_auth()
            payload = {
                "nome": nome.strip(),
                "descricao": (descricao or "").strip(),
            }
            self._auth.client.table("categorias").update(payload).eq("id", category_id).eq(
                "user_id", user_id
            ).execute()
            return True, "Categoria atualizada com sucesso!"
        except Exception:
            return False, "Não foi possível atualizar a categoria no momento."

    def delete_category(self, category_id: str) -> tuple[bool, str]:
        """Exclui uma categoria do usuario autenticado."""
        if not self._auth.is_authenticated():
            return False, "Faça login para continuar."

        if not (category_id or "").strip():
            return False, "Categoria inválida."

        try:
            user_id = self._auth.require_auth()
            self._auth.client.table("categorias").delete().eq("id", category_id).eq(
                "user_id", user_id
            ).execute()
            return True, "Categoria excluída com sucesso!"
        except Exception as exc:
            if "23503" in str(exc) or "foreign key" in str(exc).lower():
                return (
                    False,
                    "Não é possível excluir esta categoria pois existem produtos vinculados a ela.",
                )
            return False, "Não foi possível excluir a categoria no momento."

    def list_products(self, only_available: bool = False) -> tuple[bool, str, list[Product]]:
        """Lista os produtos do usuario autenticado com o nome da categoria."""
        if not self._auth.is_authenticated():
            return False, "Faça login para continuar.", []

        try:
            user_id = self._auth.require_auth()
            ok_cat, _, categories = self.list_categories()
            cat_map = {c.id: c.nome for c in categories} if ok_cat else {}

            query = (
                self._auth.client.table("produtos")
                .select("*")
                .eq("user_id", user_id)
                .order("nome")
            )
            if only_available:
                query = query.eq("disponivel", True)

            res = query.execute()
            products = [Product.from_dict(row, cat_map) for row in (res.data or [])]
            return True, "", products
        except Exception:
            return False, "Não foi possível carregar o cardápio no momento.", []

    def create_product(
        self,
        nome: str,
        descricao: str,
        preco_texto: str,
        categoria_id: str,
        disponivel: bool = True,
    ) -> tuple[bool, str]:
        """Cadastra um novo produto vinculado a uma categoria e ao usuario."""
        if not self._auth.is_authenticated():
            return False, "Faça login para continuar."

        ok, msg, preco = validate_product_data(nome, descricao, preco_texto, categoria_id)
        if not ok or preco is None:
            return False, msg

        try:
            user_id = self._auth.require_auth()
            payload = {
                "user_id": user_id,
                "categoria_id": categoria_id.strip(),
                "nome": nome.strip(),
                "descricao": (descricao or "").strip(),
                "preco": preco,
                "disponivel": bool(disponivel),
            }
            self._auth.client.table("produtos").insert(payload).execute()
            return True, "Produto cadastrado com sucesso!"
        except Exception:
            return False, "Não foi possível salvar o produto no momento. Tente novamente."

    def update_product(
        self,
        product_id: str,
        nome: str,
        descricao: str,
        preco_texto: str,
        categoria_id: str,
        disponivel: bool,
    ) -> tuple[bool, str]:
        """Atualiza um produto existente do usuario autenticado."""
        if not self._auth.is_authenticated():
            return False, "Faça login para continuar."

        if not (product_id or "").strip():
            return False, "Produto inválido."

        ok, msg, preco = validate_product_data(nome, descricao, preco_texto, categoria_id)
        if not ok or preco is None:
            return False, msg

        try:
            user_id = self._auth.require_auth()
            payload = {
                "categoria_id": categoria_id.strip(),
                "nome": nome.strip(),
                "descricao": (descricao or "").strip(),
                "preco": preco,
                "disponivel": bool(disponivel),
            }
            self._auth.client.table("produtos").update(payload).eq("id", product_id).eq(
                "user_id", user_id
            ).execute()
            return True, "Produto atualizado com sucesso!"
        except Exception:
            return False, "Não foi possível atualizar o produto no momento."

    def delete_product(self, product_id: str) -> tuple[bool, str]:
        """Exclui um produto do usuario autenticado."""
        if not self._auth.is_authenticated():
            return False, "Faça login para continuar."

        if not (product_id or "").strip():
            return False, "Produto inválido."

        try:
            user_id = self._auth.require_auth()
            self._auth.client.table("produtos").delete().eq("id", product_id).eq(
                "user_id", user_id
            ).execute()
            return True, "Produto excluído com sucesso!"
        except Exception as exc:
            if "23503" in str(exc) or "foreign key" in str(exc).lower():
                return (
                    False,
                    "Este produto já faz parte de pedidos anteriores. Marque-o como indisponível em vez de excluir.",
                )
            return False, "Não foi possível excluir o produto no momento."

    def seed_sample_menu(self) -> tuple[bool, str]:
        """Popula categorias e produtos iniciais para o usuario testar rapidamente."""
        if not self._auth.is_authenticated():
            return False, "Faça login para continuar."

        try:
            user_id = self._auth.require_auth()
            existing_cats = (
                self._auth.client.table("categorias")
                .select("id")
                .eq("user_id", user_id)
                .limit(1)
                .execute()
            )
            if existing_cats.data:
                return False, "Você já possui categorias cadastradas no seu cardápio."

            sample_categories = [
                {"user_id": user_id, "nome": "Lanches Artesanais", "descricao": "Hambúrgueres e combos na brasa"},
                {"user_id": user_id, "nome": "Pizzas", "descricao": "Massa artesanal assada no forno"},
                {"user_id": user_id, "nome": "Bebidas", "descricao": "Refrigerantes, sucos e águas"},
            ]
            cat_res = self._auth.client.table("categorias").insert(sample_categories).execute()
            cats = {row["nome"]: row["id"] for row in (cat_res.data or [])}

            sample_products = [
                {
                    "user_id": user_id,
                    "categoria_id": cats["Lanches Artesanais"],
                    "nome": "Burger Clássico Cheddar",
                    "descricao": "Pão brioche, blend 160g, cheddar cremoso e bacon crocante.",
                    "preco": 32.90,
                    "disponivel": True,
                },
                {
                    "user_id": user_id,
                    "categoria_id": cats["Lanches Artesanais"],
                    "nome": "Combo Duplo Smash",
                    "descricao": "Dois hambúrgueres smash 100g, queijo prato e batata rústica.",
                    "preco": 44.50,
                    "disponivel": True,
                },
                {
                    "user_id": user_id,
                    "categoria_id": cats["Pizzas"],
                    "nome": "Pizza Calabresa Especial",
                    "descricao": "Molho de tomate italiano, muçarela, calabresa fatiada e cebola roxa.",
                    "preco": 54.00,
                    "disponivel": True,
                },
                {
                    "user_id": user_id,
                    "categoria_id": cats["Pizzas"],
                    "nome": "Pizza Margherita",
                    "descricao": "Muçarela de búfala, tomate cereja e manjericão fresco.",
                    "preco": 49.90,
                    "disponivel": True,
                },
                {
                    "user_id": user_id,
                    "categoria_id": cats["Bebidas"],
                    "nome": "Refrigerante Lata 350ml",
                    "descricao": "Gelado, escolha o sabor nas observações.",
                    "preco": 7.50,
                    "disponivel": True,
                },
                {
                    "user_id": user_id,
                    "categoria_id": cats["Bebidas"],
                    "nome": "Suco Natural de Laranja 500ml",
                    "descricao": "Espremido na hora, sem adição de açúcar.",
                    "preco": 12.00,
                    "disponivel": True,
                },
            ]
            self._auth.client.table("produtos").insert(sample_products).execute()
            return True, "Cardápio de exemplo carregado com sucesso!"
        except Exception:
            return False, "Não foi possível carregar o cardápio de exemplo no momento."

    def create_order_from_cart(
        self,
        cart_controller: CartController,
        endereco_entrega: str,
        observacoes: str = "",
    ) -> tuple[bool, str]:
        """Cria um pedido e seus itens a partir do carrinho, validando precos no banco."""
        if not self._auth.is_authenticated():
            return False, "Faça login para finalizar seu pedido."

        cart_items = cart_controller.get_items()
        if not cart_items:
            return False, "Seu carrinho está vazio."

        ok, msg = validate_order_data(endereco_entrega, observacoes)
        if not ok:
            return False, msg

        try:
            user_id = self._auth.require_auth()
            ok_prod, err_prod, produtos_atuais = self.list_products(only_available=False)
            if not ok_prod:
                return False, err_prod

            produto_map = {p.id: p for p in produtos_atuais}
            verified_items: list[dict] = []
            total = 0.0

            for item in cart_items:
                db_prod = produto_map.get(item.product.id)
                if db_prod is None or not db_prod.disponivel:
                    return (
                        False,
                        f"O produto '{item.product.nome}' não está mais disponível.",
                    )
                if item.quantidade <= 0 or item.quantidade > 100:
                    return False, "Quantidade inválida no carrinho."
                subtotal = round(db_prod.preco * item.quantidade, 2)
                total = round(total + subtotal, 2)
                verified_items.append(
                    {
                        "user_id": user_id,
                        "produto_id": db_prod.id,
                        "nome_produto": db_prod.nome,
                        "quantidade": item.quantidade,
                        "preco_unitario": db_prod.preco,
                    }
                )

            if total <= 0:
                return False, "Não foi possível calcular o total do pedido."

            perfil_id = (
                self._auth.usuario_atual.id
                if self._auth.usuario_atual and self._auth.usuario_atual.id
                else None
            )
            order_payload = {
                "user_id": user_id,
                "perfil_id": perfil_id,
                "endereco_entrega": endereco_entrega.strip(),
                "observacoes": (observacoes or "").strip(),
                "status": "Recebido",
                "total": total,
            }
            order_res = self._auth.client.table("pedidos").insert(order_payload).execute()
            order_rows = order_res.data or []
            if not order_rows:
                return False, "Não foi possível registrar o pedido no momento."

            pedido_id = str(order_rows[0]["id"])
            for row in verified_items:
                row["pedido_id"] = pedido_id

            try:
                self._auth.client.table("itens_pedido").insert(verified_items).execute()
            except Exception:
                try:
                    self._auth.client.table("pedidos").delete().eq("id", pedido_id).eq(
                        "user_id", user_id
                    ).execute()
                except Exception:
                    pass
                return False, "Não foi possível salvar os itens do pedido. Tente novamente."

            cart_controller.clear()
            return True, "Pedido realizado com sucesso!"
        except Exception:
            return False, "Não foi possível finalizar o pedido no momento. Tente novamente."

    def list_orders(self) -> tuple[bool, str, list[Order]]:
        """Lista todos os pedidos do usuario autenticado com seus respectivos itens."""
        if not self._auth.is_authenticated():
            return False, "Faça login para visualizar seus pedidos.", []

        try:
            user_id = self._auth.require_auth()
            orders_res = (
                self._auth.client.table("pedidos")
                .select("*")
                .eq("user_id", user_id)
                .order("criado_em", desc=True)
                .execute()
            )
            orders_data = orders_res.data or []
            if not orders_data:
                return True, "", []

            items_res = (
                self._auth.client.table("itens_pedido")
                .select("*")
                .eq("user_id", user_id)
                .execute()
            )
            items_by_order: dict[str, list[OrderItem]] = {}
            for row in items_res.data or []:
                item = OrderItem.from_dict(row)
                items_by_order.setdefault(item.pedido_id, []).append(item)

            orders = [
                Order.from_dict(row, itens=items_by_order.get(str(row.get("id", "")), []))
                for row in orders_data
            ]
            return True, "", orders
        except Exception:
            return False, "Não foi possível carregar seus pedidos no momento.", []

    def update_order_status(self, order_id: str, new_status: str) -> tuple[bool, str]:
        """Atualiza o status de um pedido do usuario autenticado."""
        if not self._auth.is_authenticated():
            return False, "Faça login para continuar."

        if not (order_id or "").strip():
            return False, "Pedido inválido."

        ok, msg = validate_order_status(new_status)
        if not ok:
            return False, msg

        try:
            user_id = self._auth.require_auth()
            self._auth.client.table("pedidos").update({"status": new_status.strip()}).eq(
                "id", order_id
            ).eq("user_id", user_id).execute()
            return True, f"Status atualizado para '{new_status.strip()}'."
        except Exception:
            return False, "Não foi possível atualizar o status do pedido no momento."

    def delete_order(self, order_id: str) -> tuple[bool, str]:
        """Exclui um pedido do usuario autenticado (itens removidos em cascata)."""
        if not self._auth.is_authenticated():
            return False, "Faça login para continuar."

        if not (order_id or "").strip():
            return False, "Pedido inválido."

        try:
            user_id = self._auth.require_auth()
            self._auth.client.table("pedidos").delete().eq("id", order_id).eq(
                "user_id", user_id
            ).execute()
            return True, "Pedido excluído com sucesso!"
        except Exception:
            return False, "Não foi possível excluir o pedido no momento."
