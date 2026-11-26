import math
from dataclasses import dataclass


@dataclass
class Category:
    """Representa uma categoria de produtos na tabela public.categorias."""

    id: str
    user_id: str
    nome: str
    descricao: str = ""
    criado_em: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> "Category":
        return cls(
            id=str(data.get("id", "")),
            user_id=str(data.get("user_id", "")),
            nome=str(data.get("nome", "")),
            descricao=str(data.get("descricao", "") or ""),
            criado_em=str(data.get("criado_em", "") or ""),
        )


@dataclass
class Product:
    """Representa um item do cardapio na tabela public.produtos."""

    id: str
    user_id: str
    categoria_id: str
    nome: str
    descricao: str
    preco: float
    disponivel: bool = True
    criado_em: str = ""
    categoria_nome: str = ""

    @classmethod
    def from_dict(cls, data: dict, category_map: dict[str, str] | None = None) -> "Product":
        cat_id = str(data.get("categoria_id", ""))
        cat_nome = ""
        if category_map and cat_id in category_map:
            cat_nome = category_map[cat_id]
        elif isinstance(data.get("categorias"), dict):
            cat_nome = str(data["categorias"].get("nome", ""))

        return cls(
            id=str(data.get("id", "")),
            user_id=str(data.get("user_id", "")),
            categoria_id=cat_id,
            nome=str(data.get("nome", "")),
            descricao=str(data.get("descricao", "") or ""),
            preco=float(data.get("preco", 0.0)),
            disponivel=bool(data.get("disponivel", True)),
            criado_em=str(data.get("criado_em", "") or ""),
            categoria_nome=cat_nome,
        )


def format_brl(value: float) -> str:
    """Formata um valor numerico no padrao monetario brasileiro."""
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def validate_category_data(nome: str, descricao: str) -> tuple[bool, str]:
    """Valida dados de categoria antes de gravar no Supabase."""
    nome_limpo = (nome or "").strip()
    desc_limpa = (descricao or "").strip()

    if len(nome_limpo) < 2 or len(nome_limpo) > 60:
        return False, "O nome da categoria deve ter entre 2 e 60 caracteres."
    if len(desc_limpa) > 200:
        return False, "A descrição da categoria deve ter no máximo 200 caracteres."
    return True, ""


def validate_product_data(
    nome: str,
    descricao: str,
    preco_texto: str,
    categoria_id: str,
) -> tuple[bool, str, float | None]:
    """Valida os campos de um produto do cardapio antes de enviar ao Supabase."""
    nome_limpo = (nome or "").strip()
    desc_limpa = (descricao or "").strip()
    cat_limpa = (categoria_id or "").strip()

    if len(nome_limpo) < 2 or len(nome_limpo) > 80:
        return False, "O nome do produto deve ter entre 2 e 80 caracteres.", None
    if len(desc_limpa) > 250:
        return False, "A descrição do produto deve ter no máximo 250 caracteres.", None
    if not cat_limpa:
        return False, "Selecione uma categoria válida para o produto.", None

    preco_normalizado = (preco_texto or "").strip().replace("R$", "").replace(" ", "").replace(",", ".")
    if not preco_normalizado:
        return False, "Informe o preço do produto.", None

    try:
        preco = round(float(preco_normalizado), 2)
    except ValueError:
        return False, "O preço precisa ser um número válido (ex.: 29.90).", None

    if math.isnan(preco) or math.isinf(preco) or preco <= 0 or preco > 10000:
        return False, "O preço deve ser maior que R$ 0,00 e no máximo R$ 10.000,00.", None

    return True, "", preco
