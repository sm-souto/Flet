import flet as ft  # Importa a biblioteca do Flet para criar a interface visual


def main(page: ft.Page):
    # --- CONFIGURAÇÕES DA PÁGINA ---
    page.title = "Galeria de Imagens"
    page.padding = 30
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- LISTA DE IMAGENS DISPONÍVEIS ---
    # Usamos o serviço picsum.photos (imagens de exemplo) com "seeds"
    # diferentes para simular fotos diferentes
    urls_imagens = [
        "https://picsum.photos/seed/foto1/500/300",
        "https://picsum.photos/seed/foto2/500/300",
        "https://picsum.photos/seed/foto3/500/300",
    ]

    # --- IMAGEM PRINCIPAL (GRANDE) ---
    # Começa mostrando a primeira imagem da lista
    imagem_principal = ft.Image(
        src=urls_imagens[0],
        width=500,
        height=300,
        fit=ft.ImageFit.COVER,   # Preenche o espaço sem distorcer
        border_radius=8,
    )

    # --- FUNÇÃO QUE TROCA A IMAGEM PRINCIPAL ---
    # Recebe qual URL deve ser exibida quando uma miniatura é clicada
    def mostrar_imagem(url_clicada):
        def handler(e):
            # Atualiza a propriedade src da imagem principal
            imagem_principal.src = url_clicada
            page.update()
        return handler

    # --- CRIANDO AS MINIATURAS (THUMBNAILS) DINAMICAMENTE ---
    # Em vez de criar cada miniatura "na mão", percorremos a lista de URLs
    # com um laço for, o que deixa o código reaproveitável para N imagens
    miniaturas = []
    for url in urls_imagens:
        imagem_miniatura = ft.Image(
            src=url,
            width=80,
            height=80,
            fit=ft.ImageFit.COVER,  # Miniatura quadrada e sem distorção
            border_radius=6,
        )

        # Envolvemos a miniatura em um ft.Container para poder capturar o
        # clique (ft.Image sozinho não possui evento on_click)
        miniatura_clicavel = ft.Container(
            content=imagem_miniatura,
            on_click=mostrar_imagem(url),  # Ao clicar, troca a imagem principal
            border_radius=6,
            ink=True,  # Efeito visual de "onda" ao clicar (feedback de toque)
        )

        miniaturas.append(miniatura_clicavel)

    # --- LINHA COM AS MINIATURAS ---
    linha_miniaturas = ft.Row(
        controls=miniaturas,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )

    # --- MONTAGEM DA TELA ---
    page.add(
        ft.Column(
            controls=[imagem_principal, linha_miniaturas],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )


# Ponto de entrada do aplicativo
ft.app(target=main)
