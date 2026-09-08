import flet as ft


# LAYOUT E ESPAÇAMENTO FEITO POR MIM
# ESTILIZAÇÃO FEITA POR IA
def main(page: ft.Page):
    page.title = 'Atividade 01-04 | '
    page.scroll = ft.ScrollMode.AUTO
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.fonts = {
        "Poppins": "https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/Poppins-Regular.ttf"
    }
    page.theme = ft.Theme(font_family="Poppins")

    THEMES = {
        "light": {
            "page_bg": "#FFFFFF",      
            "card_bg": "#F2F2F5",
            "border": "#DADAE0",
            "text": "#1A1A1E",
            "muted": "#6B6B75",
            "accent": "#6C5CE7",
        },
        "dark": {
            "page_bg": "#000000",     
            "card_bg": "#18181B",
            "border": "#2A2A2E",
            "text": "#FFFFFF",
            "muted": "#A0A0A5",
            "accent": "#D4AF37",
        },
    }

    # IA
    def apply_theme(name):
        t = THEMES[name]
        page.bgcolor = t["page_bg"]
        layout.bgcolor = t["card_bg"]
        layout.border = ft.Border.all(1, t["border"])
        title.color = t["muted"]

        for btn in [btn_dog, btn_cat]:
            btn.style.side = ft.BorderSide(1, t["accent"])
            btn.style.color = t["text"]
            btn.style.overlay_color = ft.Colors.with_opacity(0.08, t["accent"])

        btn_theme.style.side = ft.BorderSide(1, t["accent"])
        btn_theme.style.color = t["text"]
        btn_theme.style.overlay_color = ft.Colors.with_opacity(0.08, t["accent"])

    # EU
    def change_theme(e):
        if img.src == 'img/cachorro.jpg' or img.src == 'img/gato.jpg':
            if page.theme_mode == ft.ThemeMode.LIGHT:
                page.theme_mode = ft.ThemeMode.DARK
                btn_theme.content = ft.Icon(ft.Icons.LIGHT_MODE)
                apply_theme("dark")
            else:
                page.theme_mode = ft.ThemeMode.LIGHT
                btn_theme.content = ft.Icon(ft.Icons.DARK_MODE)
                apply_theme("light")
        else:
            if page.theme_mode == ft.ThemeMode.LIGHT:
                page.theme_mode = ft.ThemeMode.DARK
                img.src = 'img/ponto_de_interrogacao_dark.jpg'
                btn_theme.content = ft.Icon(ft.Icons.LIGHT_MODE)
                apply_theme("dark")
            else:
                page.theme_mode = ft.ThemeMode.LIGHT
                img.src = 'img/ponto_de_interrogacao_light.jpg'
                btn_theme.content = ft.Icon(ft.Icons.DARK_MODE)
                apply_theme("light")

        page.update()

    # EU
    def change_image(e):
        for i in options.controls:
            if i == e.control:
                if i.data == 'dog':
                    img.src = 'img/cachorro.jpg'
                elif i.data == 'cat':
                    img.src = 'img/gato.jpg'

        img.update()

    # IA
    title = ft.Text(
        value='ESCOLHA UM ANIMAL',
        style=ft.TextStyle(size=13, weight=ft.FontWeight.W_500, letter_spacing=2),
    )

    btn_theme = ft.Button(
        content=ft.Icon(ft.Icons.DARK_MODE),
        on_click=change_theme,
        bgcolor="transparent",
        style=ft.ButtonStyle(
            shape=ft.CircleBorder(),
            padding=ft.Padding.all(14),
        ),
    )

    btn_dog = ft.Button(
        content=ft.Row(
            spacing=6,
            tight=True,
            controls=[ft.Icon(ft.Icons.PETS), ft.Text('Cachorro')],
        ),
        on_click=change_image,
        data='dog',
        bgcolor="transparent",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=30),
            padding=ft.Padding.symmetric(horizontal=20, vertical=14),
        ),
    )

    btn_cat = ft.Button(
        content=ft.Row(
            spacing=6,
            tight=True,
            controls=[ft.Icon(ft.Icons.PETS), ft.Text('Gato')],
        ),
        on_click=change_image,
        data='cat',
        bgcolor="transparent",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=30),
            padding=ft.Padding.symmetric(horizontal=20, vertical=14),
        ),
    )

    layout = ft.Container(
        width=480,
        padding=ft.Padding.symmetric(horizontal=40, vertical=48),
        border_radius=24,
        shadow=ft.BoxShadow(
            blur_radius=40,
            color="#00000040",
            offset=ft.Offset(0, 12)
        ),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=16,
            controls=[
                ft.Row(alignment=ft.MainAxisAlignment.START, controls=[btn_theme]),

                title,

                img := ft.Image(
                    src='img/ponto_de_interrogacao_light.jpg',
                    width=220,
                    height=220,
                    fit=ft.BoxFit.CONTAIN,
                ),

                options := ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=16,
                    controls=[btn_dog, btn_cat],
                )
            ]
        )
    )

    page.add(layout)
    apply_theme("light")
    page.update()


if __name__ == '__main__':
    ft.app(target=main)