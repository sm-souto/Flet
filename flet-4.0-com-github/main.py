import flet as ft

# LAYOUT E ESPAÇAMENTO FEITO POR MIM
# ESTILIZAÇÃO FEITA POR IA
def main(page: ft.Page):
    page.title = 'Atividade Prática | Flet com GitHub'
    page.scroll = ft.ScrollMode.AUTO
    page.bgcolor = "#0E0E10"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 0
    page.window.width = 900
    page.window.height = 1000
    page.window.min_width = 600
    page.window.min_height = 800
    page.window.resizable = True
    page.window.center()
    page.fonts = {
        "Poppins": "https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/Poppins-Regular.ttf"
    }
    page.theme = ft.Theme(font_family="Poppins")


    layout = ft.Container(
        width=700,
        padding=ft.Padding.symmetric(horizontal=60, vertical=70),
        bgcolor="#18181B",
        border_radius=24,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=30,
            color="#4D000000",
            offset=ft.Offset(0, 10),
        ),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=18,
            controls=[

                ft.Text(
                    value='Samuel Ferreira Souto',
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color="#FFFFFF",
                    text_align=ft.TextAlign.CENTER,
                ),

                ft.Text(
                    value='Técnico em Informática — Turma 2º Ano (IFNMG)\n'
                          'Estudar Python é sensacional!',
                    size=14,
                    color="#B5B5B8",
                    text_align=ft.TextAlign.CENTER,
                ),

                ft.Container(
                    content=ft.Image(
                        src='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ8K0IRTAptDBlg6uU9KYfA703RA5QoAJ6k2Vb7jtXY6A&s=10',
                        width=120,
                        height=120,
                        fit=ft.BoxFit.COVER,
                        border_radius=100,
                    ),
                    border=ft.Border.all(3, "#6C63FF"),
                    border_radius=100,
                    padding=4,
                ),
                
                ft.Container(height=8),

                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=16,
                    controls=[
                        ft.ElevatedButton(
                            content='Meu Perfil',
                            icon=ft.Icons.PERSON,
                            bgcolor="#6C63FF",
                            color="#FFFFFF",
                            style=ft.ButtonStyle(
                                padding=ft.Padding.symmetric(horizontal=20, vertical=14),
                                shape=ft.RoundedRectangleBorder(radius=10),
                            ),
                        ),
                        ft.ElevatedButton(
                            content='Projetos',
                            icon=ft.Icons.CODE,
                            bgcolor="#1E1E22",
                            color="#FFFFFF",
                            style=ft.ButtonStyle(
                                padding=ft.Padding.symmetric(horizontal=20, vertical=14),
                                shape=ft.RoundedRectangleBorder(radius=10),
                                side=ft.BorderSide(1, "#3A3A3F"),
                            ),
                        ),
                    ],
                ),
            ],
        ),
    )

    page.add(layout)
    page.update()


if __name__ == '__main__':
    ft.app(target=main)