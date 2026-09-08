import flet as ft


# LAYOUT, ESPAÇAMENTO E LÓGICA FEITO POR MIM
# ESTILIZAÇÃO FEITA POR IA
def main(page: ft.Page):
    page.title = 'Atividade 01-02 | Contador de Cliques Personalizado'
    page.scroll = ft.ScrollMode.AUTO
    page.bgcolor = "#0A0E14"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.fonts = {
        "Poppins": "https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/Poppins-Regular.ttf"
    }
    page.theme = ft.Theme(font_family="Poppins")

    ACCENT = "#22D3EE"  
    MUTED = "#7C93A8"

    def change_value(e):
        for i in options.controls:
            if i == e.control:
                value.value += i.data

        value.update()

    layout = ft.Container(
        bgcolor="#131B24",
        width=480,
        padding=ft.Padding.symmetric(horizontal=40, vertical=48),
        border_radius=24,
        border=ft.Border.all(1, "#22303C"),
        shadow=ft.BoxShadow(
            blur_radius=40,
            color="#00000080",
            offset=ft.Offset(0, 12)
        ),
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
            controls=[
                ft.Text(  # Título
                    value='CONTADOR',
                    color=MUTED,
                    style=ft.TextStyle(
                        size=15,
                        weight=ft.FontWeight.W_500,
                        letter_spacing=2,
                    ),
                ),

                value := ft.Text(  # Valor
                    value=0,
                    size=56,
                    weight=ft.FontWeight.W_600,
                    color=ft.Colors.WHITE,
                ),

                ft.Container(height=24),

                options := ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        ft.Button(  # Botão 1
                            content=ft.Icon(
                                ft.Icons.EXPOSURE_MINUS_1,
                                color=ft.Colors.WHITE,
                            ),
                            data=-1,
                            on_click=change_value,
                            bgcolor="transparent",
                            style=ft.ButtonStyle(
                                side=ft.BorderSide(1, ACCENT),
                                shape=ft.RoundedRectangleBorder(),
                                padding=ft.Padding.all(18),
                                overlay_color=ft.Colors.with_opacity(0.08, ACCENT),
                            )
                        ),
                        ft.Button(  # Botão 2
                            content=ft.Icon(
                                ft.Icons.EXPOSURE_PLUS_1,
                                color=ft.Colors.WHITE,
                            ),
                            data=+1,
                            on_click=change_value,
                            bgcolor="transparent",
                            style=ft.ButtonStyle(
                                side=ft.BorderSide(1, ACCENT),
                                shape=ft.RoundedRectangleBorder(),
                                padding=ft.Padding.all(18),
                                overlay_color=ft.Colors.with_opacity(0.08, ACCENT),
                            )
                        )
                    ]
                )
            ]
        )
    )

    page.add(layout)


if __name__ == '__main__':
    ft.app(target=main)