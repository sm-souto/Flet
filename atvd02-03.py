import flet as ft  # Importa a biblioteca do Flet para criar a interface visual


def main(page: ft.Page):
    # --- CONFIGURAÇÕES DA PÁGINA ---
    page.title = "Mudança de Tema"
    page.padding = 30
    page.theme_mode = ft.ThemeMode.LIGHT  # Tema inicial: claro
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- ÍCONE DE LÂMPADA ---
    # O ícone também muda (acesa/apagada) conforme o tema, dando feedback visual extra
    icone_lampada = ft.Icon(
        name=ft.Icons.LIGHTBULB,
        size=50,
        color="amber",
    )

    # --- TEXTO QUE MOSTRA O TEMA ATUAL ---
    texto_tema = ft.Text(
        "O tema atual é: CLARO",
        size=18,
        weight="bold",
    )

    # --- FUNÇÃO AUXILIAR: atualiza ícone e texto conforme o tema da página ---
    def atualizar_indicadores():
        if page.theme_mode == ft.ThemeMode.LIGHT:
            texto_tema.value = "O tema atual é: CLARO"
            icone_lampada.name = ft.Icons.LIGHTBULB          # lâmpada acesa
            icone_lampada.color = "amber"
        else:
            texto_tema.value = "O tema atual é: ESCURO"
            icone_lampada.name = ft.Icons.LIGHTBULB_OUTLINE  # lâmpada apagada
            icone_lampada.color = "grey"

    # --- VERSÃO BASE: um único botão que alterna o tema ---
    def alternar_tema(e):
        # Verifica o tema atual da página (page.theme_mode) e troca
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
        else:
            page.theme_mode = ft.ThemeMode.LIGHT

        atualizar_indicadores()  # Atualiza o texto e o ícone para refletir a mudança
        page.update()

    botao_alternar = ft.ElevatedButton(
        text="MUDAR TEMA",
        on_click=alternar_tema,
    )

    # --- DESAFIO: dois botões separados, cada um define o tema diretamente ---
    def definir_tema_escuro(e):
        page.theme_mode = ft.ThemeMode.DARK
        atualizar_indicadores()
        page.update()

    def definir_tema_claro(e):
        page.theme_mode = ft.ThemeMode.LIGHT
        atualizar_indicadores()
        page.update()

    botao_escuro = ft.FilledButton(          # Botão preenchido (mais "forte" visualmente)
        text="Tema Escuro",
        on_click=definir_tema_escuro,
    )
    botao_claro = ft.OutlinedButton(         # Botão apenas com borda (mais "leve")
        text="Tema Claro",
        on_click=definir_tema_claro,
    )

    # Linha com os dois botões do desafio, lado a lado
    linha_botoes_desafio = ft.Row(
        controls=[botao_escuro, botao_claro],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )

    # --- MONTAGEM DA TELA ---
    page.add(
        ft.Column(
            controls=[
                icone_lampada,
                texto_tema,
                botao_alternar,           # Solução do exercício base
                ft.Divider(),
                linha_botoes_desafio,      # Solução do desafio
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )


# Ponto de entrada do aplicativo
ft.app(target=main)
