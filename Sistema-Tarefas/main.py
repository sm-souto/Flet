import flet as ft
from database.connect_supabase import connect_supabase, verificar_tabela_tarefas
from models.sql_tarefa import SQL_Tarefa
from controllers.controle_tarefa import ControleTarefa


def main(page: ft.Page):
    page.title = "Gerenciador de Tarefas Gamificado (MVC + Supabase)"
    page.theme_mode = ft.ThemeMode.LIGHT

    # CONEXÃO COM SUPABASE
    try:
        cliente_supabase = connect_supabase()
        verificar_tabela_tarefas(cliente_supabase)
    except Exception as erro_conexao:
        exibir_tela_erro_configuracao(page, str(erro_conexao))
        return

    sql_tarefas = SQL_Tarefa(cliente_supabase)

    # INTERFACE PRINCIPAL
    page.clean()

    texto_xp = ft.Text("XP Total: 0", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_900)
    coluna_tarefas = ft.Column(spacing=8)

    input_nome = ft.TextField(label="Nova Tarefa", expand=True)
    dropdown_tipo = ft.Dropdown(
        label="Dificuldade / Tipo",
        options=[
            ft.DropdownOption(key="Comum", text="Comum (+10 XP)"),
            ft.DropdownOption(key="Urgente", text="Urgente (+20 XP)"),
            ft.DropdownOption(key="Épica", text="Épica (+50 XP)"),
        ],
        value="Comum",
        width=200,
    )

    # CONEXÃO COM CONTROLLER
    controller = ControleTarefa(
        page=page,
        sql_tarefa=sql_tarefas,
        coluna_tarefas=coluna_tarefas,
        texto_xp=texto_xp,
    )

    def ao_clicar_adicionar(evento):
        nome_digitado = input_nome.value
        tipo_selecionado = dropdown_tipo.value
        sucesso = controller.adicionar_nova_tarefa(nome_digitado, tipo_selecionado)
        if sucesso:
            input_nome.value = ""
            page.update()

    botao_adicionar = ft.Button(content="Adicionar Tarefa", on_click=ao_clicar_adicionar)

    linha_formulario = ft.Row(
        controls=[
            input_nome,
            dropdown_tipo,
            botao_adicionar,
        ]
    )

    # MÉTODO PADRÃO - PÁGINA DO FLET 
    page.add(
        ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.CLOUD_DONE, color=ft.Colors.GREEN_600, size=28),
                        ft.Text("Tarefas com MVC + Supabase", size=26, weight=ft.FontWeight.BOLD),
                    ]
                ),
                ft.Text("Dados persistidos diretamente na nuvem (PostgreSQL) com arquitetura MVC."),
                texto_xp,
                linha_formulario,
                ft.Divider(),
                coluna_tarefas,
            ],
            spacing=15,
        )
    )

    controller.carregar_tarefas_iniciais()


if __name__ == "__main__":
    ft.run(main)