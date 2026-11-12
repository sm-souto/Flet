import flet as ft
from views.despesa_card import DespesaCard
from controller.despesa_controller import DespesaController


def gastos_view(page: ft.Page):
    page.title = "Sistema de Controle de Gastos"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    controller = DespesaController()

    texto_total = ft.Text(
        value="Total Gasto: R$ 0.00",
        size=28,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.GREEN_800,
    )

    texto_erro = ft.Text(value="", color=ft.Colors.RED_600, size=14)

    input_descricao = ft.TextField(
        label="Descrição do Gasto",
        hint_text="Ex: Lanche, Passagem",
        expand=True,
    )

    input_valor = ft.TextField(label="Valor (R$)", hint_text="Ex: 15,50", width=150)

    lista_despesas = ft.Column(spacing=8)

    def atualizar_total():
        total = 0.0
        for card in lista_despesas.controls:
            total += card.valor
        texto_total.value = f"Total Gasto: R$ {total:.2f}"

    def remover_despesa(card_despesa: DespesaCard):
        controller.remover_despesa(card_despesa.despesa_id)
        lista_despesas.controls.remove(card_despesa)
        atualizar_total()

    def adicionar_despesa(evento):
        texto_erro.value = ""

        descricao_digitada = input_descricao.value
        valor_digitado = input_valor.value

        if not descricao_digitada or not valor_digitado:
            texto_erro.value = "Preencha todos os campos antes de registrar."
            return

        valor_limpo = valor_digitado.strip().replace(",", ".")
        valor_float = float(valor_limpo)

        if valor_float <= 0:
            texto_erro.value = "O valor deve ser maior que zero."
            return

        despesa_salva = controller.adicionar_despesa(
            descricao=descricao_digitada,
            valor_texto=valor_digitado,
        )

        novo_card = DespesaCard(
            despesa_id=despesa_salva.id,
            descricao=despesa_salva.descricao,
            valor=despesa_salva.valor,
            on_remover=remover_despesa,
        )

        lista_despesas.controls.append(novo_card)
        atualizar_total()

        input_descricao.value = ""
        input_valor.value = ""

    def carregar_despesas_salvas():
        despesas = controller.listar_despesas()
        for despesa in despesas:
            card = DespesaCard(
                despesa_id=despesa.id,
                descricao=despesa.descricao,
                valor=despesa.valor,
                on_remover=remover_despesa,
            )
            lista_despesas.controls.append(card)
        atualizar_total()

    botao_registrar = ft.Button(
        content="Registrar",
        icon=ft.Icons.ADD,
        on_click=adicionar_despesa,
        bgcolor=ft.Colors.GREEN_600,
        color=ft.Colors.WHITE,
    )

    formulario = ft.Row(
        controls=[input_descricao, input_valor, botao_registrar],
        alignment=ft.MainAxisAlignment.START,
    )

    cabecalho = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("💰 Controle de Gastos", size=32, weight=ft.FontWeight.BOLD),
                texto_total,
                ft.Divider(),
            ]
        ),
        padding=12,
    )

    page.add(
        cabecalho,
        formulario,
        texto_erro,
        ft.Divider(),
        ft.Text("Despesas Registradas:", size=18, weight=ft.FontWeight.W_600),
        lista_despesas,
    )

    carregar_despesas_salvas()