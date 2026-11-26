from typing import Callable
import flet as ft

from controllers.auth_controller import AuthController
from controllers.cart_controller import CartController
from controllers.order_controller import OrderController
from models.product_model import format_brl
from views.ui_helpers import show_confirm_dialog, show_feedback


def build_cart_view(
    page: ft.Page,
    auth_controller: AuthController,
    cart_controller: CartController,
    order_controller: OrderController,
    on_cart_changed: Callable[[], None],
    on_order_created: Callable[[], None],
    on_go_menu: Callable[[], None],
    on_auth_required: Callable[[], None],
) -> ft.Control:
    """Monta a tela do carrinho de compras e finalizacao do pedido."""
    if not auth_controller.is_authenticated():
        on_auth_required()
        return ft.Container()

    default_addr = (
        auth_controller.usuario_atual.endereco if auth_controller.usuario_atual else ""
    )

    items_column = ft.Column(spacing=10)
    total_text = ft.Text(format_brl(0.0), size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.DEEP_ORANGE_700)
    empty_state = ft.Container(visible=False)
    checkout_card = ft.Card(elevation=2, visible=True)

    endereco_field = ft.TextField(
        label="Endereço de entrega",
        hint_text="Rua, número, bairro e complemento",
        value=default_addr,
        prefix_icon=ft.Icons.LOCATION_ON,
    )
    obs_field = ft.TextField(
        label="Observações (opcional)",
        hint_text="Ex.: sem cebola, troco para R$ 100,00, tocar interfone",
        multiline=True,
        min_lines=2,
        max_lines=3,
        prefix_icon=ft.Icons.NOTES,
    )
    checkout_btn = ft.Button(
        content="Finalizar Pedido",
        icon=ft.Icons.CHECK_CIRCLE,
        bgcolor=ft.Colors.DEEP_ORANGE_600,
        color=ft.Colors.WHITE,
        height=46,
    )

    def _render_cart() -> None:
        if not auth_controller.is_authenticated():
            on_auth_required()
            return

        items = cart_controller.get_items()
        items_column.controls.clear()

        if not items:
            empty_state.visible = True
            checkout_card.visible = False
            empty_state.content = ft.Card(
                content=ft.Container(
                    padding=28,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=12,
                        controls=[
                            ft.Icon(ft.Icons.SHOPPING_CART_OUTLINED, size=52, color=ft.Colors.GREY_400),
                            ft.Text("Seu carrinho está vazio", size=18, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                "Adicione itens do cardápio para fazer seu pedido.",
                                color=ft.Colors.GREY_600,
                            ),
                            ft.Button(
                                content="Ver Cardápio",
                                icon=ft.Icons.RESTAURANT_MENU,
                                bgcolor=ft.Colors.DEEP_ORANGE_600,
                                color=ft.Colors.WHITE,
                                on_click=lambda e: on_go_menu(),
                            ),
                        ],
                    ),
                )
            )
            page.update()
            return

        empty_state.visible = False
        checkout_card.visible = True

        for item in items:
            prod = item.product

            def _make_qty_handler(pid: str, delta: int):
                def _handler(e) -> None:
                    if not auth_controller.is_authenticated():
                        on_auth_required()
                        return
                    current_items = {i.product.id: i for i in cart_controller.get_items()}
                    if pid not in current_items:
                        return
                    nova_qtd = current_items[pid].quantidade + delta
                    ok, msg = cart_controller.update_quantity(pid, nova_qtd)
                    if not ok:
                        show_feedback(page, msg, is_error=True)
                    on_cart_changed()
                    _render_cart()

                return _handler

            def _make_remove_handler(pid: str, nome: str):
                def _handler(e) -> None:
                    if not auth_controller.is_authenticated():
                        on_auth_required()
                        return

                    def _do_remove() -> None:
                        ok, msg = cart_controller.remove_item(pid)
                        show_feedback(page, msg, is_error=not ok)
                        on_cart_changed()
                        _render_cart()

                    show_confirm_dialog(
                        page,
                        "Remover item",
                        f"Deseja remover '{nome}' do carrinho?",
                        _do_remove,
                        confirm_label="Remover",
                    )

                return _handler

            row_card = ft.Card(
                elevation=1,
                content=ft.Container(
                    padding=14,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=ft.BorderRadius.all(10),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        wrap=True,
                        controls=[
                            ft.Column(
                                spacing=2,
                                expand=True,
                                controls=[
                                    ft.Text(prod.nome, size=15, weight=ft.FontWeight.BOLD),
                                    ft.Text(
                                        f"Unitário: {format_brl(prod.preco)}",
                                        size=12,
                                        color=ft.Colors.GREY_600,
                                    ),
                                ],
                            ),
                            ft.Row(
                                spacing=4,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.REMOVE_CIRCLE_OUTLINE,
                                        tooltip="Diminuir quantidade",
                                        on_click=_make_qty_handler(prod.id, -1),
                                    ),
                                    ft.Text(str(item.quantidade), size=15, weight=ft.FontWeight.BOLD),
                                    ft.IconButton(
                                        icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                                        tooltip="Aumentar quantidade",
                                        on_click=_make_qty_handler(prod.id, 1),
                                    ),
                                    ft.Container(width=10),
                                    ft.Text(
                                        format_brl(item.subtotal),
                                        size=15,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.DEEP_ORANGE_700,
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_OUTLINE,
                                        icon_color=ft.Colors.RED_600,
                                        tooltip="Remover item",
                                        on_click=_make_remove_handler(prod.id, prod.nome),
                                    ),
                                ],
                            ),
                        ],
                    ),
                ),
            )
            items_column.controls.append(row_card)

        total_text.value = format_brl(cart_controller.get_total())
        page.update()

    def _handle_clear_cart(e=None) -> None:
        if not auth_controller.is_authenticated():
            on_auth_required()
            return

        def _do_clear() -> None:
            cart_controller.clear()
            on_cart_changed()
            _render_cart()
            show_feedback(page, "Carrinho esvaziado.")

        show_confirm_dialog(
            page,
            "Limpar carrinho",
            "Deseja remover todos os itens do carrinho?",
            _do_clear,
            confirm_label="Limpar",
        )

    def _handle_checkout(e=None) -> None:
        if not auth_controller.is_authenticated():
            on_auth_required()
            return

        checkout_btn.disabled = True
        page.update()
        try:
            ok, msg = order_controller.create_order_from_cart(
                cart_controller=cart_controller,
                endereco_entrega=endereco_field.value or "",
                observacoes=obs_field.value or "",
            )
            show_feedback(page, msg, is_error=not ok)
            if ok:
                on_cart_changed()
                on_order_created()
                return
        finally:
            checkout_btn.disabled = False
            page.update()

    checkout_btn.on_click = _handle_checkout

    checkout_card.content = ft.Container(
        padding=18,
        bgcolor=ft.Colors.WHITE,
        border_radius=ft.BorderRadius.all(12),
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Text("Dados da Entrega", size=17, weight=ft.FontWeight.BOLD),
                endereco_field,
                obs_field,
                ft.Divider(height=10),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("Total do Pedido:", size=17, weight=ft.FontWeight.W_600),
                        total_text,
                    ],
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    wrap=True,
                    spacing=10,
                    controls=[
                        ft.OutlinedButton(
                            content="Limpar Carrinho",
                            icon=ft.Icons.DELETE_SWEEP,
                            on_click=_handle_clear_cart,
                        ),
                        checkout_btn,
                    ],
                ),
            ],
        ),
    )

    _render_cart()

    return ft.Column(
        spacing=16,
        controls=[
            ft.Text("Meu Carrinho", size=22, weight=ft.FontWeight.BOLD),
            empty_state,
            items_column,
            checkout_card,
        ],
    )
