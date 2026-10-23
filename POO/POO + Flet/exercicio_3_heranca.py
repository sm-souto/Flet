import flet as ft


class TarefaItem(ft.Container):

    def __init__(self, nome: str, on_remover, on_atualizar_xp):
        super().__init__()
        self.nome = nome
        self.on_remover = on_remover
        self.on_atualizar_xp = on_atualizar_xp

        self.xp = 10
        self.cor_fundo = "#E3F2FD"
        self.icone = ft.Icons.TASK_ALT

        self.padding = 12
        self.border_radius = 8
        self.bgcolor = self.cor_fundo

        self.checkbox = ft.Checkbox(on_change=self.ao_marcar)
        self.texto = ft.Text(self.nome, expand=True, size=16)
        self.botao_excluir = ft.IconButton(
            icon=ft.Icons.DELETE,
            icon_color=ft.Colors.RED_400,
            on_click=self.ao_excluir,
        )

        self.montar_layout()

    def montar_layout(self):

        self.content = ft.Row(
            controls=[
                ft.Icon(self.icone),
                self.checkbox,
                self.texto,
                ft.Text(f"+{self.xp} XP", weight=ft.FontWeight.BOLD),
                self.botao_excluir,
            ]
        )

    def ao_marcar(self, evento):

        if self.checkbox.value:
            self.texto.style = ft.TextStyle(decoration=ft.TextDecoration.LINE_THROUGH)
            self.on_atualizar_xp(self.xp)
        else:
            self.texto.style = ft.TextStyle(decoration=ft.TextDecoration.NONE)
            self.on_atualizar_xp(-self.xp)
        self.update()

    def ao_excluir(self, evento):

        if self.checkbox.value:
            self.on_atualizar_xp(-self.xp)
        self.on_remover(self)


class TarefaUrgente(TarefaItem):

    def __init__(self, nome: str, on_remover, on_atualizar_xp):
        super().__init__(nome, on_remover, on_atualizar_xp)

    
        self.xp = 30
        self.cor_fundo = "#FFCDD2"  
        self.icone = ft.Icons.WARNING_AMBER

        self.bgcolor = self.cor_fundo
        self.montar_layout()  

# ==========================================
#           INTERFACE PRINCIPAL
# ==========================================

def main(page: ft.Page):
    page.title = "Exercício 3: Herança com TarefaUrgente"
    page.theme_mode = ft.ThemeMode.LIGHT

    xp_total = 0
    xp_texto = ft.Text(f"XP Total: {xp_total}", size=22, weight=ft.FontWeight.BOLD)
    lista_tarefas = ft.Column(spacing=8)
    input_nome = ft.TextField(label="Nova Tarefa", expand=True)

    def atualizar_xp(pontos):
        nonlocal xp_total
        xp_total += pontos
        xp_texto.value = f"XP Total: {xp_total}"
        page.update()

    def remover_tarefa(tarefa_item):
        lista_tarefas.controls.remove(tarefa_item)
        page.update()

    def adicionar_tarefa(evento):
        if not input_nome.value or not input_nome.value.strip():
            return

        nova_tarefa = TarefaItem(
            nome=input_nome.value.strip(),
            on_remover=remover_tarefa,
            on_atualizar_xp=atualizar_xp,
        )
        lista_tarefas.controls.append(nova_tarefa)
        input_nome.value = ""
        page.update()

    def adicionar_urgente(evento):
        if not input_nome.value or not input_nome.value.strip():
            return

        nova_tarefa = TarefaUrgente(
            nome=input_nome.value.strip(),
            on_remover=remover_tarefa,
            on_atualizar_xp=atualizar_xp,
        )
        lista_tarefas.controls.append(nova_tarefa)
        input_nome.value = ""
        page.update()

    linha_formulario = ft.Row(
        controls=[
            input_nome,
            ft.Button(content="Adicionar", on_click=adicionar_tarefa),
            ft.Button(content="Adicionar Urgente", on_click=adicionar_urgente),
        ]
    )

    page.add(
        ft.Column(
            controls=[
                ft.Text("Exercício 3: Herança com TarefaUrgente", size=24, weight=ft.FontWeight.BOLD),
                xp_texto,
                linha_formulario,
                ft.Divider(),
                lista_tarefas,
            ],
            spacing=15,
        )
    )


if __name__ == "__main__":
    ft.run(main)