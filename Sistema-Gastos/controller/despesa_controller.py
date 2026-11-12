from models.despesa import Despesa
from database.connection import get_client


class DespesaController:
    TABLE_NAME = "despesas"

    def __init__(self):
        self._client = get_client()

    def listar_despesas(self) -> list[Despesa]:
        resposta = (
            self._client
            .table(self.TABLE_NAME)
            .select("*")
            .order("id", desc=True)
            .execute()
        )
        despesas = []
        for item in resposta.data:
            despesas.append(Despesa.from_dict(item))
        return despesas

    def adicionar_despesa(self, descricao: str, valor_texto: str) -> Despesa:
        descricao = descricao.strip()
        if not descricao:
            raise ValueError("A descrição não pode estar vazia.")

        valor_texto = valor_texto.strip().replace(",", ".")
        if not valor_texto:
            raise ValueError("O valor não pode estar vazio.")

        valor = float(valor_texto)
        if valor <= 0:
            raise ValueError("O valor deve ser maior que zero.")

        nova_despesa = Despesa(descricao=descricao, valor=valor)
        resposta = (
            self._client
            .table(self.TABLE_NAME)
            .insert(nova_despesa.to_dict())
            .execute()
        )

        return Despesa.from_dict(resposta.data[0])

    def remover_despesa(self, despesa_id: int) -> None:
        (
            self._client
            .table(self.TABLE_NAME)
            .delete()
            .eq("id", despesa_id)
            .execute()
        )

    def calcular_total(self, despesas: list[Despesa]) -> float:
        total = 0.0
        for despesa in despesas:
            total += despesa.valor
        return total