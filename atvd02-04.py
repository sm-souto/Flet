import flet as ft  # Importa a biblioteca do Flet para criar a interface visual


def main(page: ft.Page):
    # --- CONFIGURAÇÕES DA PÁGINA ---
    page.title = "Layout de Card"  # Define o título que aparece na janela
    page.padding = 30              # Adiciona um espaçamento nas bordas da página
    page.bgcolor = ft.Colors.BLUE_GREY_50  # Define uma cor de fundo suave para a tela

    # --- MONTAGEM DA COLUNA DIREITA (TEXTOS) ---
    # Criamos a ft.Column que vai guardar os textos empilhados (um abaixo do outro)
    coluna_textos = ft.Column(
        controls=[
            ft.Text("Fone de Ouvido Bluetooth", size=20, weight="bold"),  # Título do produto
            ft.Text("- Cancelamento de ruído\n- Bateria de 20h", size=14, color="grey"),  # Descrição
            ft.Text("R$ 299,90", size=18, weight="bold", color="green"),  # Preço em destaque
        ],
        spacing=10,  # Espaço de 10 pixels entre cada texto
        alignment=ft.MainAxisAlignment.CENTER,  # Alinha o conteúdo verticalmente no centro da coluna
    )

    # --- MONTAGEM DO CARD COMPLETO (EIXO HORIZONTAL) ---
    # Usamos uma ft.Row para colocar a Imagem ao lado da Coluna de Textos
    card_linha = ft.Row(
        controls=[
            # 1º Item da Row: A Imagem (100x100 pixels)
            ft.Image(
                src="https://picsum.photos/100/100",  # URL de uma imagem de exemplo
                width=100,                             # Largura fixa
                height=100,                            # Altura fixa
                fit=ft.ImageFit.COVER,                 # Ajusta a imagem sem distorcer
                border_radius=8,                       # Arredonda os cantos da imagem
            ),
            # 2º Item da Row: A Coluna com os Textos que criamos acima
            coluna_textos,
        ],
        spacing=20,  # Espaço horizontal de 20 pixels entre a imagem e o texto
        vertical_alignment=ft.CrossAxisAlignment.CENTER,  # Alinha verticalmente no centro da linha
    )

    # --- MOLDURA DO CARD (CONTAINER) ---
    # Colocamos a ft.Row dentro de um ft.Container para dar o aspecto visual de "cartão"
    card_produto = ft.Container(
        content=card_linha,               # Insere a linha montada dentro da caixa
        bgcolor=ft.Colors.WHITE,          # Cor de fundo branca para o cartão
        padding=20,                       # Espaçamento interno (margem interna)
        border_radius=12,                 # Arredonda as bordas do cartão
        border=ft.border.all(1, "grey"),  # Borda fina para dar acabamento
        width=450,                        # Largura total fixa do card
    )

    # Adiciona o card pronto à página visual
    page.add(card_produto)

    # ---------------------------------------------------------------
    # --- DESAFIO: PLAYER DE MÚSICA ---
    # Uma ft.Row com 3 IconButtons (Voltar, Play/Pause, Avançar),
    # todos centralizados na linha
    # ---------------------------------------------------------------

    # Guardamos o estado de "tocando" em uma lista para poder alterá-lo
    # de dentro da função (variáveis simples não podem ser reatribuídas
    # dentro de uma função aninhada sem "nonlocal")
    estado_player = {"tocando": False}

    # Ícone central do player: começa como "play" (triângulo)
    botao_play_pause = ft.IconButton(
        icon=ft.Icons.PLAY_ARROW,
        icon_size=36,
    )

    def alternar_play_pause(e):
        # Inverte o estado (tocando <-> pausado)
        estado_player["tocando"] = not estado_player["tocando"]
        # Troca o ícone conforme o novo estado
        if estado_player["tocando"]:
            botao_play_pause.icon = ft.Icons.PAUSE
        else:
            botao_play_pause.icon = ft.Icons.PLAY_ARROW
        page.update()

    botao_play_pause.on_click = alternar_play_pause

    player_musica = ft.Row(
        controls=[
            ft.IconButton(icon=ft.Icons.SKIP_PREVIOUS, icon_size=32),  # Botão Voltar
            botao_play_pause,                                          # Botão Play/Pause
            ft.IconButton(icon=ft.Icons.SKIP_NEXT, icon_size=32),      # Botão Avançar
        ],
        alignment=ft.MainAxisAlignment.CENTER,  # Centraliza os 3 botões na linha
        spacing=5,
    )

    # Container só para dar um acabamento visual parecido com o card acima
    card_player = ft.Container(
        content=player_musica,
        bgcolor=ft.Colors.WHITE,
        padding=15,
        border_radius=12,
        border=ft.border.all(1, "grey"),
        width=450,
    )

    page.add(card_player)


# Ponto de entrada do aplicativo
ft.app(target=main)
