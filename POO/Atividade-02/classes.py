class Veiculo:

    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo
        self.ligado = False

    def ligar(self):
        self.ligado = True
        return f'Veículo Ligado!'

    def desligar(self):
        self.ligado = False
        return f'Veículo Desligado!'

    def descrever(self):
        return f'{self.marca} {self.modelo}'

class Carro(Veiculo):

    def __init__(self, marca, modelo, quantidade_portas):
        super().__init__(marca, modelo)
        self.quantidade_portas = quantidade_portas

    def descrever(self):
        return f'Carro {self.marca} {self.modelo} - {self.quantidade_portas} portas'

class Moto(Veiculo):

    def __init__(self, marca, modelo, cilindradas):
        super().__init__(marca, modelo)
        self.cilindradas = cilindradas

    def empinar(self):
        if self.ligado == True:
            return f'Moto {self.marca} {self.modelo} - {self.cilindradas} cilindradas empinando!'
        elif self.ligado == False:
            return f'Moto não pode empinar pois está desligada!'