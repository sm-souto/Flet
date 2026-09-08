import flet as ft


# LAYOUT, ESPAÇAMENTO E LÓGICA FEITO POR MIM
# ESTILIZAÇÃO FEITA POR IA
def main(page: ft.Page):
    page.title = 'Atividade 01-03 | Mensagem de Boas-Vindas Dinâmica'
    page.scroll = ft.ScrollMode.AUTO
    page.bgcolor = "#0A140F"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.fonts = {
        "Poppins": "https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/Poppins-Regular.ttf"
    }
    page.theme = ft.Theme(font_family="Poppins")

    ACCENT = "#34D399"  # verde-esmeralda — único ponto de destaque
    MUTED = "#7FA895"


    def send_message():
        if not name.value: 
            saudacao.value = 'Olá!'
        else:
            saudacao.value = f'Olá, {name.value}! Seja bem-vindo(a) ao Flet!'
        
        saudacao.update()
        

    layout = ft.Container(
        bgcolor="#0F1D17",
        width=480,
        padding=ft.Padding.symmetric(horizontal=40, vertical=48),
        border_radius=24,
        border=ft.Border.all(1, "#1E3229"),
        shadow=ft.BoxShadow(
            blur_radius=40,
            color="#00000080",
            offset=ft.Offset(0, 12)
        ),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=16,
            controls=[
                name := ft.TextField(
                    label='Digite seu nome',
                    color=ft.Colors.WHITE,
                    label_style=ft.TextStyle(color=MUTED),
                    border_color="#1E3229",
                    focused_border_color=ACCENT,
                    cursor_color=ACCENT,
                    bgcolor="transparent",
                    border_radius=12,
                ),

                ft.Button(
                    content='Enviar Saudação',
                    on_click=send_message,
                    color=ft.Colors.WHITE,
                    bgcolor="transparent",
                    style=ft.ButtonStyle(
                        side=ft.BorderSide(1, ACCENT),
                        shape=ft.RoundedRectangleBorder(radius=30),
                        padding=ft.Padding.symmetric(horizontal=28, vertical=16),
                        overlay_color=ft.Colors.with_opacity(0.08, ACCENT),
                    ),
                ),

                ft.Divider(color="#1E3229"),

                saudacao := ft.Text(
                    color=ft.Colors.WHITE,
                    size=16,
                    text_align=ft.TextAlign.CENTER,
                )
            ]
        )
    )

    page.add(layout)
    page.update()


if __name__ == '__main__':
    ft.app(target=main)