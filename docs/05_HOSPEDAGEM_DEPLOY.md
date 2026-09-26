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
