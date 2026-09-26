# Atualizar o ChaveRadar no Visual Studio - v0.2.2

Esta versao adiciona suporte ao PostgreSQL do Supabase sem retirar o SQLite local.

1. Pare o servidor local com `Ctrl+C`.
2. Extraia esta versao sobre a raiz do projeto atual:
   `C:\Users\daniel.gusmao\source\repos\ChaveRadar`
3. Aceite substituir os arquivos existentes.
4. Nao apague `.venv`, `.vs`, `.sln` ou `.git`.
5. No Developer PowerShell, confirme que `(.venv)` esta ativo.
6. Execute somente:

```powershell
pip install -r requirements.txt
python manage.py check
```

7. Se o check terminar sem erros:

```powershell
git add .
git commit -m "ChaveRadar v0.2.2 - adiciona PostgreSQL Supabase"
git push
```

8. No Render, adicionar `DATABASE_URL` com a URI do **Session pooler** do Supabase. Nunca versionar essa URI.
9. O Render fara novo deploy a partir do push. Se o auto-deploy nao iniciar, usar `Manual Deploy -> Deploy latest commit`.
10. Depois do deploy, validar Dashboard, Leads, Perfis, Importacao e Revisao.
