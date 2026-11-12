class Despesa:
    def __init__(self, descricao: str, valor: float, id: int = None):
        self.id = id
        self.descricao = descricao
        self.valor = valor

    def to_dict(self) -> dict:
        return {
            "descricao": self.descricao,
            "valor": self.valor,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Despesa":
        return cls(
            id=data.get("id"),
            descricao=data.get("descricao", ""),
            valor=float(data.get("valor", 0.0)),
        )