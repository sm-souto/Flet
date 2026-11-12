import flet as ft
from views.gastos_view import gastos_view


def main(page: ft.Page):
    gastos_view(page)


if __name__ == "__main__":
    ft.run(main)