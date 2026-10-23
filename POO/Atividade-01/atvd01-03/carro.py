class Carro:
    
    def __init__(self, marca, modelo, ano):
        self.marca = marca
        self.modelo = modelo
        self.ano = ano
        
    def detalhes(self):
        return f'Carro do modelo {self.modelo} - {self.ano} da {self.marca}'
    
    def idade_carro(self, ano_atual):
        return ano_atual - self.ano