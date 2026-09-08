import flet as ft

# LAYOUT E ESPAÇAMENTO FEITO POR MIM
# ESTILIZAÇÃO FEITA POR IA
def main(page: ft.Page):
    page.title = 'Atividade 01-01 | Cartão de Apresentação Pessoal'
    page.scroll = ft.ScrollMode.AUTO
    page.bgcolor = "#0E0E10"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.fonts = {
        "Poppins": "https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/Poppins-Regular.ttf"
    }
    page.theme = ft.Theme(font_family="Poppins")

    ACCENT = "#D4AF37"  
    MUTED = "#A0A0A5"
    PHOTO_SIZE = 200

    layout = ft.Container(
        bgcolor="#18181B",
        width=480,
        padding=ft.Padding.symmetric(horizontal=40, vertical=48),
        border_radius=24,
        border=ft.Border.all(1, "#2A2A2E"),
        shadow=ft.BoxShadow(
            blur_radius=40,
            color="#00000080",
            offset=ft.Offset(0, 12),
        ),
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=18,
            controls=[
                ft.Container(
                    content=ft.Image( # Imagem
                        src='img/my_photo.png',
                        width=PHOTO_SIZE,
                        height=PHOTO_SIZE,
                        fit=ft.BoxFit.COVER,
                        border_radius=ft.BorderRadius.all(PHOTO_SIZE / 2),
                    ),
                    border=ft.Border.all(2, ACCENT),
                    border_radius=PHOTO_SIZE / 2 + 4,
                    padding=4,
                ),

                ft.Container(height=10),  # Espaçamento

                ft.Text(  # Nome
                    value='Samuel Ferreira Souto',
                    size=26,
                    weight=ft.FontWeight.W_600,
                    color=ft.Colors.WHITE,
                ),

                ft.Text(  # Cargo
                    value='ESTUDANTE DE INFORMÁTICA E MÚSICA',
                    size=13,
                    color=MUTED,
                    style=ft.TextStyle(
                        letter_spacing=1.5    
                    )
                ),

                ft.Container(height=20),  # Espaçamento

                ft.Button( # Botão
                    content='Entrar em Contato',
                    color=ft.Colors.WHITE,
                    bgcolor="transparent",
                    style=ft.ButtonStyle(
                        side=ft.BorderSide(1, ACCENT),
                        shape=ft.RoundedRectangleBorder(radius=30),
                        padding=ft.Padding.symmetric(horizontal=28, vertical=16),
                        overlay_color=ft.Colors.with_opacity(0.08, ACCENT),
                    ),
                )
            ]
        )
    )

    page.add(layout)
    page.update()


if __name__ == '__main__':
    ft.app(target=main)