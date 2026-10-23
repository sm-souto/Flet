from classes import Carro
from classes import Moto


carro = Carro("Toyota", "Corolla", 4)
moto = Moto("Honda", "CB 500", 500)

print(carro.descrever())
print()
print(moto.ligar())
print(moto.empinar())
print(moto.desligar())
print(moto.empinar())  