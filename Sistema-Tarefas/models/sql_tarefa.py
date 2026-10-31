from models.model_tarefa import Tarefa
from supabase import Client

# Classe de consultas padrão do BD
class SQL_Tarefa:

    def __init__(self, cliente_supabase: Client, nome_tabela: str = "tarefas"):
        self.cliente = cliente_supabase
        self.tabela = nome_tabela

    def listar_todas(self):
        try:
            resposta = self.cliente.table(self.tabela).select("*").order("id").execute()
            linhas = resposta.data
            lista_objetos = []
            for item in linhas:
                tarefa = Tarefa.de_dicionario(item)
                lista_objetos.append(tarefa)
            return lista_objetos
        except Exception as erro:
            print("Erro ao listar tarefas do banco:", erro)
            raise erro

    def listar_por_id(self, id_tarefa: int):
        try:
            resposta = self.cliente.table(self.tabela).select("*").eq("id", id_tarefa).execute()
            if resposta.data and len(resposta.data) > 0:
                primeiro_registro = resposta.data[0]
                return Tarefa.de_dicionario(primeiro_registro)
            return None
        except Exception as erro:
            print(f"Erro ao buscar tarefa id {id_tarefa}:", erro)
            raise erro

    def inserir(self, tarefa: Tarefa):
        try:
            dados = {
                "nome": tarefa.nome,
                "tipo": tarefa.tipo,
                "xp": tarefa.xp,
                "concluida": tarefa.concluida,
            }
            resposta = self.cliente.table(self.tabela).insert(dados).execute()
            if resposta.data and len(resposta.data) > 0:
                novo_id = resposta.data[0].get("id")
                tarefa.id = novo_id
            return tarefa
        except Exception as erro:
            print("Erro ao inserir tarefa:", erro)
            raise erro

    def atualizar_status(self, id_tarefa: int, concluida: bool):
        try:
            resposta = self.cliente.table(self.tabela).update({"concluida": concluida}).eq("id", id_tarefa).execute()
            return resposta.data
        except Exception as erro:
            print(f"Erro ao atualizar status da tarefa id {id_tarefa}:", erro)
            raise erro

    def excluir(self, id_tarefa: int):
        try:
            resposta = self.cliente.table(self.tabela).delete().eq("id", id_tarefa).execute()
            return resposta.data
        except Exception as erro:
            print(f"Erro ao excluir tarefa id {id_tarefa}:", erro)
            raise erro