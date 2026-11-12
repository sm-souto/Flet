import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

_client: Client = None


def get_client() -> Client:
    global _client

    if _client is None:
        url = os.getenv("SUPABASE_URL", "")
        key = os.getenv("SUPABASE_KEY", "")

        if not url or url == "https://bexypupmafdpsbnmlcfs.supabase.co":
            raise EnvironmentError("SUPABASE_URL não configurada no arquivo .env.")
        if not key or key == "sb_publishable_NQSH9_TzBWTIazQN-G490w_w8PZfwCM":
            raise EnvironmentError("SUPABASE_KEY não configurada no arquivo .env.")

        _client = create_client(url, key)

    return _client