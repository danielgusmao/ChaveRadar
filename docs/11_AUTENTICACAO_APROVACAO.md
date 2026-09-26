# 11 - Autenticacao e aprovacao de usuarios

## Objetivo

O ChaveRadar nao deve ficar aberto publicamente. Toda tela operacional exige login.

Novos usuarios podem solicitar cadastro, mas a conta nasce inativa e somente um administrador pode liberar o acesso.

## Fluxo

`cadastro -> conta inativa -> fila de aprovacao -> admin aprova/rejeita -> login liberado/bloqueado`

## Regras

- Cadastro publico disponivel em `/cadastro/`.
- Login em `/entrar/`.
- Conta nova usa o `User` nativo do Django com `is_active=False`.
- A solicitacao e registrada em `accounts_userapproval`.
- Apenas usuarios `is_staff=True` podem abrir `/usuarios/pendentes/`.
- Aprovacao ativa o usuario e registra quem aprovou e quando.
- Rejeicao mantem o usuario inativo e registra quem rejeitou e quando.
- O administrador tambem pode usar `/admin/`.
- Paginas de Dashboard, Leads, Perfis, Importacao, Revisao e Exportacao exigem autenticacao.

## Primeiro administrador no Render

O Render precisa ter pelo menos um administrador antes de a protecao ser ativada.

Variaveis temporarias/secretas:

- `CHAVERADAR_ADMIN_USERNAME`
- `CHAVERADAR_ADMIN_EMAIL`
- `CHAVERADAR_ADMIN_PASSWORD`

Build Command recomendado para o primeiro deploy da v0.2.3:

```text
pip install -r requirements.txt && python manage.py migrate && python manage.py bootstrap_admin && python manage.py collectstatic --noinput
```

O comando `bootstrap_admin` e idempotente: cria o administrador se ele nao existir; em deploys posteriores apenas confirma as permissoes e nao redefine a senha existente.

Depois que o primeiro administrador entrar com sucesso, pode-se remover `CHAVERADAR_ADMIN_PASSWORD` do Render. Sem as tres variaveis completas, o comando simplesmente nao altera nada.

## Seguranca

- Senhas sao armazenadas pelo sistema de hashing do Django, nunca em texto puro no banco.
- Validadores de senha do Django foram habilitados.
- Cookies de sessao e CSRF sao marcados como seguros em producao.
- `SECRET_KEY`, `DATABASE_URL` e senhas administrativas nunca devem ir para GitHub ou documentacao.
