import flet as ft


class DespesaCard(ft.Container):
    
    def __init__(self, descricao: str, valor: float, on_remover):
        super().__init__()
        self.descricao = descricao
        self.valor = valor
        self.on_remover = on_remover
        
        self.padding = 12
        self.border_radius = 8
        self.bgcolor = '#C8E6C9'
        
        self.texto_descricao = ft.Text(
            self.descricao,
            expand=True,
            size=16
        )
        self.texto_valor = ft.Text(
            f'R$ {self.valor:.2f}',
            size=16,
            weight=ft.FontWeight.BOLD
        )
        self.botao_excluir = ft.IconButton(
            icon=ft.Icons.DELETE,
            icon_color=ft.Colors.RED_400,
            on_click=self.ao_excluir
        )
        
        # LAYOUT
        self.content = ft.Row(
            controls=[
                ft.Icon(ft.Icons.SHOPPING_BASKET),
                self.texto_descricao,
                self.texto_valor,
                self.botao_excluir
            ]
        )
        
    # Exluir classe
    def ao_excluir(self, e):
        self.on_remover(self)