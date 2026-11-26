from typing import Callable
import flet as ft

from controllers.auth_controller import AuthController
from controllers.cart_controller import CartController
from controllers.order_controller import OrderController
from models.product_model import format_brl
from views.ui_helpers import show_feedback


def build_home_view(
    page: ft.Page,
    auth_controller: AuthController,
    cart_controller: CartController,
    order_controller: OrderController,
    on_cart_changed: Callable[[], None],
    on_go_admin: Callable[[], None],
    on_auth_required: Callable[[], None],
) -> ft.Control:
    """Monta a tela principal do cardapio para busca e adicao ao carrinho."""
    if not auth_controller.is_authenticated():
        on_auth_required()
        return ft.Container()

    selected_category_id = "ALL"
    search_query = ""

    search_field = ft.TextField(
        label="Buscar no cardápio",
        hint_text="Ex.: burger, pizza, suco...",
        prefix_icon=ft.Icons.SEARCH,
        expand=True,
    )
    category_dropdown = ft.Dropdown(
        label="Categoria",
        width=230,
        value="ALL",
        options=[ft.dropdown.Option(key="ALL", text="Todas as categorias")],
    )
    products_grid = ft.ResponsiveRow(spacing=12, run_spacing=12)
    status_container = ft.Container(visible=False)

    def _load_data() -> None:
        if not auth_controller.is_authenticated():
            on_auth_required()
            return

        ok_cat, msg_cat, categories = order_controller.list_categories()
        ok_prod, msg_prod, products = order_controller.list_products(only_available=False)

        if not ok_cat or not ok_prod:
            show_feedback(page, msg_prod or msg_cat or "Erro ao carregar cardápio.", is_error=True)

        opts = [ft.dropdown.Option(key="ALL", text="Todas as categorias")]
        for cat in categories:
            opts.append(ft.dropdown.Option(key=cat.id, text=cat.nome))
        category_dropdown.options = opts
        if selected_category_id not in {o.key for o in opts}:
            category_dropdown.value = "ALL"

        filtered = []
        term = search_query.strip().lower()
        for prod in products:
            if selected_category_id != "ALL" and prod.categoria_id != selected_category_id:
                continue
            if term and term not in prod.nome.lower() and term not in prod.descricao.lower():
                continue
            filtered.append(prod)

        products_grid.controls.clear()

        if not products:
            status_container.visible = True
            status_container.content = ft.Card(
                content=ft.Container(
                    padding=24,
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=12,
                        controls=[
                            ft.Icon(ft.Icons.RESTAURANT_MENU, size=48, color=ft.Colors.DEEP_ORANGE_500),
                            ft.Text(
                                "Seu cardápio ainda está vazio!",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                "Você pode carregar um cardápio de exemplo agora ou cadastrar categorias e produtos manualmente em Gerenciar.",
                                text_align=ft.TextAlign.CENTER,
                                color=ft.Colors.GREY_700,
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                wrap=True,
                                spacing=10,
                                controls=[
                                    ft.Button(
                                        content="Carregar Cardápio de Exemplo",
                                        icon=ft.Icons.AUTO_AWESOME,
                                        bgcolor=ft.Colors.DEEP_ORANGE_600,
                                        color=ft.Colors.WHITE,
                                        on_click=_handle_seed,
                                    ),
                                    ft.OutlinedButton(
                                        content="Gerenciar Cardápio",
                                        icon=ft.Icons.ADMIN_PANEL_SETTINGS,
                                        on_click=lambda e: on_go_admin(),
                                    ),
                                ],
                            ),
                        ],
                    ),
                )
            )
        elif not filtered:
            status_container.visible = True
            status_container.content = ft.Container(
                padding=24,
                alignment=ft.Alignment.CENTER,
                content=ft.Text(
                    "Nenhum produto encontrado para este filtro.",
                    color=ft.Colors.GREY_600,
                    size=15,
                ),
            )
        else:
            status_container.visible = False
            for prod in filtered:
                availability_badge = ft.Container(
                    content=ft.Text(
                        "Disponível" if prod.disponivel else "Indisponível",
                        size=11,
                        weight=ft.FontWeight.W_600,
                        color=ft.Colors.GREEN_800 if prod.disponivel else ft.Colors.RED_800,
                    ),
                    bgcolor=ft.Colors.GREEN_50 if prod.disponivel else ft.Colors.RED_50,
                    padding=ft.Padding.symmetric(horizontal=8, vertical=3),
                    border_radius=ft.BorderRadius.all(10),
                )

                def _make_add_handler(item_prod):
                    def _on_add(e) -> None:
                        if not auth_controller.is_authenticated():
                            on_auth_required()
                            return
                        ok, msg = cart_controller.add_item(item_prod, 1)
                        show_feedback(page, msg, is_error=not ok)
                        if ok:
                            on_cart_changed()

                    return _on_add

                card = ft.Card(
                    col={"xs": 12, "sm": 6, "md": 4},
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
                                    controls=[
                                        ft.Container(
                                            content=ft.Text(
                                                prod.categoria_nome or "Geral",
                                                size=11,
                                                weight=ft.FontWeight.W_600,
                                                color=ft.Colors.DEEP_ORANGE_800,
                                            ),
                                            bgcolor=ft.Colors.DEEP_ORANGE_50,
                                            padding=ft.Padding.symmetric(horizontal=8, vertical=3),
                                            border_radius=ft.BorderRadius.all(10),
                                        ),
                                        availability_badge,
                                    ],
                                ),
                                ft.Text(
                                    prod.nome,
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    max_lines=1,
                                ),
                                ft.Text(
                                    prod.descricao or "Sem descrição informada.",
                                    size=13,
                                    color=ft.Colors.GREY_700,
                                    max_lines=2,
                                ),
                                ft.Divider(height=8),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text(
                                            format_brl(prod.preco),
                                            size=18,
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.Colors.DEEP_ORANGE_700,
                                        ),
                                        ft.Button(
                                            content="Adicionar",
                                            icon=ft.Icons.ADD_SHOPPING_CART,
                                            bgcolor=ft.Colors.DEEP_ORANGE_600,
                                            color=ft.Colors.WHITE,
                                            disabled=not prod.disponivel,
                                            on_click=_make_add_handler(prod),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ),
                )
                products_grid.controls.append(card)

        page.update()

    def _handle_seed(e=None) -> None:
        if not auth_controller.is_authenticated():
            on_auth_required()
            return
        ok, msg = order_controller.seed_sample_menu()
        show_feedback(page, msg, is_error=not ok)
        _load_data()

    def _on_search_change(e) -> None:
        nonlocal search_query
        search_query = e.control.value or ""
        _load_data()

    def _on_cat_select(e) -> None:
        nonlocal selected_category_id
        selected_category_id = e.control.value or "ALL"
        _load_data()

    search_field.on_change = _on_search_change
    category_dropdown.on_select = _on_cat_select

    _load_data()

    return ft.Column(
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
                            ft.Text("Cardápio Delivery", size=22, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                "Escolha os itens e adicione ao seu carrinho.",
                                size=13,
                                color=ft.Colors.GREY_600,
                            ),
                        ],
                    ),
                    ft.OutlinedButton(
                        content="Atualizar Cardápio",
                        icon=ft.Icons.REFRESH,
                        on_click=lambda e: _load_data(),
                    ),
                ],
            ),
            ft.Row(
                spacing=12,
                wrap=True,
                controls=[search_field, category_dropdown],
            ),
            status_container,
            products_grid,
        ],
    )
