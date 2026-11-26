# SaborExpress Delivery — Sistema Web com Flet, MVC e Supabase

Sistema completo de **Delivery** desenvolvido em **Python + Flet + Supabase** seguindo a arquitetura **MVC (Model, View, Controller)** e as 5 rotinas essenciais de segurança.

## Estrutura do Projeto (MVC)

- `main.py` — Ponto de entrada da aplicação web Flet (`ft.run(..., view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=porta)`), controle de sessão por usuário e proteção de telas.
- `models/` — Classes de domínio (`UserProfile`, `Category`, `Product`, `CartItem`, `Order`, `OrderItem`) e funções de validação rigorosa de entradas.
- `controllers/` — Regras de negócio e comunicação autenticada com o Supabase (`AuthController`, `CartController`, `OrderController`), com tratamento de erros via `try / except` e mensagens seguras.
- `views/` — Interfaces gráficas em Flet (`login_view.py`, `home_view.py`, `cart_view.py`, `tracking_view.py`, `admin_view.py`, `ui_helpers.py`).
- `services/` — Cliente Supabase isolado por sessão (`supabase_client.py`) carregando variáveis via `.env` e atualização periódica de pedidos (`realtime_service.py`).

## Configuração do Banco de Dados (Supabase)

1. Acesse o painel do seu projeto no Supabase e abra o **SQL Editor**.
2. Cole o script SQL das tabelas (`perfis`, `categorias`, `produtos`, `pedidos`, `itens_pedido`) com as chaves estrangeiras e políticas de RLS e execute (**Run**).
3. Confira em **Authentication -> Policies** se todas as 5 tabelas estão com **RLS enabled** e as 4 políticas (`SELECT`, `INSERT`, `UPDATE`, `DELETE`).

## Execução Local

```bash
pip install -r requirements.txt
python main.py
```

O servidor iniciará em `http://localhost:8080`. Certifique-se de que o arquivo `.env` na raiz possui `SUPABASE_URL` (sem `/rest/v1/`) e `SUPABASE_KEY` (chave pública `Publishable` / `anon`).

## Hospedagem na Nuvem

- **Render**: Web Service conectado ao GitHub, Build: `pip install -r requirements.txt`, Start: `python main.py`, e cadastre `SUPABASE_URL` e `SUPABASE_KEY` em *Environment Variables*.
- **Hugging Face Spaces**: Space com SDK *Docker* (já há um `Dockerfile` pronto na raiz) e cadastre `SUPABASE_URL` e `SUPABASE_KEY` em *Settings -> Variables and secrets*.
- **Koyeb**: Conecte o repositório GitHub ou `Dockerfile` e cadastre `SUPABASE_URL` e `SUPABASE_KEY` nas variáveis de ambiente.
