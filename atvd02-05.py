import flet as ft  # Importa a biblioteca do Flet para criar a interface visual


def main(page: ft.Page):
    # --- CONFIGURAÇÕES DA PÁGINA ---
    page.title = "Barra de Reações"
    page.padding = 30
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- ESTADO DA CURTIDA ---
    # Um dicionário guarda o contador e se o usuário já curtiu ou não.
    # Usamos um dicionário (em vez de variáveis soltas) para poder
    # alterar os valores de dentro das funções sem precisar de "nonlocal"
    estado = {"curtidas": 15, "curtido": False}

    # --- TEXTO QUE MOSTRA O NÚMERO DE CURTIDAS ---
    texto_curtidas = ft.Text(f"{estado['curtidas']} Curtidas", size=16)

    # --- BOTÃO DE CORAÇÃO (CURTIR) ---
    # Começa com o ícone de coração vazio (FAVORITE_BORDER)
    botao_curtir = ft.IconButton(
        icon=ft.Icons.FAVORITE_BORDER,
        icon_color="black",
    )

    def alternar_curtida(e):
        if not estado["curtido"]:
            # Usuário está curtindo agora
            estado["curtido"] = True
            estado["curtidas"] += 1
            # DESAFIO: coração preenchido e cor rosa
            botao_curtir.icon = ft.Icons.FAVORITE
            botao_curtir.icon_color = "pink"
        else:
            # Usuário está descurtindo (clicou de novo)
            estado["curtido"] = False
            estado["curtidas"] -= 1
            # Volta ao estado original: coração vazio, cor padrão
            botao_curtir.icon = ft.Icons.FAVORITE_BORDER
            botao_curtir.icon_color = "black"

        # Atualiza o texto do contador de curtidas
        texto_curtidas.value = f"{estado['curtidas']} Curtidas"
        page.update()

    botao_curtir.on_click = alternar_curtida

    # --- BOTÃO DE COMENTÁRIO (apenas ilustrativo, sem lógica própria) ---
    botao_comentar = ft.IconButton(
        icon=ft.Icons.CHAT_BUBBLE_OUTLINE,
        icon_color="black",
    )

    # --- BOTÃO DE COMPARTILHAR (apenas ilustrativo, sem lógica própria) ---
    botao_compartilhar = ft.IconButton(
        icon=ft.Icons.SHARE_OUTLINED,
        icon_color="black",
    )

    # --- LINHA COM OS 3 BOTÕES DE REAÇÃO ---
    barra_botoes = ft.Row(
        controls=[botao_curtir, botao_comentar, botao_compartilhar],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15,
    )

    # --- MONTAGEM DA TELA ---
    page.add(
        ft.Column(
            controls=[barra_botoes, texto_curtidas],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )


# Ponto de entrada do aplicativo
ft.app(target=main)
