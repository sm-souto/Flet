import flet as ft


def main(page: ft.Page):
    # Page Configs
    page.title = 'Atividade 03 | Card E-Commerce'
    page.bgcolor = ft.Colors.BLACK
    page.scroll = ft.ScrollMode.AUTO
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER

    # FUNCTIONS to use
    def change_main_image(e):
        for i, element in enumerate(options.controls):
            if element == e.control:
                element.opacity = 1
                main_image.src = image_src[i].src
            else:
                element.opacity = 0.5
                
        main_image.update()
        options.update()

    # VARIABLES to use
    # Lista de imagens
    image_src = [ # Proriedade de lista .Image dentro de .Container
        ft.Image(src='img/poltrona_amarela.jpg'), 
        ft.Image(src='img/poltrona_amarela_frente.jpg'),
        ft.Image(src='img/poltrona_cinza.jpg')
    ] 

    product_images = ft.Container( # Imagens - LEFT
        # Small Screen; # Medium Screen
        col={'xs': 12, 'md': 6}, # RESPONSIVIDADE
        bgcolor=ft.Colors.WHITE,
        padding=ft.Padding.all(30),
        aspect_ratio=9/16,
        content=ft.Column( # Imagens em coluna
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[     #Lorus
                main_image := ft.Image(
                    src=image_src[0].src
                ),
                options := ft.Row( # Pequenas imagens em linha
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Container( # element. 0
                            image_src[0], # *Artifício
                            width=80,
                            height=80,
                            opacity=1,
                            on_click=change_main_image # Evento ao clicar
                        ),

                        ft.Container( # element. 1 
                            image_src[1],
                            width=80,
                            height=80,
                            opacity=0.5,
                            on_click=change_main_image
                        ),
                        
                        ft.Container( # element. 2
                            image_src[2],
                            width=80,
                            height=80,
                            opacity=0.5,
                            on_click=change_main_image
                        )
                    ]
                )
            ]
        )
    )
    
    product_details = ft.Container( # Textos, Interações e Estilização - RIGHT
        # Small Screen; # Medium Screen
        col={'xs': 12, 'md': 6}, # RESPONSIVIDADE
        padding=ft.Padding.all(30),
        bgcolor=ft.Colors.BLACK87, # Opacity: 87
        aspect_ratio=9/16,
        content=ft.Column(
            controls=[
                ft.Text(
                    value='CADEIRAS',
                    color=ft.Colors.AMBER,
                    weight=ft.FontWeight.BOLD # Negrito
                ),
                
                ft.Text(
                    value='Poltrona Amarela Moderna',
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD,
                    size=30
                ),
                
                ft.Text(
                    value='Sala de Estar',
                    color=ft.Colors.GREY,
                    italic=True # Itálico
                ),
                
                ft.ResponsiveRow(
                    columns=12, # Tamanho Padrão
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            col={'xs': 12, 'sm': 6}, # Número de colunas virtuais
                            value='R$ 399',
                            color=ft.Colors.WHITE,
                            size=30
                        ),
                        
                        ft.Row(
                            col={'xs': 12, 'sm': 6},
                            spacing=5, # "Margin"
                            wrap=False,
                            controls=[
                                ft.Icon( # Icon padronizado do FLET
                                    ft.Icons.STAR,          # Symbol de Iteração
                                    color=ft.Colors.AMBER if _ < 4 else ft.Colors.WHITE # Condicional da Iteração,
                                ) for _ in range(5) # Iteração de .Icon 5x (5 Estrelas)
                            ]
                        )
                    ]
                ),
                
                ft.Tabs( # Abas
                    selected_index=0,
                    length=2,
                    content=ft.Column(
                        controls=[
                            ft.TabBar( # Barra de Navegação da Aba
                                indicator_color=ft.Colors.AMBER,
                                label_color=ft.Colors.AMBER,
                                unselected_label_color=ft.Colors.GREY, 
                                tabs=[
                                    ft.Tab(label='Descrição'), # Título da Aba
                                    ft.Tab(label='Detalhes') # Título da outra Aba
                                ]
                            ),
                            ft.TabBarView( # Texto dentro das Abas
                                height=150, 
                                controls=[
                                    ft.Container(
                                        padding=ft.Padding.all(10),
                                        content=ft.Text( # Descrição
                                            value='A Poltrona Decorativa Cadeira Reforçada Opala Bege'
                                            ' Cor Amarelo Desenho Do Tecido Suede é perfeita para criar'
                                            ' um ambiente moderno e aconchegante na sua casa. Com seu'
                                            ' design retrô e cor amarela vibrante.',
                                            color=ft.Colors.GREY
                                        )
                                    ),
                                    ft.Container(
                                        padding=ft.Padding.all(10),
                                        content=ft.Text( # Detalhes
                                            value='Dimensões 0.8m de largura, 0.9m de altura e 0.76m de profundidade.'
                                            '\n \nMaterial dos pés: Eucalipto.',
                                            color=ft.Colors.GREY
                                        )
                                    )
                                ]
                            )
                        ]
                    )
                ),
                
                ft.ResponsiveRow(
                    columns=12,
                    controls=[
                        ft.Dropdown( # Etiqueta de escolha de options
                            col=6,
                            label='Cor',
                            label_style=ft.TextStyle(color=ft.Colors.WHITE, size=16),
                            border_color=ft.Colors.GREY,
                            border_width=0.5,
                            options=[
                                ft.DropdownOption(text='Amarelo'),
                                ft.DropdownOption(text='Vermelho'),
                                ft.DropdownOption(text='Azul')
                            ]
                        ),
                        ft.Dropdown(
                            col=6,
                            label='Quantidade',
                            label_style=ft.TextStyle(color=ft.Colors.WHITE, size=16),
                            border_color=ft.Colors.GREY,
                            border_width=0.5,
                            options=[                                  # Iteração na lista
                                ft.DropdownOption(text=f'{num} unid.') for num in range(1, 11)
                            ]
                        )
                    ]
                ),
                
                ft.Container(expand=True), # Container vazio para jogar botões para baixo
                
                ft.ElevatedButton( # / ft.Button() é o Botão
                    width=900,
                    content='Adicionar a lista de desejos',
                    style=ft.ButtonStyle( # Vários estilos personalizáveis
                        padding=ft.Padding.all(20), # do content até a borda (espaçamento interno)
                        side={ # Borda e Espessura
                            ft.ControlState.DEFAULT: ft.BorderSide(width=2, color=ft.Colors.WHITE)
                        },
                        bgcolor={ # Com cursor em cima
                            ft.ControlState.HOVERED: ft.Colors.WHITE
                        },
                        color={ # Sem cursor em cima
                            ft.ControlState.DEFAULT: ft.Colors.WHITE,
                            ft.ControlState.HOVERED: ft.Colors.BLACK
                        }
                    )
                ),
                
                ft.ElevatedButton( # / ft.Button() é o Botão
                    width=900,
                    content='Adicionar ao carrinho',
                    style=ft.ButtonStyle( # Vários estilos personalizáveis
                        padding=ft.Padding.all(20), # do content até a borda (espaçamento interno)
                        side={ # Borda e Espessura
                            ft.ControlState.DEFAULT: ft.BorderSide(width=2, color=ft.Colors.AMBER)
                        },
                        bgcolor={ # Com cursor em cima
                            ft.ControlState.DEFAULT: ft.Colors.AMBER,
                            ft.ControlState.HOVERED: ft.Colors.AMBER_ACCENT_200
                        },
                        color={ # Sem cursor em cima
                            ft.ControlState.DEFAULT: ft.Colors.BLACK
                        }
                    )
                )
            ]
        )
    )

#---------------------------------------------------------------------------------------------------------------------------
    # APLICAÇÃO
    # Layout Principal
    layout = ft.Container( #Container Principal
        width=900,
        margin=ft.Margin.all(30),
        shadow=ft.BoxShadow(blur_radius=300, color=ft.Colors.CYAN),
        content=ft.ResponsiveRow( # Content LADO A LADO
            columns=12, # 2 Colunas 
            spacing=0, # Margem entre as duas colunas
            run_spacing=0, # Margem entre as duas colunas verticalmente
            controls=[
                product_images,
                product_details
            ]
        )
    )

    page.add(layout)


if __name__ == '__main__':
    ft.app(target=main)