import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import Client, create_client

_ROOT_ENV = Path(__file__).resolve().parent.parent / ".env"


def get_supabase_config() -> tuple[str, str]:
    """Carrega e valida as credenciais publicas do Supabase via variaveis de ambiente."""
    if _ROOT_ENV.exists():
        load_dotenv(dotenv_path=_ROOT_ENV, override=False)
    load_dotenv(override=False)

    supabase_url = os.environ.get("SUPABASE_URL", "").strip().rstrip("/")
    if supabase_url.endswith("/rest/v1"):
        supabase_url = supabase_url[:-8]

    supabase_key = os.environ.get("SUPABASE_KEY", "").strip()

    if not supabase_url or not supabase_key:
        raise ValueError("Variáveis de ambiente do Supabase não configuradas.")

    if not (supabase_url.startswith("https://") or supabase_url.startswith("http://")):
        raise ValueError("URL do Supabase inválida nas variáveis de ambiente.")

    if "service_role" in supabase_key or supabase_key.startswith("sb_secret"):
        raise ValueError("Chave privada não pode ser utilizada na aplicação cliente.")

    return supabase_url, supabase_key


def create_supabase_client() -> Client:
    """Cria uma nova instancia isolada do cliente Supabase para a sessao atual."""
    url, key = get_supabase_config()
    return create_client(url, key)
