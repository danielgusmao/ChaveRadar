# 05 - Hospedagem e deploy

## Desenvolvimento

Windows + Visual Studio 2026 Community + Python + Django. SQLite local.

## Producao inicial

```text
Registro.br -> DNS -> Render -> Django -> PostgreSQL
                     ^
                     |
                   GitHub
```

- GitHub armazena o código e aciona/publica alterações no Render conforme configuração.
- O DNS pode continuar no Registro.br.
- Cloudflare e opcional.
- Supabase pode ser usado como PostgreSQL gerenciado se fizer sentido no momento do deploy.
- Precos e limites de planos gratuitos mudam; validar imediatamente antes de publicar.

## Segredos

Não versionar tokens de Meta/API. Em produção, usar secrets/variaveis protegidas do provedor. Em ambiente local, usar armazenamento seguro quando iniciarmos as integracoes.


## Estado confirmado em 26/09/2026

- Render Web Service publicado com sucesso: `https://chaveradar.onrender.com`.
- GitHub: `danielgusmao/ChaveRadar`, branch `main`.
- Banco de producao escolhido: Supabase PostgreSQL.
- Projeto Supabase em South America (Sao Paulo), plano Free, status Healthy.
- Conexao de producao: Session pooler, configurada no Render pela variavel secreta `DATABASE_URL`.
- Nao salvar URI, senha ou credenciais no repositorio.
