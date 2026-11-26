from typing import Callable
import flet as ft


def show_feedback(page: ft.Page, message: str, is_error: bool = False) -> None:
    """Exibe uma notificacao amigavel ao usuario via SnackBar."""
    snack = ft.SnackBar(
        content=ft.Text(message, color=ft.Colors.WHITE, weight=ft.FontWeight.W_500),
        bgcolor=ft.Colors.RED_700 if is_error else ft.Colors.GREEN_700,
        duration=3500,
    )
    page.show_dialog(snack)


def show_confirm_dialog(
    page: ft.Page,
    title: str,
    message: str,
    on_confirm: Callable[[], None],
    confirm_label: str = "Excluir",
    danger: bool = True,
) -> None:
    """Abre um dialogo de confirmacao antes de executar uma acao destrutiva."""

    def _close(e=None) -> None:
        page.pop_dialog()

    def _confirm(e=None) -> None:
        page.pop_dialog()
        on_confirm()

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(title, weight=ft.FontWeight.BOLD),
        content=ft.Text(message),
        actions=[
            ft.TextButton(content="Cancelar", on_click=_close),
            ft.Button(
                content=confirm_label,
                bgcolor=ft.Colors.RED_700 if danger else ft.Colors.DEEP_ORANGE_600,
                color=ft.Colors.WHITE,
                on_click=_confirm,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.show_dialog(dialog)


_STATUS_STYLES: dict[str, tuple[str, str]] = {
    "Recebido": (ft.Colors.BLUE_50, ft.Colors.BLUE_800),
    "Em preparo": (ft.Colors.AMBER_50, ft.Colors.AMBER_900),
    "Saiu para entrega": (ft.Colors.DEEP_ORANGE_50, ft.Colors.DEEP_ORANGE_800),
    "Entregue": (ft.Colors.GREEN_50, ft.Colors.GREEN_800),
    "Cancelado": (ft.Colors.RED_50, ft.Colors.RED_800),
}


def status_badge(status: str) -> ft.Container:
    """Retorna um selo colorido para o status do pedido."""
    bg, fg = _STATUS_STYLES.get(status, (ft.Colors.GREY_200, ft.Colors.GREY_800))
    return ft.Container(
        content=ft.Text(status, size=12, weight=ft.FontWeight.W_600, color=fg),
        bgcolor=bg,
        padding=ft.Padding.symmetric(horizontal=10, vertical=4),
        border_radius=ft.BorderRadius.all(12),
    )


def format_timestamp(iso_str: str) -> str:
    """Formata timestamp ISO do banco para exibicao simples (DD/MM/AAAA HH:MM)."""
    if not iso_str:
        return ""
    try:
        date_part, time_part = iso_str.split("T", 1)
        year, month, day = date_part.split("-")
        hh_mm = time_part[:5]
        return f"{day}/{month}/{year} às {hh_mm}"
    except Exception:
        return iso_str[:16]
