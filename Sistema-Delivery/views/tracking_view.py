from typing import Callable
import flet as ft

from controllers.auth_controller import AuthController
from controllers.order_controller import OrderController
from models.product_model import format_brl
from views.ui_helpers import format_timestamp, show_confirm_dialog, show_feedback, status_badge


def build_tracking_view(
    page: ft.Page,
    auth_controller: AuthController,
    order_controller: OrderController,
    on_auth_required: Callable[[], None],
) -> tuple[ft.Control, Callable[[], None]]:
    """Monta a tela de acompanhamento de pedidos e retorna (view, refresh_callback)."""
    if not auth_controller.is_authenticated():
        on_auth_required()
        return ft.Container(), lambda: None

    orders_column = ft.Column(spacing=12)

    def _load_orders() -> None:
        if not auth_controller.is_authenticated():
            on_auth_required()
            return

        ok, msg, orders = order_controller.list_orders()
        orders_column.controls.clear()

        if not ok:
            show_feedback(page, msg, is_error=True)

        if not orders:
            orders_column.controls.append(
                ft.Card(
                    content=ft.Container(
                        padding=28,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10,
                            controls=[
                                ft.Icon(ft.Icons.LOCAL_SHIPPING_OUTLINED, size=50, color=ft.Colors.GREY_400),
                                ft.Text("Você ainda não realizou nenhum pedido.", size=17, weight=ft.FontWeight.BOLD),
                                ft.Text(
                                    "Escolha itens no cardápio e finalize no carrinho para acompanhar aqui.",
                                    color=ft.Colors.GREY_600,
                                ),
                            ],
                        ),
                    )
                )
            )
            page.update()
            return

        for order in orders:
            item_rows = [
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(f"{it.quantidade}x {it.nome_produto}", size=13),
                        ft.Text(format_brl(it.subtotal), size=13, weight=ft.FontWeight.W_500),
                    ],
                )
                for it in order.itens
            ]

            def _make_cancel_handler(oid: str):
                def _handler(e) -> None:
                    if not auth_controller.is_authenticated():
                        on_auth_required()
                        return

                    def _do_cancel() -> None:
                        ok_upd, msg_upd = order_controller.update_order_status(oid, "Cancelado")
                        show_feedback(page, msg_upd, is_error=not ok_upd)
                        _load_orders()

                    show_confirm_dialog(
                        page,
                        "Cancelar pedido",
                        "Tem certeza que deseja cancelar este pedido?",
                        _do_cancel,
                        confirm_label="Cancelar Pedido",
                    )

                return _handler

            def _make_delete_handler(oid: str):
                def _handler(e) -> None:
                    if not auth_controller.is_authenticated():
                        on_auth_required()
                        return

                    def _do_delete() -> None:
                        ok_del, msg_del = order_controller.delete_order(oid)
                        show_feedback(page, msg_del, is_error=not ok_del)
                        _load_orders()

                    show_confirm_dialog(
                        page,
                        "Excluir registro do pedido",
                        "Deseja excluir permanentemente este pedido do seu histórico?",
                        _do_delete,
                        confirm_label="Excluir",
                    )

                return _handler

            action_buttons: list[ft.Control] = []
            if order.status in ("Recebido", "Em preparo"):
                action_buttons.append(
                    ft.OutlinedButton(
                        content="Cancelar Pedido",
                        icon=ft.Icons.CANCEL_OUTLINED,
                        on_click=_make_cancel_handler(order.id),
                    )
                )
            action_buttons.append(
                ft.TextButton(
                    content="Excluir",
                    icon=ft.Icons.DELETE_OUTLINE,
                    on_click=_make_delete_handler(order.id),
                )
            )

            short_id = order.id[:8].upper()
            card = ft.Card(
                elevation=2,
                content=ft.Container(
                    padding=16,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=ft.BorderRadius.all(12),
                    content=ft.Column(
                        spacing=8,
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                wrap=True,
                                controls=[
                                    ft.Column(
                                        spacing=2,
                                        controls=[
                                            ft.Text(f"Pedido #{short_id}", size=16, weight=ft.FontWeight.BOLD),
                                            ft.Text(
                                                format_timestamp(order.criado_em),
                                                size=12,
                                                color=ft.Colors.GREY_600,
                                            ),
                                        ],
                                    ),
                                    status_badge(order.status),
                                ],
                            ),
                            ft.Text(
                                f"Entrega: {order.endereco_entrega}",
                                size=13,
                                color=ft.Colors.GREY_800,
                            ),
                            ft.Text(
                                f"Observações: {order.observacoes}",
                                size=12,
                                color=ft.Colors.GREY_600,
                                visible=bool(order.observacoes),
                            ),
                            ft.Divider(height=8),
                            ft.Column(spacing=4, controls=item_rows),
                            ft.Divider(height=8),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                wrap=True,
                                controls=[
                                    ft.Text(
                                        f"Total: {format_brl(order.total)}",
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.DEEP_ORANGE_700,
                                    ),
                                    ft.Row(spacing=8, controls=action_buttons),
                                ],
                            ),
                        ],
                    ),
                ),
            )
            orders_column.controls.append(card)

        page.update()

    _load_orders()

    view = ft.Column(
        spacing=16,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                wrap=True,
                controls=[
                    ft.Column(
                        spacing=2,
                        controls=[
                            ft.Text("Meus Pedidos", size=22, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                "Acompanhe o andamento das suas entregas em tempo real.",
                                size=13,
                                color=ft.Colors.GREY_600,
                            ),
                        ],
                    ),
                    ft.OutlinedButton(
                        content="Atualizar",
                        icon=ft.Icons.REFRESH,
                        on_click=lambda e: _load_orders(),
                    ),
                ],
            ),
            orders_column,
        ],
    )
    return view, _load_orders
