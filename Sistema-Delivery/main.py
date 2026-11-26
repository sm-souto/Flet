import os
import flet as ft

from controllers.auth_controller import AuthController
from controllers.cart_controller import CartController
from controllers.order_controller import OrderController
from services.realtime_service import RealtimeOrderWatcher
from views.admin_view import build_admin_view
from views.cart_view import build_cart_view
from views.home_view import build_home_view
from views.login_view import build_login_view
from views.tracking_view import build_tracking_view
from views.ui_helpers import show_feedback


def main(page: ft.Page) -> None:
    """Ponto de entrada da aplicacao Flet em arquitetura MVC."""
    page.title = "SaborExpress Delivery"
    page.bgcolor = ft.Colors.GREY_100
    page.padding = 0
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.DEEP_ORANGE,
        use_material3=True,
    )

    try:
        auth_controller = AuthController()
    except ValueError:
        page.add(
            ft.Container(
                expand=True,
                alignment=ft.Alignment.CENTER,
                padding=24,
                content=ft.Text(
                    "Configuração do servidor incompleta. Verifique as variáveis de ambiente.",
                    color=ft.Colors.RED_700,
                    size=16,
                    weight=ft.FontWeight.BOLD,
                ),
            )
        )
        return

    cart_controller = CartController(auth_controller)
    order_controller = OrderController(auth_controller)
    realtime_watcher = RealtimeOrderWatcher(interval_seconds=12)

    current_tab = 0
    body_container = ft.Container(
        expand=True,
        padding=ft.Padding.symmetric(horizontal=20, vertical=16),
    )

    cart_badge_text = ft.Text("0", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
    user_label = ft.Text("", size=13, color=ft.Colors.WHITE)

    def _update_header_state() -> None:
        if auth_controller.is_authenticated() and auth_controller.usuario_atual:
            user_label.value = f"Olá, {auth_controller.usuario_atual.nome}"
        else:
            user_label.value = ""
        cart_badge_text.value = str(cart_controller.get_total_count())
        page.update()

    def _handle_logout(e=None) -> None:
        realtime_watcher.stop()
        cart_controller.clear()
        auth_controller.logout()
        abrir_tela_login()
        show_feedback(page, "Você saiu da sua conta com segurança.")

    def abrir_tela_login() -> None:
        """Exibe a tela inicial de Login/Cadastro limpando qualquer controle interno."""
        realtime_watcher.stop()
        page.appbar = None
        page.navigation_bar = None
        page.controls.clear()
        page.scroll = ft.ScrollMode.AUTO
        page.add(
            build_login_view(
                page=page,
                auth_controller=auth_controller,
                on_login_success=lambda: abrir_tela_principal(0),
            )
        )
        page.update()

    def _render_tab(index: int) -> None:
        nonlocal current_tab
        if not auth_controller.is_authenticated():
            abrir_tela_login()
            return

        current_tab = index
        if page.navigation_bar is not None:
            page.navigation_bar.selected_index = index

        realtime_watcher.stop()

        if index == 0:
            body_container.content = build_home_view(
                page=page,
                auth_controller=auth_controller,
                cart_controller=cart_controller,
                order_controller=order_controller,
                on_cart_changed=_update_header_state,
                on_go_admin=lambda: _render_tab(3),
                on_auth_required=abrir_tela_login,
            )
        elif index == 1:
            body_container.content = build_cart_view(
                page=page,
                auth_controller=auth_controller,
                cart_controller=cart_controller,
                order_controller=order_controller,
                on_cart_changed=_update_header_state,
                on_order_created=lambda: _render_tab(2),
                on_go_menu=lambda: _render_tab(0),
                on_auth_required=abrir_tela_login,
            )
        elif index == 2:
            tracking_view, refresh_cb = build_tracking_view(
                page=page,
                auth_controller=auth_controller,
                order_controller=order_controller,
                on_auth_required=abrir_tela_login,
            )
            body_container.content = tracking_view
            realtime_watcher.start(
                on_tick=refresh_cb,
                is_active=lambda: auth_controller.is_authenticated() and current_tab == 2,
            )
        else:
            body_container.content = build_admin_view(
                page=page,
                auth_controller=auth_controller,
                order_controller=order_controller,
                on_auth_required=abrir_tela_login,
                on_profile_updated=_update_header_state,
            )

        _update_header_state()

    def abrir_tela_principal(tab_index: int = 0) -> None:
        """Verifica sessao autenticada antes de montar a navegacao principal."""
        if not auth_controller.is_authenticated():
            abrir_tela_login()
            return

        page.controls.clear()
        page.scroll = ft.ScrollMode.AUTO

        page.appbar = ft.AppBar(
            title=ft.Row(
                spacing=8,
                controls=[
                    ft.Icon(ft.Icons.DELIVERY_DINING, color=ft.Colors.WHITE),
                    ft.Text("SaborExpress", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                ],
            ),
            bgcolor=ft.Colors.DEEP_ORANGE_600,
            actions=[
                ft.Container(
                    padding=ft.Padding.only(right=8),
                    alignment=ft.Alignment.CENTER,
                    content=user_label,
                ),
                ft.Container(
                    padding=ft.Padding.symmetric(horizontal=10, vertical=4),
                    margin=ft.Margin.only(right=6),
                    bgcolor=ft.Colors.DEEP_ORANGE_800,
                    border_radius=ft.BorderRadius.all(14),
                    on_click=lambda e: _render_tab(1),
                    content=ft.Row(
                        spacing=4,
                        controls=[
                            ft.Icon(ft.Icons.SHOPPING_CART, size=16, color=ft.Colors.WHITE),
                            cart_badge_text,
                        ],
                    ),
                ),
                ft.IconButton(
                    icon=ft.Icons.LOGOUT,
                    icon_color=ft.Colors.WHITE,
                    tooltip="Sair",
                    on_click=_handle_logout,
                ),
            ],
        )

        page.navigation_bar = ft.NavigationBar(
            selected_index=tab_index,
            on_change=lambda e: _render_tab(e.control.selected_index),
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.Icons.RESTAURANT_MENU,
                    label="Cardápio",
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.SHOPPING_CART,
                    label="Carrinho",
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.LOCAL_SHIPPING,
                    label="Pedidos",
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.ADMIN_PANEL_SETTINGS,
                    label="Gerenciar",
                ),
            ],
        )

        page.add(
            ft.Container(
                alignment=ft.Alignment.TOP_CENTER,
                content=ft.Container(
                    width=1100,
                    content=body_container,
                ),
            )
        )
        _render_tab(tab_index)

    abrir_tela_login()


if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 8080))
    ft.run(main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=porta)