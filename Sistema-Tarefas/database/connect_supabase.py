import os # Importar do sistema operacional
from dotenv import load_dotenv
from supabase import create_client, Client


def connect_supabase() -> Client: # Conectando com o Supabase de acordo com dados de .env
    load_dotenv()
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_KEY')
    
    return create_client(ulr, key)

def verificar_tabela_tarefas(cliente: Client) -> bool: # Método de segurança
    try:
        resposta = cliente.table('tarefas').select('id').limit(1).execute()
        return True
    except Exception as erro:
        raise RuntimeError(erro)