import flet as ft  # Importa a biblioteca do Flet para criar a interface visual


def main(page: ft.Page):
    # --- CONFIGURAÇÕES DA PÁGINA ---
    page.title = "Tela de Login"
    page.padding = 30
    page.window.width = 380         # Largura da janela (ideal para formulário de login)
    page.window.height = 420        # Altura da janela
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # --- CAMPO DE USUÁRIO ---
    # ft.TextField é o campo de entrada de texto padrão do Flet
    campo_usuario = ft.TextField(
        label="Usuário",           # Texto exibido dentro/acima do campo
        border=ft.InputBorder.OUTLINE,
        width=300,
    )

    # --- CAMPO DE SENHA ---
    # password=True esconde o texto digitado com pontinhos/asteriscos
    # can_reveal_password=True adiciona um ícone de "olho" que permite
    # mostrar a senha temporariamente
    campo_senha = ft.TextField(
        label="Senha",
        password=True,
        can_reveal_password=True,
        border=ft.InputBorder.OUTLINE,
        width=300,
    )

    # --- TEXTO DE STATUS ---
    # Começa mostrando uma mensagem neutra, aguardando a ação do usuário
    texto_status = ft.Text(
        "Status: Aguardando login...",
        color="grey700",
    )

    # --- FUNÇÃO EXECUTADA AO CLICAR NO BOTÃO "ENTRAR" ---
    def fazer_login(e):
        # .value pega o texto que o usuário digitou em cada campo
        usuario = campo_usuario.value
        senha = campo_senha.value

        # DESAFIO: validação simples -> senha precisa ter mais de 6 caracteres
        if len(senha) <= 6:
            # Se a validação falhar, mostra erro em vermelho no texto de status
            texto_status.value = "Erro: a senha deve ter mais de 6 caracteres."
            texto_status.color = "red"
        elif usuario == "":
            texto_status.value = "Erro: informe o usuário."
            texto_status.color = "red"
        else:
            # Se passou pelas validações, mostra sucesso em verde
            texto_status.value = "Login bem-sucedido!"
            texto_status.color = "green"

        # page.update() é obrigatório: sem ele, a mudança de valor não
        # aparece na tela, pois o Flet só redesenha quando mandamos
        page.update()

    # --- BOTÃO "ENTRAR" ---
    botao_entrar = ft.ElevatedButton(
        on_click=fazer_login,  # Aponta para a função criada acima
        width=150,
    )

    # --- MONTAGEM DA TELA ---
    # Column empilha verticalmente: usuário, senha, botão e status
    page.add(
        ft.Column(
            controls=[
                campo_usuario,
                campo_senha,
                botao_entrar,
                texto_status,
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )


# Ponto de entrada do aplicativo
ft.app(target=main)