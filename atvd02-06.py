import flet as ft  # Importa a biblioteca do Flet para criar a interface visual


def main(page: ft.Page):
    # --- CONFIGURAÇÕES DA PÁGINA ---
    page.title = "Semáforo com Containers"
    page.padding = 30
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- CORES "ACESAS" E "APAGADAS" DE CADA LUZ ---
    # Guardamos as cores de cada luz quando está ativa, para reaproveitar
    # tanto na criação quanto na lógica de troca do desafio
    cor_vermelho_aceso = "red"
    cor_amarelo_aceso = "yellow"
    cor_verde_aceso = "green"
    cor_apagada = ft.Colors.GREY_900  # Cor escura para simular luz apagada

    # --- CRIANDO CADA CÍRCULO (LUZ) COMO UM ft.Container ---
    # Para deixar um Container circular: width == height, e
    # border_radius = metade do valor (aqui, 60/2 = 30)
    luz_vermelha = ft.Container(
        width=60,
        height=60,
        border_radius=30,
        bgcolor=cor_vermelho_aceso,  # Começa acesa (semáforo no estado inicial)
        margin=10,                  # Espaço entre uma luz e outra
    )
    luz_amarela = ft.Container(
        width=60,
        height=60,
        border_radius=30,
        bgcolor=cor_apagada,        # Começa apagada
        margin=10,
    )
    luz_verde = ft.Container(
        width=60,
        height=60,
        border_radius=30,
        bgcolor=cor_apagada,        # Começa apagada
        margin=10,
    )

    # --- CORPO DO SEMÁFORO ---
    # Um Container retangular preto, com uma Column dentro contendo as 3 luzes
    corpo_semaforo = ft.Container(
        content=ft.Column(
            controls=[luz_vermelha, luz_amarela, luz_verde],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        ),
        bgcolor=ft.Colors.BLACK,
        padding=15,
        border_radius=20,
        width=110,
    )

    # --- DESAFIO: BOTÃO "PRÓXIMO" QUE AVANÇA O SEMÁFORO ---
    # Lista com a sequência de estados: cada item é a luz que deve
    # ficar acesa naquele momento
    sequencia = ["vermelho", "amarelo", "verde"]
    estado_atual = {"indice": 0}  # Índice de qual luz está acesa agora

    def atualizar_luzes():
        # Primeiro, apaga todas as luzes
        luz_vermelha.bgcolor = cor_apagada
        luz_amarela.bgcolor = cor_apagada
        luz_verde.bgcolor = cor_apagada

        # Depois, acende apenas a luz correspondente ao estado atual
        luz_ativa = sequencia[estado_atual["indice"]]
        if luz_ativa == "vermelho":
            luz_vermelha.bgcolor = cor_vermelho_aceso
        elif luz_ativa == "amarelo":
            luz_amarela.bgcolor = cor_amarelo_aceso
        else:
            luz_verde.bgcolor = cor_verde_aceso

    def proxima_luz(e):
        # Avança para o próximo índice; quando chega no fim, volta ao início
        # (operador % faz esse "loop" automaticamente)
        estado_atual["indice"] = (estado_atual["indice"] + 1) % len(sequencia)
        atualizar_luzes()
        page.update()

    botao_proximo = ft.ElevatedButton(
        text="Próximo",
        on_click=proxima_luz,
    )

    # --- MONTAGEM DA TELA ---
    page.add(
        ft.Column(
            controls=[corpo_semaforo, botao_proximo],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )


# Ponto de entrada do aplicativo
ft.app(target=main)

