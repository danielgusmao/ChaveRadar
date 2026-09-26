# 02 - Arquitetura

## Fluxo

```text
Fontes de dados
  |-- API oficial (contas conectadas)
  |-- CSV/Excel/colar (terceiros)
  `-- Provedor licenciado (futuro)
            |
            v
Ingestáo -> validação -> deduplicacao -> banco bruto
            |
            v
Contexto da publicação/imóvel
            |
            v
Deteccao de intenção (regras + IA quando necessário)
            |
            v
Qualificacao determinística
            |
            v
Revisão humana / auto-aprovacao
            |
            v
Dashboard e exportação
```

## Tecnologias

- Backend: Django/Python.
- Interface: HTML responsivo + Bootstrap.
- Desenvolvimento local: SQLite.
- Producao: PostgreSQL.
- Hospedagem inicial: Render.
- Codigo: GitHub.
- Mobile inicial: PWA/site responsivo.

## Regra de separacao

A coleta não deve conhecer as regras de qualificação. Todos os conectores transformam sua entrada em entidades `Profile`, `Publication` e `Comment`; a classificação e a mesma independentemente da origem.
