# Atualizar o ChaveRadar no Visual Studio - v0.2.4

Esta versao mantem login/cadastro/aprovacao administrativa e adiciona aprovacao em massa na fila de Revisao.

## Atualizacao local

1. Pare o servidor com `Ctrl+C`.
2. Extraia o pacote sobre:
   `C:\Users\daniel.gusmao\source\repos\ChaveRadar`
3. Aceite substituir os arquivos.
4. Nao apague `.venv`, `.vs`, `.sln` ou `.git`.
5. No Developer PowerShell, com `(.venv)` ativo, execute:

```powershell
pip install -r requirements.txt
python manage.py migrate
python manage.py check
```

6. Para testar localmente antes do Render, crie um administrador:

```powershell
python manage.py createsuperuser
python manage.py runserver
```

7. Acesse `http://127.0.0.1:8000/`, entre como administrador e teste **Revisao -> Selecionar todos -> Aprovar selecionados**.

## Antes do deploy no Render

Nao faca o push antes de configurar o primeiro administrador no Render conforme `docs/11_AUTENTICACAO_APROVACAO.md`.
