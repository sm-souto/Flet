from typing import Callable
import flet as ft

from controllers.auth_controller import AuthController
from controllers.order_controller import OrderController
from models.order_model import ORDER_STATUSES
from models.product_model import Category, Product, format_brl
from views.ui_helpers import format_timestamp, show_confirm_dialog, show_feedback, status_badge


def build_admin_view(
    page: ft.Page,
    auth_controller: AuthController,
    order_controller: OrderController,
    on_auth_required: Callable[[], None],
    on_profile_updated: Callable[[], None],
) -> ft.Control:
    """Monta a area de gerenciamento (CRUD completo das tabelas e perfil)."""
    if not auth_controller.is_authenticated():
        on_auth_required()
        return ft.Container()

    active_section = "produtos"
    section_content = ft.Column(spacing=16)

    btn_produtos = ft.Button(content="Produtos", icon=ft.Icons.FASTFOOD)
    btn_categorias = ft.OutlinedButton(content="Categorias", icon=ft.Icons.CATEGORY)
    btn_pedidos = ft.OutlinedButton(content="Pedidos", icon=ft.Icons.RECEIPT_LONG)
    btn_perfil = ft.OutlinedButton(content="Meu Perfil", icon=ft.Icons.PERSON)

    def _update_section_buttons() -> None:
        mapping = {
            "produtos": btn_produtos,
            "categorias": btn_categorias,
            "pedidos": btn_pedidos,
            "perfil": btn_perfil,
        }
        for key, btn in mapping.items():
            if key == active_section:
                btn.style = ft.ButtonStyle(
                    bgcolor=ft.Colors.DEEP_ORANGE_600,
                    color=ft.Colors.WHITE,
                )
            else:
                btn.style = ft.ButtonStyle(
                    bgcolor=ft.Colors.GREY_200,
                    color=ft.Colors.GREY_800,
                )

    def _render_produtos() -> None:
        if not auth_controller.is_authenticated():
            on_auth_required()
            return

        ok_cat, _, categories = order_controller.list_categories()
        ok_prod, msg_prod, products = order_controller.list_products(only_available=False)
        if not ok_prod:
            show_feedback(page, msg_prod, is_error=True)

        cat_options = [ft.dropdown.Option(key=c.id, text=c.nome) for c in categories]

        nome_field = ft.TextField(label="Nome do produto", expand=True)
        preco_field = ft.TextField(
            label="Preço (R$)",
            hint_text="Ex.: 29.90",
            width=150,
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        cat_dropdown = ft.Dropdown(
            label="Categoria",
            width=220,
            options=cat_options,
            value=categories[0].id if categories else None,
        )
        desc_field = ft.TextField(label="Descrição (opcional)", expand=True)
        disp_switch = ft.Switch(label="Disponível no cardápio", value=True)

        def _handle_create_product(e) -> None:
            if not auth_controller.is_authenticated():
                on_auth_required()
                return
            ok, msg = order_controller.create_product(
                nome=nome_field.value or "",
                descricao=desc_field.value or "",
                preco_texto=preco_field.value or "",
                categoria_id=cat_dropdown.value or "",
                disponivel=bool(disp_switch.value),
            )
            show_feedback(page, msg, is_error=not ok)
            if ok:
                _render_produtos()

        def _open_edit_product(prod: Product) -> None:
            if not auth_controller.is_authenticated():
                on_auth_required()
                return
            e_nome = ft.TextField(label="Nome", value=prod.nome)
            e_desc = ft.TextField(label="Descrição", value=prod.descricao)
            e_preco = ft.TextField(label="Preço (R$)", value=f"{prod.preco:.2f}")
            e_cat = ft.Dropdown(
                label="Categoria",
                options=cat_options,
                value=prod.categoria_id,
            )
            e_disp = ft.Switch(label="Disponível", value=prod.disponivel)

            def _save_edit(e) -> None:
                ok, msg = order_controller.update_product(
                    product_id=prod.id,
                    nome=e_nome.value or "",
                    descricao=e_desc.value or "",
                    preco_texto=e_preco.value or "",
                    categoria_id=e_cat.value or "",
                    disponivel=bool(e_disp.value),
                )
                show_feedback(page, msg, is_error=not ok)
                if ok:
                    page.pop_dialog()
                    _render_produtos()

            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Editar Produto", weight=ft.FontWeight.BOLD),
                content=ft.Container(
                    width=400,
                    content=ft.Column(
                        tight=True,
                        spacing=10,
                        controls=[e_nome, e_cat, e_preco, e_desc, e_disp],
                    ),
                ),
                actions=[
                    ft.TextButton(content="Cancelar", on_click=lambda e: page.pop_dialog()),
                    ft.Button(
                        content="Salvar Alterações",
                        bgcolor=ft.Colors.DEEP_ORANGE_600,
                        color=ft.Colors.WHITE,
                        on_click=_save_edit,
                    ),
                ],
            )
            page.show_dialog(dlg)

        def _confirm_delete_product(prod: Product) -> None:
            def _do_delete() -> None:
                ok, msg = order_controller.delete_product(prod.id)
                show_feedback(page, msg, is_error=not ok)
                if ok:
                    _render_produtos()

            show_confirm_dialog(
                page,
                "Excluir produto",
                f"Deseja excluir o produto '{prod.nome}'?",
                _do_delete,
            )

        form_controls: list[ft.Control] = [
            ft.Text("Cadastrar Novo Produto", size=17, weight=ft.FontWeight.BOLD),
        ]
        if not ok_cat or not categories:
            form_controls.append(
                ft.Text(
                    "Cadastre primeiro uma categoria na aba 'Categorias' (ou carregue o cardápio de exemplo) para poder criar produtos.",
                    color=ft.Colors.AMBER_900,
                )
            )
        else:
            form_controls.extend(
                [
                    ft.Row(wrap=True, spacing=10, controls=[nome_field, cat_dropdown, preco_field]),
                    ft.Row(wrap=True, spacing=10, controls=[desc_field, disp_switch]),
                    ft.Button(
                        content="Cadastrar Produto",
                        icon=ft.Icons.ADD,
                        bgcolor=ft.Colors.DEEP_ORANGE_600,
                        color=ft.Colors.WHITE,
                        on_click=_handle_create_product,
                    ),
                ]
            )

        prod_cards: list[ft.Control] = []
        for p in products:
            prod_cards.append(
                ft.Card(
                    elevation=1,
                    content=ft.Container(
                        padding=14,
                        bgcolor=ft.Colors.WHITE,
                        border_radius=ft.BorderRadius.all(10),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            wrap=True,
                            controls=[
                                ft.Column(
                                    spacing=2,
                                    expand=True,
                                    controls=[
                                        ft.Text(
                                            f"{p.nome} ({p.categoria_nome or 'Sem categoria'})",
                                            weight=ft.FontWeight.BOLD,
                                            size=15,
                                        ),
                                        ft.Text(
                                            f"{format_brl(p.preco)} • {'Disponível' if p.disponivel else 'Indisponível'}",
                                            color=ft.Colors.GREY_700,
                                            size=13,
                                        ),
                                    ],
                                ),
                                ft.Row(
                                    spacing=4,
                                    controls=[
                                        ft.IconButton(
                                            icon=ft.Icons.EDIT_OUTLINED,
                                            tooltip="Editar produto",
                                            on_click=lambda e, item=p: _open_edit_product(item),
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE_OUTLINE,
                                            icon_color=ft.Colors.RED_600,
                                            tooltip="Excluir produto",
                                            on_click=lambda e, item=p: _confirm_delete_product(item),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ),
                )
            )

        if not prod_cards:
            prod_cards.append(ft.Text("Nenhum produto cadastrado ainda.", color=ft.Colors.GREY_600))

        section_content.controls = [
            ft.Card(
                elevation=2,
                content=ft.Container(
                    padding=16,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=ft.BorderRadius.all(12),
                    content=ft.Column(spacing=10, controls=form_controls),
                ),
            ),
            ft.Text("Produtos Cadastrados", size=17, weight=ft.FontWeight.BOLD),
            *prod_cards,
        ]
        page.update()

    def _render_categorias() -> None:
        if not auth_controller.is_authenticated():
            on_auth_required()
            return

        ok, msg, categories = order_controller.list_categories()
        if not ok:
            show_feedback(page, msg, is_error=True)

        nome_cat = ft.TextField(label="Nome da categoria", expand=True)
        desc_cat = ft.TextField(label="Descrição (opcional)", expand=True)

        def _handle_create_cat(e) -> None:
            if not auth_controller.is_authenticated():
                on_auth_required()
                return
            ok_c, msg_c = order_controller.create_category(
                nome=nome_cat.value or "",
                descricao=desc_cat.value or "",
            )
            show_feedback(page, msg_c, is_error=not ok_c)
            if ok_c:
                _render_categorias()

        def _open_edit_cat(cat: Category) -> None:
            e_nome = ft.TextField(label="Nome", value=cat.nome)
            e_desc = ft.TextField(label="Descrição", value=cat.descricao)

            def _save_edit(e) -> None:
                ok_u, msg_u = order_controller.update_category(
                    category_id=cat.id,
                    nome=e_nome.value or "",
                    descricao=e_desc.value or "",
                )
                show_feedback(page, msg_u, is_error=not ok_u)
                if ok_u:
                    page.pop_dialog()
                    _render_categorias()

            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Editar Categoria", weight=ft.FontWeight.BOLD),
                content=ft.Container(
                    width=380,
                    content=ft.Column(tight=True, spacing=10, controls=[e_nome, e_desc]),
                ),
                actions=[
                    ft.TextButton(content="Cancelar", on_click=lambda e: page.pop_dialog()),
                    ft.Button(
                        content="Salvar",
                        bgcolor=ft.Colors.DEEP_ORANGE_600,
                        color=ft.Colors.WHITE,
                        on_click=_save_edit,
                    ),
                ],
            )
            page.show_dialog(dlg)

        def _confirm_delete_cat(cat: Category) -> None:
            def _do_delete() -> None:
                ok_d, msg_d = order_controller.delete_category(cat.id)
                show_feedback(page, msg_d, is_error=not ok_d)
                if ok_d:
                    _render_categorias()

            show_confirm_dialog(
                page,
                "Excluir categoria",
                f"Deseja excluir a categoria '{cat.nome}'?",
                _do_delete,
            )

        cat_cards: list[ft.Control] = []
        for c in categories:
            cat_cards.append(
                ft.Card(
                    elevation=1,
                    content=ft.Container(
                        padding=14,
                        bgcolor=ft.Colors.WHITE,
                        border_radius=ft.BorderRadius.all(10),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            wrap=True,
                            controls=[
                                ft.Column(
                                    spacing=2,
                                    expand=True,
                                    controls=[
                                        ft.Text(c.nome, weight=ft.FontWeight.BOLD, size=15),
                                        ft.Text(
                                            c.descricao or "Sem descrição.",
                                            color=ft.Colors.GREY_600,
                                            size=13,
                                        ),
                                    ],
                                ),
                                ft.Row(
                                    spacing=4,
                                    controls=[
                                        ft.IconButton(
                                            icon=ft.Icons.EDIT_OUTLINED,
                                            tooltip="Editar categoria",
                                            on_click=lambda e, item=c: _open_edit_cat(item),
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE_OUTLINE,
                                            icon_color=ft.Colors.RED_600,
                                            tooltip="Excluir categoria",
                                            on_click=lambda e, item=c: _confirm_delete_cat(item),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ),
                )
            )

        if not cat_cards:
            cat_cards.append(ft.Text("Nenhuma categoria cadastrada ainda.", color=ft.Colors.GREY_600))

        section_content.controls = [
            ft.Card(
                elevation=2,
                content=ft.Container(
                    padding=16,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=ft.BorderRadius.all(12),
                    content=ft.Column(
                        spacing=10,
                        controls=[
                            ft.Text("Cadastrar Nova Categoria", size=17, weight=ft.FontWeight.BOLD),
                            ft.Row(wrap=True, spacing=10, controls=[nome_cat, desc_cat]),
                            ft.Button(
                                content="Cadastrar Categoria",
                                icon=ft.Icons.ADD,
                                bgcolor=ft.Colors.DEEP_ORANGE_600,
                                color=ft.Colors.WHITE,
                                on_click=_handle_create_cat,
                            ),
                        ],
                    ),
                ),
            ),
            ft.Text("Categorias Cadastradas", size=17, weight=ft.FontWeight.BOLD),
            *cat_cards,
        ]
        page.update()

    def _render_pedidos() -> None:
        if not auth_controller.is_authenticated():
            on_auth_required()
            return

        ok, msg, orders = order_controller.list_orders()
        if not ok:
            show_feedback(page, msg, is_error=True)

        order_cards: list[ft.Control] = []
        for o in orders:
            status_dd = ft.Dropdown(
                label="Atualizar status",
                width=210,
                value=o.status,
                options=[ft.dropdown.Option(key=s, text=s) for s in ORDER_STATUSES],
            )

            def _make_status_handler(oid: str):
                def _on_select(e) -> None:
                    if not auth_controller.is_authenticated():
                        on_auth_required()
                        return
                    ok_s, msg_s = order_controller.update_order_status(oid, e.control.value or "")
                    show_feedback(page, msg_s, is_error=not ok_s)
                    _render_pedidos()

                return _on_select

            def _make_delete_order(oid: str):
                def _on_click(e) -> None:
                    def _do_delete() -> None:
                        ok_d, msg_d = order_controller.delete_order(oid)
                        show_feedback(page, msg_d, is_error=not ok_d)
                        _render_pedidos()

                    show_confirm_dialog(
                        page,
                        "Excluir pedido",
                        f"Deseja excluir o pedido #{oid[:8].upper()}?",
                        _do_delete,
                    )

                return _on_click

            status_dd.on_select = _make_status_handler(o.id)

            order_cards.append(
                ft.Card(
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
                                    spacing=4,
                                    expand=True,
                                    controls=[
                                        ft.Row(
                                            spacing=8,
                                            controls=[
                                                ft.Text(
                                                    f"Pedido #{o.id[:8].upper()}",
                                                    weight=ft.FontWeight.BOLD,
                                                    size=15,
                                                ),
                                                status_badge(o.status),
                                            ],
                                        ),
                                        ft.Text(
                                            f"{format_timestamp(o.criado_em)} • {format_brl(o.total)}",
                                            size=13,
                                            color=ft.Colors.GREY_700,
                                        ),
                                        ft.Text(
                                            f"Endereço: {o.endereco_entrega}",
                                            size=12,
                                            color=ft.Colors.GREY_600,
                                        ),
                                    ],
                                ),
                                ft.Row(
                                    spacing=8,
                                    controls=[
                                        status_dd,
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE_OUTLINE,
                                            icon_color=ft.Colors.RED_600,
                                            tooltip="Excluir pedido",
                                            on_click=_make_delete_order(o.id),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ),
                )
            )

        if not order_cards:
            order_cards.append(ft.Text("Nenhum pedido encontrado.", color=ft.Colors.GREY_600))

        section_content.controls = [
            ft.Text("Gerenciar Status dos Pedidos", size=17, weight=ft.FontWeight.BOLD),
            *order_cards,
        ]
        page.update()

    def _render_perfil() -> None:
        if not auth_controller.is_authenticated() or auth_controller.usuario_atual is None:
            on_auth_required()
            return

        user = auth_controller.usuario_atual
        p_nome = ft.TextField(label="Nome completo", value=user.nome, prefix_icon=ft.Icons.PERSON)
        p_tel = ft.TextField(label="Telefone", value=user.telefone, prefix_icon=ft.Icons.PHONE)
        p_end = ft.TextField(
            label="Endereço padrão de entrega",
            value=user.endereco,
            prefix_icon=ft.Icons.LOCATION_ON,
        )

        def _save_profile(e) -> None:
            if not auth_controller.is_authenticated():
                on_auth_required()
                return
            ok, msg = auth_controller.update_profile(
                nome=p_nome.value or "",
                telefone=p_tel.value or "",
                endereco=p_end.value or "",
            )
            show_feedback(page, msg, is_error=not ok)
            if ok:
                on_profile_updated()

        section_content.controls = [
            ft.Card(
                elevation=2,
                content=ft.Container(
                    padding=18,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=ft.BorderRadius.all(12),
                    content=ft.Column(
                        spacing=12,
                        controls=[
                            ft.Text("Dados do Meu Perfil", size=17, weight=ft.FontWeight.BOLD),
                            ft.Text(f"E-mail da conta: {user.email}", color=ft.Colors.GREY_700),
                            p_nome,
                            p_tel,
                            p_end,
                            ft.Button(
                                content="Salvar Perfil",
                                icon=ft.Icons.SAVE,
                                bgcolor=ft.Colors.DEEP_ORANGE_600,
                                color=ft.Colors.WHITE,
                                on_click=_save_profile,
                            ),
                        ],
                    ),
                ),
            )
        ]
        page.update()

    def _switch_section(sec: str) -> None:
        nonlocal active_section
        if not auth_controller.is_authenticated():
            on_auth_required()
            return
        active_section = sec
        _update_section_buttons()
        if sec == "produtos":
            _render_produtos()
        elif sec == "categorias":
            _render_categorias()
        elif sec == "pedidos":
            _render_pedidos()
        else:
            _render_perfil()

    btn_produtos.on_click = lambda e: _switch_section("produtos")
    btn_categorias.on_click = lambda e: _switch_section("categorias")
    btn_pedidos.on_click = lambda e: _switch_section("pedidos")
    btn_perfil.on_click = lambda e: _switch_section("perfil")

    _switch_section("produtos")

    return ft.Column(
        spacing=16,
        controls=[
            ft.Text("Painel de Gerenciamento", size=22, weight=ft.FontWeight.BOLD),
            ft.Row(
                wrap=True,
                spacing=8,
                controls=[btn_produtos, btn_categorias, btn_pedidos, btn_perfil],
            ),
            section_content,
        ],
    )
