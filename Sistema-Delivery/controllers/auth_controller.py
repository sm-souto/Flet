from supabase import Client

from models.user_model import (
    UserProfile,
    validate_email,
    validate_password,
    validate_profile_data,
)
from services.supabase_client import create_supabase_client


class AuthController:
    """Gerencia autenticacao no Supabase Auth, controle de sessao e perfil do usuario."""

    def __init__(self) -> None:
        self.client: Client = create_supabase_client()
        self.usuario_atual: UserProfile | None = None

    def is_authenticated(self) -> bool:
        """Verifica se ha um usuario autenticado valido na sessao."""
        return self.usuario_atual is not None and bool(self.usuario_atual.user_id)

    def require_auth(self) -> str:
        """Retorna o user_id autenticado ou lanca PermissionError."""
        if not self.is_authenticated():
            raise PermissionError("Usuário não autenticado.")
        return self.usuario_atual.user_id

    def _ensure_profile(
        self,
        user_id: str,
        email: str,
        fallback_nome: str = "",
        fallback_telefone: str = "",
        fallback_endereco: str = "",
    ) -> UserProfile:
        """Carrega o perfil do usuario em public.perfis ou cria caso ainda nao exista."""
        response = (
            self.client.table("perfis")
            .select("*")
            .eq("user_id", user_id)
            .limit(1)
            .execute()
        )
        rows = response.data or []
        if rows:
            return UserProfile.from_dict(rows[0], email=email)

        nome_inicial = (fallback_nome or email.split("@")[0] or "Cliente").strip()[:80]
        if len(nome_inicial) < 2:
            nome_inicial = "Cliente"

        payload = {
            "user_id": user_id,
            "nome": nome_inicial,
            "telefone": (fallback_telefone or "").strip()[:25],
            "endereco": (fallback_endereco or "").strip()[:200],
        }
        created = self.client.table("perfis").insert(payload).execute()
        created_rows = created.data or []
        if created_rows:
            return UserProfile.from_dict(created_rows[0], email=email)

        return UserProfile(
            id="",
            user_id=user_id,
            email=email,
            nome=nome_inicial,
            telefone=payload["telefone"],
            endereco=payload["endereco"],
        )

    def login(self, email: str, password: str) -> tuple[bool, str]:
        """Autentica o usuario usando Supabase Auth com mensagem de erro generica."""
        ok_email, email_result = validate_email(email)
        if not ok_email or not password:
            return False, "E-mail ou senha inválidos."

        try:
            res = self.client.auth.sign_in_with_password(
                {"email": email_result, "password": password}
            )
        except Exception:
            return False, "E-mail ou senha inválidos."

        if not res or not res.user or not res.session:
            return False, "E-mail ou senha inválidos."

        metadata = res.user.user_metadata or {}
        try:
            self.usuario_atual = self._ensure_profile(
                user_id=str(res.user.id),
                email=str(res.user.email or email_result),
                fallback_nome=str(metadata.get("nome", "")),
                fallback_telefone=str(metadata.get("telefone", "")),
                fallback_endereco=str(metadata.get("endereco", "")),
            )
            return True, "Login realizado com sucesso!"
        except Exception:
            self.logout()
            return False, "Não foi possível carregar seu perfil no momento. Tente novamente."

    def register(
        self,
        nome: str,
        email: str,
        password: str,
        telefone: str = "",
        endereco: str = "",
    ) -> tuple[bool, str]:
        """Cria uma nova conta via Supabase Auth e registra o perfil do usuario."""
        ok_profile, msg_profile = validate_profile_data(nome, telefone, endereco)
        if not ok_profile:
            return False, msg_profile

        ok_email, email_result = validate_email(email)
        if not ok_email:
            return False, email_result

        ok_pwd, msg_pwd = validate_password(password)
        if not ok_pwd:
            return False, msg_pwd

        nome_limpo = nome.strip()
        tel_limpo = (telefone or "").strip()
        end_limpo = (endereco or "").strip()

        try:
            res = self.client.auth.sign_up(
                {
                    "email": email_result,
                    "password": password,
                    "options": {
                        "data": {
                            "nome": nome_limpo,
                            "telefone": tel_limpo,
                            "endereco": end_limpo,
                        }
                    },
                }
            )
        except Exception:
            return False, "Não foi possível criar a conta. Verifique os dados ou use outro e-mail."

        if not res or not res.user:
            return False, "Não foi possível concluir o cadastro. Tente novamente."

        if res.session is None:
            return (
                True,
                "Cadastro realizado! Se a confirmação por e-mail estiver ativa, confirme sua caixa de entrada e faça login.",
            )

        try:
            self.usuario_atual = self._ensure_profile(
                user_id=str(res.user.id),
                email=str(res.user.email or email_result),
                fallback_nome=nome_limpo,
                fallback_telefone=tel_limpo,
                fallback_endereco=end_limpo,
            )
            return True, "Conta criada com sucesso! Bem-vindo ao sistema."
        except Exception:
            self.logout()
            return False, "Conta criada, mas não foi possível inicializar seu perfil. Faça login novamente."

    def update_profile(self, nome: str, telefone: str, endereco: str) -> tuple[bool, str]:
        """Atualiza os dados do perfil do usuario autenticado."""
        if not self.is_authenticated():
            return False, "Faça login para editar o perfil."

        ok, msg = validate_profile_data(nome, telefone, endereco)
        if not ok:
            return False, msg

        payload = {
            "nome": nome.strip(),
            "telefone": (telefone or "").strip(),
            "endereco": (endereco or "").strip(),
        }

        try:
            user_id = self.require_auth()
            res = (
                self.client.table("perfis")
                .update(payload)
                .eq("user_id", user_id)
                .execute()
            )
            rows = res.data or []
            if rows:
                self.usuario_atual = UserProfile.from_dict(rows[0], email=self.usuario_atual.email)
            else:
                self.usuario_atual.nome = payload["nome"]
                self.usuario_atual.telefone = payload["telefone"]
                self.usuario_atual.endereco = payload["endereco"]
            return True, "Perfil atualizado com sucesso!"
        except Exception:
            return False, "Não foi possível atualizar o perfil no momento. Tente novamente."

    def logout(self) -> tuple[bool, str]:
        """Encerra a sessao no Supabase Auth e limpa os dados da memoria."""
        try:
            self.client.auth.sign_out()
        except Exception:
            pass
        finally:
            self.usuario_atual = None
            self.client = create_supabase_client()
        return True, "Sessão encerrada com sucesso."
