# Atualizar o ChaveRadar no Visual Studio - v0.2.1

1. Pare o servidor local com `Ctrl+C`.
2. Extraia os arquivos desta versao sobre a raiz do projeto atual:
   `C:\Users\daniel.gusmao\source\repos\ChaveRadar`
3. Aceite substituir os arquivos existentes.
4. Nao apague `.venv`, `.vs`, `.sln` ou arquivos do Git.
5. No Developer PowerShell, confirme que `(.venv)` esta ativo.
6. Execute:

```powershell
pip install -r requirements.txt
python manage.py check
```

7. Se `check` terminar sem erros, envie a versao ao GitHub:

```powershell
git add .
git commit -m "ChaveRadar v0.2.1 - prepara deploy Render"
git push
```

8. Somente depois do push volte ao Render. Nao clicar em Deploy Web Service antes desta etapa.
