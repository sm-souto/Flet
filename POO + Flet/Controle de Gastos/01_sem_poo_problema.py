# MUITO DIFÍCIL DE COMPREENDER
import flet as ft


def main(page: ft.Page):
    
    page.title = "Sistema | Controle de Gastos"
    page.theme_mode = ft.ThemeMode.LIGHT

    total_gasto = 0.0
    texto_total = ft.Text(
        f"Total Gasto: R$ {total_gasto:.2f}",
        size=24,
        weight=ft.FontWeight.BOLD,
    )

    input_descricao = ft.TextField(label="Descrição do Gasto", expand=True)
    input_valor = ft.TextField(label="Valor (R$)", width=130)

    lista_despesas = ft.Column(spacing=8)


    def adicionar_despesa(e):
        nonlocal total_gasto

        if not input_descricao.value or not input_valor.value:
            return

        descricao = input_descricao.value
        valor = float(input_valor.value.replace(",", "."))

        container_despesa = ft.Container(
            bgcolor="#C8E6C9",
            border_radius=8,
            padding=12,
        )

        def remover_despesa(item_container):
            nonlocal total_gasto
            total_gasto -= valor
            texto_total.value = f"Total Gasto: R$ {total_gasto:.2f}"
            lista_despesas.controls.remove(item_container)
            page.update()

        def clicar_lixeira(e):
            remover_despesa(container_despesa)

        botao_lixeira = ft.IconButton(
            icon=ft.Icons.DELETE,
            icon_color=ft.Colors.RED_400,
            on_click=clicar_lixeira,
        )

        container_despesa.content = ft.Row(
            controls=[
                ft.Icon(ft.Icons.SHOPPING_BASKET),
                ft.Text(descricao, expand=True, size=16),
                ft.Text(
                    f"R$ {valor:.2f}",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                ),
                botao_lixeira,
            ]
        )

        total_gasto += valor
        texto_total.value = f"Total Gasto: R$ {total_gasto:.2f}"
        lista_despesas.controls.append(container_despesa)
        input_descricao.value = ""
        input_valor.value = ""
        page.update()


    botao_registrar = ft.Button("Registrar", on_click=adicionar_despesa)

    page.add(
        texto_total,
        ft.Row(controls=[input_descricao, input_valor, botao_registrar]),
        lista_despesas,
    )   


ft.run(main)