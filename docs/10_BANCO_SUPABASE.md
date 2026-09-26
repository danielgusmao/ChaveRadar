# 10 - Banco PostgreSQL no Supabase

## Decisao atual

O banco de producao do ChaveRadar sera PostgreSQL hospedado no Supabase.
O desenvolvimento local continua podendo usar SQLite quando `DATABASE_URL` nao estiver definida.

## Projeto criado

- Nome: ChaveRadar
- Plano: Free
- Regiao: South America (Sao Paulo)
- Status confirmado: Healthy
- Metodo de conexao escolhido: Session pooler
- Porta: 5432

## Por que Session pooler

O deploy esta no Render e a conexao escolhida no Supabase e o Session pooler, adequado para acesso por rede IPv4. Nao usar a conexao direta pura neste fluxo atual.

## Segredo

A URI completa contem credenciais. Ela nao deve ser colocada no GitHub, em documentos, screenshots ou arquivos versionados.

No Render, criar uma variavel de ambiente:

`DATABASE_URL=<URI completa copiada do Supabase, com a senha real no lugar indicado>`

Se a senha tiver caracteres especiais, usar a URI produzida/aceita pelo Supabase com a senha corretamente codificada.

## Comportamento da v0.2.2

- Se `DATABASE_URL` existir: Django usa PostgreSQL/Supabase com SSL.
- Se `DATABASE_URL` nao existir: Django usa SQLite local em `dados/chaveradar.db`.

## Deploy

Depois de configurar `DATABASE_URL` no Render e enviar a v0.2.2 ao GitHub, o Build Command continua executando as migrations. O comando `seed_demo` e idempotente e pode carregar os 24 registros de demonstracao no novo banco sem duplicar os mesmos comentarios.
