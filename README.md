# ChaveRadar v0.2.0

MVP web responsivo para organizar comentarios publicos de perfis imobiliarios, identificar sinais de intencao comercial e apresentar leads por nivel de qualificacao.

## O que esta versao ja possui

- Dashboard responsivo para computador e celular.
- Identidade visual inicial ChaveRadar.
- Cadastro estrutural de perfis, publicacoes, comentarios e classificacoes.
- Lista consolidada de leads com filtros.
- Tela de perfis monitorados.
- Importacao de CSV.
- Classificador inicial por regras para Alto / Medio / Baixo / Nao Lead.
- Fila de revisao humana.
- Exportacao de leads para Excel.
- Comando para carregar 24 leads de demonstracao.
- Admin do Django.

## Teste rapido no Windows / Visual Studio

Com a `.venv` ativada, execute:

```powershell
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Depois abra:

`http://127.0.0.1:8000/`

O comando `seed_demo` pode ser executado novamente sem duplicar os registros ja carregados.

## Atualizar um projeto ja criado no Visual Studio

1. Pare o servidor com `Ctrl+C`.
2. Feche o Visual Studio ou mantenha-o aberto sem o servidor rodando.
3. Extraia o pacote na raiz `C:\Users\daniel.gusmao\source\repos\ChaveRadar`, aceitando substituir os arquivos do pacote.
4. O pacote nao inclui `.sln`, `.pyproj` nem `.venv`, portanto esses itens locais sao preservados.
5. Reabra/atualize o Visual Studio e rode os comandos de teste acima.

## Documentacao

Leia primeiro `docs/00_CHECKPOINT.md`. Ele e o ponto oficial de retomada do projeto e deve permanecer cumulativo.
