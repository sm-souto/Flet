class Tarefa:
    
    def __init__(self, nome: str, tipo: str = "Comum", xp: int = 10, concluida: bool = False, id_tarefa: int = None):
        self.id = id_tarefa
        self.nome = nome
        self.tipo = tipo
        self.xp = xp
        self.concluida = concluida
        
    def alterar_conclusao(self):
        if self.concluida:
            self.concluida = False
        else:
            self.concluida = True
            
    def para_dicionario(self):
        dados = {'nome':self.nome, 'tipo':self.tipo, 'xp':self.xp, 'concluida':self.concluida}
        if self.id is not None:
            dados['id'] = self.id
        
        return dados
    
    @staticmethod
    def de_dicionario(dados: dict):
        return Tarefa(
            id_tarefa = dados.get('id'),
            nome = dados.get('nome', ''),
            tipo = dados.get('tipo', 'Comum'),
            xp = dados.get('xp', 10),
            concluida = dados.get('concluida', False)
        )