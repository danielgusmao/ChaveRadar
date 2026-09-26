# ChaveRadar v0.2.5

MVP web responsivo para organizar comentarios publicos de perfis imobiliarios, identificar sinais de intencao comercial e apresentar leads por nivel de qualificacao.

## O que esta versao possui

- Dashboard responsivo para computador e celular.
- Lista consolidada de leads com filtros.
- Tela de perfis de origem dos dados.
- Tela de Monitoramento com cadastro, edicao e exclusao segura de contas do Instagram.
- Ativar/pausar monitoramento e alertas por perfil; palavras-chave adicionais por conta.
- Importacao de CSV.
- Classificador inicial por regras para Alto / Medio / Baixo / Nao Lead.
- Fila de revisao humana.
- Aprovacao em massa de leads selecionados na fila de revisao.
- Exportacao de leads para Excel.
- PostgreSQL/Supabase em producao e SQLite local.
- Tela de login.
- Tela de cadastro.
- Cadastro novo bloqueado ate aprovacao de administrador.
- Tela interna para administradores aprovarem ou rejeitarem usuarios.
- Logout e protecao das paginas internas por autenticacao.
- Comando seguro e idempotente para criar o primeiro administrador no Render.
- Admin nativo do Django em `/admin/`.

## Teste local no Windows / Visual Studio

Com a `.venv` ativada:

```powershell
pip install -r requirements.txt
python manage.py migrate
python manage.py check
python manage.py createsuperuser
python manage.py runserver
```

Abra `http://127.0.0.1:8000/`.

A pagina inicial redireciona para `/entrar/` quando nao houver sessao autenticada.

## Fluxo de cadastro

1. Usuario acessa `/cadastro/`.
2. Preenche nome, e-mail, usuario e senha.
3. A conta e criada com `is_active=False`.
4. O administrador entra no sistema.
5. Administrador abre **Usuarios** -> **Cadastros pendentes**.
6. Ao clicar **Aprovar**, a conta passa a `is_active=True` e pode efetuar login.
7. Ao clicar **Rejeitar**, a conta continua bloqueada.

## Primeiro administrador no Render

Como o plano gratuito pode nao oferecer Shell, a v0.2.5 inclui:

```text
python manage.py bootstrap_admin
```

Antes do primeiro deploy desta versao, crie temporariamente no Render:

- `CHAVERADAR_ADMIN_USERNAME`
- `CHAVERADAR_ADMIN_EMAIL`
- `CHAVERADAR_ADMIN_PASSWORD`

E acrescente `python manage.py bootstrap_admin` ao Build Command depois de `migrate`.

O comando cria o administrador somente se ele ainda nao existir e nao redefine sua senha em deploys futuros. Depois de confirmar o primeiro login, a senha de bootstrap pode ser removida das variaveis do Render.

## Banco em producao

Sem `DATABASE_URL`, o projeto usa SQLite local. Com `DATABASE_URL`, usa PostgreSQL/Supabase. A URI e senhas nunca devem ser versionadas.

## Documentacao

Leia primeiro `docs/00_CHECKPOINT.md`. Ele e o ponto oficial de retomada e deve permanecer cumulativo.
