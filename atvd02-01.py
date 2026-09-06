import flet as ft  # Importa a biblioteca do Flet para criar a interface visual


def main(page: ft.Page):
    # --- CONFIGURAÇÕES DA PÁGINA ---
    page.title = "Fato do Dia"          # Define o título que aparece na janela
    page.padding = 30                   # Adiciona um espaçamento nas bordas da página
    page.bgcolor = ft.Colors.BLUE_GREY_50  # Cor de fundo suave para a tela
    # Centraliza o card na tela toda (horizontal e verticalmente)
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- DESAFIO: FONTE CUSTOMIZADA DO GOOGLE FONTS ---
    # page.fonts recebe um dicionário {"nome_que_eu_escolho": "url_do_arquivo_da_fonte"}
    # O Flet baixa e registra essa fonte para ser usada em qualquer ft.Text
    page.fonts = {
        "Roboto Slab": "https://fonts.gstatic.com/s/robotoslab/v34/BngbUXZYTXPIvIBgJJSb6s3BzlRRfKOFbvjojISzR8T3.ttf"
    }

    # --- TÍTULO CENTRALIZADO ---
    # text_align=ft.TextAlign.CENTER alinha o texto dentro do próprio ft.Text
    titulo = ft.Text(
        "FATO DO DIA",
        size=22,
        weight="bold",
        text_align=ft.TextAlign.CENTER,
    )

    # --- LINHA DE SEPARAÇÃO ---
    # ft.Divider cria uma linha horizontal, como um <hr> do HTML
    linha_separadora = ft.Divider(thickness=1, color="grey")

    # --- TEXTO PRINCIPAL (o "fato") ---
    # font_family="Roboto Slab" usa a fonte customizada registrada acima
    fato = ft.Text(
        "As formigas se esticam ao acordar pela manhã, "
        "como se estivessem bocejando.",
        size=16,
        text_align=ft.TextAlign.CENTER,  # Texto principal centralizado
        font_family="Roboto Slab",
    )

    # --- FONTE DA INFORMAÇÃO, ALINHADA À DIREITA ---
    fonte_texto = ft.Text(
        "- Fonte: Curiosidades",
        size=12,
        italic=True,
        color="grey700",
        text_align=ft.TextAlign.RIGHT,
    )

    # --- MONTAGEM DA COLUNA (empilha os textos, um abaixo do outro) ---
    coluna_card = ft.Column(
        controls=[titulo, linha_separadora, fato, fonte_texto],
        spacing=15,
        # width fixo faz o text_align de cada Text ter efeito visível,
        # pois cada Text passa a ocupar toda a largura da coluna
        width=400,
    )

    # --- MOLDURA DO CARD (Container dando o visual de "cartão") ---
    card_info = ft.Container(
        content=coluna_card,
        bgcolor=ft.Colors.WHITE,
        padding=25,
        border_radius=12,
        border=(1, "grey300"),
    )

    # Adiciona o card pronto à página visual
    page.add(card_info)


# Ponto de entrada do aplicativo
ft.app(target=main)