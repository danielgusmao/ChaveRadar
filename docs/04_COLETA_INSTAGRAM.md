# 04 - Coleta Instagram

## Contas próprias/conectadas

Usar a API oficial da Meta conforme o tipo de conta e fluxo de autenticação disponivel. Primeira sincronização pode fazer backfill; sincronizacoes seguintes devem buscar apenas novidades. Webhooks podem ser avaliados futuramente.

## Perfis de terceiros

Não implementar scraping automatizado. Usar importacao manual por copiar/colar, CSV ou Excel, ou integrar futuramente um fornecedor licenciado.

## Cobertura

Cada execucao registra sucesso/falha, quantidade de publicações, comentários encontrados, novos, duplicados e falhas. O dashboard deve distinguir `sem leads` de `sem dados suficientes`.
