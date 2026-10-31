import flet as ft
from models.model_tarefa import Tarefa


# Layout da tarefa
class TarefaCard(ft.Container):

    def __init__(self, tarefa: Tarefa, on_alternar_conclusao, on_remover):
        super().__init__()
        self.tarefa = tarefa
        self.on_alternar_conclusao = on_alternar_conclusao
        self.on_remover = on_remover
        
        self.cor_fundo = "#E3F2FD"
        self.icone = ft.Icons.TASK_ALT
        self.rotulo_tipo = "Comum"

    def construir_layout(self):
        self.padding = 12
        self.border_radius = 8
        self.bgcolor = self.cor_fundo
        self.checkbox = ft.Checkbox(value=self.tarefa.concluida, on_change=self.ao_mudar_checkbox)

        if self.tarefa.concluida:
            estilo_texto = ft.TextStyle(decoration=ft.TextDecoration.LINE_THROUGH)
        else:
            estilo_texto = ft.TextStyle(decoration=ft.TextDecoration.NONE)

        self.texto_nome = ft.Text(self.tarefa.nome, expand=True, size=16, style=estilo_texto)
        self.botao_excluir = ft.IconButton(
            icon=ft.Icons.DELETE,
            icon_color=ft.Colors.RED_400,
            on_click=self.ao_clicar_excluir,
        )
        self.content = ft.Row(
            controls=[
                ft.Icon(self.icone),
                self.checkbox,
                self.texto_nome,
                ft.Container(
                    content=ft.Text(self.rotulo_tipo, size=12, weight=ft.FontWeight.W_500),
                    padding=ft.Padding.symmetric(horizontal=8, vertical=4),
                    bgcolor=ft.Colors.WHITE,
                    border_radius=4,
                ),
                ft.Text(f"+{self.tarefa.xp} XP", weight=ft.FontWeight.BOLD),
                self.botao_excluir,
            ]
        )

    def ao_mudar_checkbox(self, evento):
        novo_status = self.checkbox.value
        if novo_status:
            self.texto_nome.style = ft.TextStyle(decoration=ft.TextDecoration.LINE_THROUGH)
        else:
            self.texto_nome.style = ft.TextStyle(decoration=ft.TextDecoration.NONE)
        self.update()

        self.on_alternar_conclusao(self.tarefa, novo_status)

    def ao_clicar_excluir(self, evento):
        self.on_remover(self.tarefa, self)


# TIPOS DE TAREFAS
class TarefaComumCard(TarefaCard):
    def __init__(self, tarefa: Tarefa, on_alternar_conclusao, on_remover):
        super().__init__(tarefa, on_alternar_conclusao, on_remover)
        self.cor_fundo = "#E3F2FD"  
        self.icone = ft.Icons.TASK_ALT
        self.rotulo_tipo = "Comum"
        self.construir_layout()


class TarefaUrgenteCard(TarefaCard):
    def __init__(self, tarefa: Tarefa, on_alternar_conclusao, on_remover):
        super().__init__(tarefa, on_alternar_conclusao, on_remover)
        self.cor_fundo = "#FFCDD2"  
        self.icone = ft.Icons.WARNING_AMBER
        self.rotulo_tipo = "Urgente"
        self.construir_layout()


class TarefaEpicaCard(TarefaCard):
    def __init__(self, tarefa: Tarefa, on_alternar_conclusao, on_remover):
        super().__init__(tarefa, on_alternar_conclusao, on_remover)
        self.cor_fundo = "#FFE082"  
        self.icone = ft.Icons.STAR
        self.rotulo_tipo = "Épica ⭐"
        self.construir_layout()


# SELECIONA A TAREFA CRIADA
def criar_card_tarefa(tarefa: Tarefa, on_alternar_conclusao, on_remover) -> TarefaCard:
    if tarefa.tipo == "Urgente":
        return TarefaUrgenteCard(tarefa, on_alternar_conclusao, on_remover)
    elif tarefa.tipo == "Épica":
        return TarefaEpicaCard(tarefa, on_alternar_conclusao, on_remover)
    else:
        return TarefaComumCard(tarefa, on_alternar_conclusao, on_remover)