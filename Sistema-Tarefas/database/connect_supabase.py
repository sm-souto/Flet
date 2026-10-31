import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client, Client


def connect_supabase() -> Client:
    arquivo_env = Path(__file__).resolve().parents[1] / ".env"
    load_dotenv(dotenv_path=arquivo_env)
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise RuntimeError(
            "Configure SUPABASE_URL e SUPABASE_KEY no arquivo .env."
        )

    return create_client(url, key)


def verificar_tabela_tarefas(cliente: Client) -> bool:
    try:
        cliente.table("tarefas").select("id").limit(1).execute()
        return True
    except Exception as erro:
        raise RuntimeError(f"Não foi possível acessar a tabela 'tarefas': {erro}") from erro