import re
from dataclasses import dataclass

_EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


@dataclass
class UserProfile:
    """Representa o perfil autenticado na tabela public.perfis."""

    id: str
    user_id: str
    email: str
    nome: str
    telefone: str = ""
    endereco: str = ""
    criado_em: str = ""

    @classmethod
    def from_dict(cls, data: dict, email: str = "") -> "UserProfile":
        return cls(
            id=str(data.get("id", "")),
            user_id=str(data.get("user_id", "")),
            email=email,
            nome=str(data.get("nome", "")),
            telefone=str(data.get("telefone", "") or ""),
            endereco=str(data.get("endereco", "") or ""),
            criado_em=str(data.get("criado_em", "") or ""),
        )


def validate_email(email: str) -> tuple[bool, str]:
    """Valida formato e tamanho do e-mail informado."""
    clean = (email or "").strip()
    if not clean:
        return False, "Informe o seu e-mail."
    if len(clean) > 120 or not _EMAIL_REGEX.match(clean):
        return False, "Informe um e-mail válido."
    return True, clean.lower()


def validate_password(password: str) -> tuple[bool, str]:
    """Valida requisitos minimos e maximos de senha para cadastro."""
    if not password:
        return False, "Informe a sua senha."
    if len(password) < 6 or len(password) > 128:
        return False, "A senha deve ter entre 6 e 128 caracteres."
    return True, ""


def validate_profile_data(nome: str, telefone: str, endereco: str) -> tuple[bool, str]:
    """Valida os campos do perfil do usuario antes de salvar no banco."""
    nome_limpo = (nome or "").strip()
    tel_limpo = (telefone or "").strip()
    end_limpo = (endereco or "").strip()

    if len(nome_limpo) < 2 or len(nome_limpo) > 80:
        return False, "O nome deve ter entre 2 e 80 caracteres."
    if len(tel_limpo) > 25:
        return False, "O telefone deve ter no máximo 25 caracteres."
    if len(end_limpo) > 200:
        return False, "O endereço deve ter no máximo 200 caracteres."
    return True, ""
