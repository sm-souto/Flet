from typing import Callable
import flet as ft

from controllers.auth_controller import AuthController
from views.ui_helpers import show_feedback


def build_login_view(
    page: ft.Page,
    auth_controller: AuthController,
    on_login_success: Callable[[], None],
) -> ft.Control:
    """Monta a tela inicial de Login e Cadastro utilizando Supabase Auth."""
    is_register_mode = False

    feedback_text = ft.Text("", color=ft.Colors.RED_700, size=13, visible=False)

    nome_field = ft.TextField(
        label="Nome completo",
        prefix_icon=ft.Icons.PERSON,
        visible=False,
    )
    telefone_field = ft.TextField(
        label="Telefone (opcional)",
        prefix_icon=ft.Icons.PHONE,
        visible=False,
    )
    endereco_field = ft.TextField(
        label="Endereço padrão de entrega (opcional)",
        prefix_icon=ft.Icons.LOCATION_ON,
        visible=False,
    )
    email_field = ft.TextField(
        label="E-mail",
        prefix_icon=ft.Icons.EMAIL,
        keyboard_type=ft.KeyboardType.EMAIL,
    )
    password_field = ft.TextField(
        label="Senha",
        prefix_icon=ft.Icons.LOCK,
        password=True,
        can_reveal_password=True,
    )

    submit_btn = ft.Button(
        content="Entrar",
        icon=ft.Icons.LOGIN,
        bgcolor=ft.Colors.DEEP_ORANGE_600,
        color=ft.Colors.WHITE,
        height=46,
        width=float("inf"),
    )

    login_tab_btn = ft.Button(
        content="Entrar",
        bgcolor=ft.Colors.DEEP_ORANGE_600,
        color=ft.Colors.WHITE,
        expand=True,
    )
    register_tab_btn = ft.OutlinedButton(
        content="Criar Conta",
        expand=True,
    )

    def _set_feedback(msg: str, is_error: bool = True) -> None:
        feedback_text.value = msg
        feedback_text.color = ft.Colors.RED_700 if is_error else ft.Colors.GREEN_700
        feedback_text.visible = bool(msg)
        page.update()

    def _switch_mode(register: bool) -> None:
        nonlocal is_register_mode
        is_register_mode = register
        nome_field.visible = register
        telefone_field.visible = register
        endereco_field.visible = register
        feedback_text.visible = False

        if register:
            submit_btn.content = "Cadastrar e Entrar"
            submit_btn.icon = ft.Icons.PERSON_ADD
            login_tab_btn.bgcolor = ft.Colors.GREY_200
            login_tab_btn.color = ft.Colors.GREY_800
            register_tab_btn.style = ft.ButtonStyle(
                bgcolor=ft.Colors.DEEP_ORANGE_600,
                color=ft.Colors.WHITE,
            )
        else:
            submit_btn.content = "Entrar"
            submit_btn.icon = ft.Icons.LOGIN
            login_tab_btn.bgcolor = ft.Colors.DEEP_ORANGE_600
            login_tab_btn.color = ft.Colors.WHITE
            register_tab_btn.style = None

        page.update()

    def _handle_submit(e=None) -> None:
        _set_feedback("")
        submit_btn.disabled = True
        page.update()

        try:
            if is_register_mode:
                ok, msg = auth_controller.register(
                    nome=nome_field.value or "",
                    email=email_field.value or "",
                    password=password_field.value or "",
                    telefone=telefone_field.value or "",
                    endereco=endereco_field.value or "",
                )
                if ok and auth_controller.is_authenticated():
                    show_feedback(page, msg, is_error=False)
                    on_login_success()
                    return
                if ok:
                    _switch_mode(False)
                    _set_feedback(msg, is_error=False)
                else:
                    _set_feedback(msg, is_error=True)
            else:
                ok, msg = auth_controller.login(
                    email=email_field.value or "",
                    password=password_field.value or "",
                )
                if ok and auth_controller.is_authenticated():
                    show_feedback(page, msg, is_error=False)
                    on_login_success()
                    return
                _set_feedback(msg, is_error=True)
        except Exception:
            _set_feedback("Não foi possível concluir a operação no momento.", is_error=True)
        finally:
            submit_btn.disabled = False
            page.update()

    login_tab_btn.on_click = lambda e: _switch_mode(False)
    register_tab_btn.on_click = lambda e: _switch_mode(True)
    submit_btn.on_click = _handle_submit
    email_field.on_submit = _handle_submit
    password_field.on_submit = _handle_submit

    card = ft.Card(
        elevation=4,
        content=ft.Container(
            width=430,
            padding=28,
            bgcolor=ft.Colors.WHITE,
            border_radius=ft.BorderRadius.all(16),
            content=ft.Column(
                spacing=14,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(
                        ft.Icons.DELIVERY_DINING,
                        size=52,
                        color=ft.Colors.DEEP_ORANGE_600,
                    ),
                    ft.Text(
                        "SaborExpress Delivery",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREY_900,
                    ),
                    ft.Text(
                        "Faça login ou crie sua conta para pedir e gerenciar seu cardápio.",
                        size=13,
                        color=ft.Colors.GREY_600,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Row(
                        spacing=10,
                        controls=[login_tab_btn, register_tab_btn],
                    ),
                    nome_field,
                    email_field,
                    password_field,
                    telefone_field,
                    endereco_field,
                    feedback_text,
                    submit_btn,
                ],
            ),
        ),
    )

    return ft.Container(
        expand=True,
        alignment=ft.Alignment.CENTER,
        padding=20,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            controls=[card],
        ),
    )
