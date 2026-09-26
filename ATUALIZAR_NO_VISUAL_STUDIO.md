# Atualizar no Visual Studio - v0.2.0

## Passos

1. No terminal onde o servidor esta rodando, pressione `Ctrl+C`.
2. Extraia o conteudo deste ZIP dentro de:

`C:\Users\daniel.gusmao\source\repos\ChaveRadar`

3. Aceite substituir os arquivos com o mesmo nome.
4. O ZIP nao contem a sua `.sln`, `.pyproj`, `.vs` ou `.venv`.
5. Volte ao Developer PowerShell e confirme que aparece `(.venv)`.
6. Execute:

```powershell
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

7. Abra `http://127.0.0.1:8000/`.

Se as novas pastas nao aparecerem no Gerenciador de Solucoes, use **Mostrar Todos os Arquivos** ou recarregue o projeto. Isso nao impede o Django de executar os arquivos existentes no disco.
