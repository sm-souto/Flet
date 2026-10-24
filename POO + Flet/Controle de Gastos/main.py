import flet as ft
from classe_despesa_base import DespesaCard


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
 
    def remover_despesa(card_despesa):
        nonlocal total_gasto
        total_gasto -= card_despesa.valor
        texto_total.value = f"Total Gasto: R$ {total_gasto:.2f}"
        lista_despesas.controls.remove(card_despesa)
        page.update()
 
    def adicionar_despesa(e):
        nonlocal total_gasto
 
        if not input_descricao.value or not input_valor.value:
            return
 
        descricao = input_descricao.value
        valor = float(input_valor.value.replace(",", "."))
 
        novo_card = DespesaCard(
            descricao=descricao,
            valor=valor,
            on_remover=remover_despesa,
        )
 
        total_gasto += valor
        texto_total.value = f"Total Gasto: R$ {total_gasto:.2f}"
        lista_despesas.controls.append(novo_card)
        input_descricao.value = ""
        input_valor.value = ""
        page.update()
 
    botao_registrar = ft.Button("Registrar", on_click=adicionar_despesa)
 
    page.add(
        texto_total,
        ft.Row(controls=[input_descricao, input_valor, botao_registrar]),
        lista_despesas
    )
 
 
ft.run(main)