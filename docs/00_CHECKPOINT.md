# Atualizacao - 2026-09-26 - v0.2.3 autenticacao e aprovacao administrativa

- Nova decisao: o ChaveRadar passa a exigir **login** para todas as telas operacionais (Dashboard, Leads, Perfis, Importacao, Revisao e Exportacao).
- Criado fluxo de **cadastro publico com aprovacao obrigatoria**: novo usuario e criado com `is_active=False` e nao consegue entrar antes da liberacao.
- Criado app `accounts` com modelo `UserApproval` para registrar status `pending/approved/rejected`, data da solicitacao, data da revisao e administrador responsavel.
- Criadas telas `/entrar/`, `/cadastro/`, `/cadastro/aguardando/` e, para administradores, `/usuarios/pendentes/`.
- Administradores (`is_staff=True`) podem aprovar ou rejeitar cadastros diretamente pela interface do ChaveRadar; o Django Admin continua disponivel em `/admin/`.
- A aprovacao ativa o usuario; a rejeicao mantem a conta inativa.
- Habilitados validadores de senha do Django e cookies seguros em producao.
- Criado comando `python manage.py bootstrap_admin` para criar o primeiro superusuario no Render usando variaveis secretas de ambiente, sem redefinir senha em deploys futuros.
- Variaveis previstas no Render: `CHAVERADAR_ADMIN_USERNAME`, `CHAVERADAR_ADMIN_EMAIL` e `CHAVERADAR_ADMIN_PASSWORD`. Nunca registrar valores reais no GitHub ou docs.
- Build Command recomendado no primeiro deploy da v0.2.3: `pip install -r requirements.txt && python manage.py migrate && python manage.py bootstrap_admin && python manage.py collectstatic --noinput`.
- Corrigido o rodape para usar automaticamente a versao do arquivo `VERSION` e diferenciar ambiente `Local`/`Online`; remove a exibicao fixa `MVP local / v0.2.0`.
- Interface passa a mostrar usuario autenticado, menu de sair e atalho de administracao para staff.
- Documento tematico criado: `docs/11_AUTENTICACAO_APROVACAO.md`.
- Regra permanente mantida: toda versao entregue deve conter `docs/00_CHECKPOINT.md` atualizado dentro do pacote.
- Proximo passo operacional: validar localmente `migrate` + `check`; depois configurar as 3 variaveis de bootstrap no Render **antes do push**, atualizar o Build Command e somente entao publicar a v0.2.3.

---
# Atualizacao - 2026-09-26 - Aprendizado por revisao humana definido

- Teste do botao `Confirmar` na tela Revisao concluido com sucesso: o lead `@cliente_exemplo` foi aprovado, saiu da fila e a contagem caiu de 26 para 25.
- A revisao humana passa a ser tratada como **feedback supervisionado** do sistema. Cada acao `Confirmar` ou `Nao e lead` deve ficar registrada no banco para medir acertos/erros do classificador.
- Decisao de arquitetura: o ChaveRadar **nao vai "treinar uma IA" automaticamente a cada clique**. Primeiro, o sistema acumula historico de revisoes e usa esse historico para ajustar regras, limiares de confianca e prompts.
- Evolucao prevista do classificador: regras deterministicas para casos obvios -> IA semantica para casos ambiguos -> decisao final auditavel -> revisao humana -> feedback armazenado.
- O feedback humano devera registrar pelo menos: classificacao sugerida, decisao humana, nivel final, intencoes finais, data da revisao e versao do classificador.
- Quando houver volume suficiente de revisoes, considerar aprendizado supervisionado/fine-tuning apenas se trouxer ganho real; para o MVP, preferir prompt + regras + exemplos revisados, que e mais simples, barato e auditavel.
- Proxima versao deve corrigir o rodape `MVP local / v0.2.0`, evitar handle duplicado quando nome e handle forem iguais e preparar os campos de auditoria de revisao.
- Regra permanente: toda versao entregue deve conter `docs/00_CHECKPOINT.md` atualizado dentro do pacote.

---
# Atualizacao - 2026-09-26 - Tela Revisao validada com 26 leads

- A tela `Revisao` foi validada no ambiente online `https://chaveradar.onrender.com/revisao/`.
- A fila mostra **26 leads aguardando validacao**, incluindo os 2 registros importados recentemente.
- Exemplos confirmados na tela: `@comprador_exemplo` classificado como Medio por `CONDOMINIUM`/`PRICE` com confianca 0,91; `@cliente_exemplo` classificado como Alto por `AVAILABILITY` com confianca 0,96.
- As classificacoes dos 24 registros anteriores tambem continuam visiveis, preservando intencao, nivel e confianca.
- Pontos de UX observados para proxima versao: evitar repetir handle duas vezes quando `display_name == handle`; revisar texto/acentuacao visual; confirmar comportamento real dos botoes `Confirmar` e `Nao e lead`.
- Proximo teste funcional: confirmar um lead na fila e verificar se ele sai da fila e se a contagem reduz; depois testar a acao `Nao e lead`.
- Regra permanente: toda versao entregue deve conter `docs/00_CHECKPOINT.md` atualizado dentro do pacote.

---
# Atualizacao - 2026-09-26 - Importacao real validada no ambiente online

- Teste da tela **Importar comentarios** concluido no ChaveRadar publicado no Render.
- O arquivo de modelo foi processado com sucesso: **2 novos**, **0 duplicados**, **0 invalidos**.
- A tela **Leads** passou de 24 para **26 registros**, confirmando que os 2 novos comentarios foram persistidos no PostgreSQL/Supabase.
- Os novos registros aparecem corretamente com perfil de origem `@imobiliaria_exemplo`, contexto do imovel/regiao e niveis de qualificacao.
- Observacao visual pendente: sidebar ainda exibe `MVP local` e `v0.2.0`; corrigir em uma proxima versao.
- Proximo passo: validar a tela **Revisao** para confirmar que os 2 novos registros aparecem no fluxo de revisao humana e que as classificacoes estao coerentes.

---
# Atualizacao - 2026-09-26 - Importacao CSV validada em producao

- Importacao manual testada no ChaveRadar publicado no Render.
- Arquivo CSV de modelo foi processado com sucesso.
- Resultado exibido pela interface: **2 novos**, **0 duplicados**, **0 invalidos**.
- O fluxo de importacao esta gravando no PostgreSQL/Supabase e a interface confirmou `Importacao concluida.`
- Observacao visual: o rodape lateral ainda exibe `MVP local` e versao `v0.2.0`, embora a versao implantada seja v0.2.2; corrigir em uma proxima versao.
- Proximo teste: abrir `Leads` e `Revisao` para confirmar que os 2 novos registros foram classificados e aparecem no fluxo de revisao.
- Regra permanente: toda versao entregue deve conter `docs/00_CHECKPOINT.md` atualizado dentro do pacote.

---
# Atualizacao - 2026-09-26 - Persistencia PostgreSQL confirmada apos redeploy

- O Build Command do Render foi alterado para remover `python manage.py seed_demo`; o seed de demonstracao passa a ser somente ferramenta manual de desenvolvimento/teste.
- Um novo deploy foi concluido com sucesso no Render sem executar o seed.
- Apos o redeploy, o Supabase Table Editor continuou mostrando **24 registros** em `leads_comment`.
- Isso comprova que os dados do ChaveRadar estao persistindo no PostgreSQL/Supabase e nao dependem do filesystem temporario do Render.
- As classificacoes em `leads_classification` ja haviam sido confirmadas no PostgreSQL.
- Proximo passo aprovado: testar o fluxo real do MVP de ponta a ponta: importacao manual -> classificacao -> revisao -> persistencia -> dashboard/exportacao.
- Regra permanente: toda versao entregue deve conter `docs/00_CHECKPOINT.md` atualizado dentro do pacote.

---
# Atualizacao - 2026-09-26 - Persistencia PostgreSQL confirmada apos novo deploy

- Build Command do Render foi atualizado para remover `python manage.py seed_demo` do fluxo de producao.
- Novo deploy foi executado automaticamente apos a alteracao do Build Command e concluiu com `Deploy succeeded | Live`.
- Fonte do deploy permaneceu no commit `b39f4b5` da v0.2.2; o gatilho exibido foi `Build command updated`.
- Os 24 comentarios e respectivas classificacoes ja haviam sido confirmados no Supabase antes deste deploy. Como `seed_demo` nao foi executado novamente, o proximo passo e confirmar que os 24 registros permanecem no Supabase; isso validara definitivamente a persistencia do PostgreSQL entre deploys.
- `seed_demo` passa a ser considerado ferramenta manual de desenvolvimento/teste e nao deve fazer parte do Build Command de producao.
- Regra permanente mantida: toda versao entregue deve incluir `docs/00_CHECKPOINT.md` atualizado dentro do pacote.

---
# Atualizacao - 2026-09-26 - PostgreSQL Supabase validado no Table Editor

- Deploy da v0.2.2 no Render concluido com sucesso e status `Deploy succeeded | Live`.
- Conexao `DATABASE_URL` com o Supabase Session pooler foi aceita pelo Django; as migrations foram aplicadas com sucesso.
- No Supabase Table Editor foram confirmadas as tabelas do Django e do dominio ChaveRadar, incluindo `leads_profile`, `leads_publication`, `leads_comment`, `leads_classification` e `leads_collectionrun`.
- Isso confirma que o schema do ChaveRadar esta persistido no PostgreSQL do Supabase, e nao apenas no SQLite temporario do Render.
- Proximo passo: validar os dados de demonstracao no PostgreSQL, conferindo registros em `leads_comment` e `leads_classification`; depois testar persistencia atraves de um novo deploy sem executar mudancas no banco.
- Regra permanente: toda versao entregue deve conter `docs/00_CHECKPOINT.md` atualizado dentro do pacote.

---
# Atualizacao - 2026-09-26 - v0.2.2 enviada ao GitHub

- Regra permanente: toda versao entregue deve conter `docs/00_CHECKPOINT.md` atualizado dentro do pacote.
- Commit da v0.2.2 concluido localmente: `b39f4b5` - `ChaveRadar v0.2.2 - adiciona PostgreSQL Supabase`.
- `git status` ficou limpo antes do envio.
- Push concluido com sucesso para `https://github.com/danielgusmao/ChaveRadar.git`, branch `main` (`0d5473b..b39f4b5`).
- A v0.2.2 publicada no GitHub contem suporte a `DATABASE_URL`, `dj-database-url`, `psycopg[binary]`, documentacao do Supabase e checkpoint cumulativo.
- Proximo passo: no Render, adicionar a variavel de ambiente `DATABASE_URL` usando a URI do **Supabase Session pooler** (porta 5432), sem expor a senha em chat/GitHub; depois salvar e acompanhar o novo deploy.
- A URI deve permanecer somente como segredo no Render; nunca registrar em arquivos versionados.

---
# Atualizacao - 2026-09-26 - Supabase PostgreSQL preparado (v0.2.2)

- Regra permanente: toda versao entregue deve conter `docs/00_CHECKPOINT.md` atualizado dentro do pacote.
- Primeiro deploy do ChaveRadar no Render foi concluido com sucesso e ficou `Live`; URL inicial: `https://chaveradar.onrender.com`.
- Usuario confirmou que os links/telas publicados estao funcionando.
- Projeto Supabase `ChaveRadar` criado no plano Free, regiao **South America (Sao Paulo)** e status **Healthy**.
- Metodo de conexao escolhido no Supabase: **Session pooler**, tipo URI, porta **5432**. A URI completa e a senha NAO devem ser registradas em documentacao ou GitHub.
- v0.2.2 passa a suportar dois bancos: SQLite local quando `DATABASE_URL` estiver ausente; PostgreSQL/Supabase quando `DATABASE_URL` estiver definida no Render.
- Dependencias adicionadas: `dj-database-url` e `psycopg[binary]`.
- Proxima sequencia: atualizar arquivos locais com v0.2.2 -> `pip install -r requirements.txt` -> `python manage.py check` -> commit/push -> adicionar `DATABASE_URL` no Render -> novo deploy -> validar persistencia.

---
# Atualizacao - 2026-09-26 - Preparacao guiada do primeiro deploy no Render (v0.2.1)

- Regra permanente reafirmada: toda versao entregue do ChaveRadar deve conter `docs/00_CHECKPOINT.md` atualizado dentro do pacote.
- Usuario confirmou que esta realizando o primeiro deploy web e pediu fluxo mais lento, uma etapa por vez.
- GitHub remoto confirmado pelo usuario: `https://github.com/danielgusmao/ChaveRadar.git`, branch `main` criada e primeiro push concluido.
- `gunicorn` e `whitenoise` ja estavam instalados na `.venv` local.
- O usuario executou `pip freeze > requirements.txt`; nesta versao o projeto volta a usar um `requirements.txt` curto e controlado para evitar dependencias locais desnecessarias no Render.
- `settings.py` foi preparado para desenvolvimento local e Render: `SECRET_KEY` e `DEBUG` por variaveis de ambiente, inclusao automatica de `RENDER_EXTERNAL_HOSTNAME` em `ALLOWED_HOSTS`, WhiteNoise para arquivos estaticos e possibilidade futura de `DJANGO_ALLOWED_HOSTS` para dominio proprio.
- Banco continua SQLite apenas para o primeiro teste de deploy. Como o plano gratuito do Render nao fornece disco persistente, nao considerar SQLite como banco definitivo de producao; PostgreSQL sera a etapa posterior.
- Estado do Render observado: repositorio `danielgusmao/ChaveRadar`, Python 3, branch `main`, formulario de criacao de Web Service aberto. O usuario NAO deve clicar em `Deploy Web Service` antes de atualizar os arquivos locais, executar `python manage.py check` e realizar novo `git push`.
- Proxima acao: substituir os arquivos locais pela v0.2.1, validar `python manage.py check`, fazer commit/push e somente entao preencher/revisar os campos do Render em conjunto.

---
# Atualizacao - 2026-09-26 - MVP visual v0.2.0 pronto para teste

- Criada a primeira versao funcional para teste: **ChaveRadar v0.2.0**.
- Direcao visual definida: minimalista, profissional e responsiva, com sidebar escura, area principal clara e acento verde-petroleo/teal.
- Referencias de produto usadas apenas como inspiracao de usabilidade: dashboards simples e orientados a metricas do Pipedrive e a interface mais calma/consistente do Linear. Nao copiar identidade visual ou elementos proprietarios.
- Logo inicial implementada como marca vetorial simples dentro da interface: radar circular + ponteiro/chave, acompanhada do wordmark `ChaveRadar`. Nao depende de arquivo de imagem externo e pode ser substituida futuramente.
- O MVP agora inclui: Dashboard, Leads, Perfis, Importar CSV, Revisao humana e Exportar Excel.
- Criado classificador inicial por regras para Alto/Medio/Baixo/Nao Lead. IA ainda nao foi integrada; esta fase serve para validar fluxo e regras rapidamente.
- Criado comando `python manage.py seed_demo` com os 24 leads de referencia fornecidos anteriormente pelo usuario. O comando e idempotente e nao deve duplicar os dados ja existentes.
- Criado `docs/modelo_importacao.csv` para testar importacao manual.
- Criada migracao inicial do app `leads`.
- Pacote de atualizacao foi estruturado para ser extraido sobre a raiz do projeto Visual Studio existente, sem incluir `.sln`, `.pyproj`, `.vs` ou `.venv`.
- Sequencia de teste da v0.2.0: `pip install -r requirements.txt`; `python manage.py migrate`; `python manage.py seed_demo`; `python manage.py runserver`.
- Nesta etapa o pacote passou por validacao sintatica (`compileall`). O ambiente de construcao nao tinha acesso externo para instalar Django e executar `manage.py check`; a validacao funcional final deve ser feita na `.venv` local ja confirmada do usuario com Django 5.2.17.
- Proxima etapa apos o teste visual: coletar feedback de layout/fluxo e ajustar rapidamente antes de integrar Meta API, IA ou hospedagem.

---
# Atualizacao - 2026-09-26 - Primeira execucao local confirmada

- O projeto ChaveRadar foi iniciado com sucesso no Visual Studio 2026.
- Ambiente virtual `.venv` ativo com Python 3.11.
- Django 5.2.17 instalado e validado.
- `python manage.py check` retornou sem problemas.
- `python manage.py runserver` iniciou corretamente em `http://127.0.0.1:8000/`.
- A pagina padrao do Django foi exibida no navegador, confirmando que a base local esta funcional.
- Proximo passo: criar a primeira app Django `leads` e substituir a pagina padrao por uma tela inicial simples do ChaveRadar.

---

## 26/09/2026 - Ambiente virtual validado e Django operacional

### Estado confirmado nesta interacao

- A `.venv` foi ativada com sucesso no Developer PowerShell; o prompt passou a exibir `(.venv)`.
- `python -m django --version` retornou **5.2.17**.
- `python manage.py check` retornou **System check identified no issues (0 silenced)**.
- O ambiente local do ChaveRadar esta funcional e pronto para iniciar o servidor de desenvolvimento.
- Proxima acao: executar `python manage.py runserver` e validar a primeira abertura do projeto no navegador.

## 26/09/2026 - Confirmado: terminal ainda usa Python global

### Estado confirmado nesta interacao

- O comando `python manage.py check` falhou com `ModuleNotFoundError: No module named 'django'`.
- O problema nao e a instalacao: o Django 5.2.17 foi instalado corretamente em `.venv`.
- O Developer PowerShell ainda esta usando o Python global da Microsoft Store, fora do ambiente virtual.
- Nao reinstalar o Django. A correcao e ativar a `.venv` no terminal com `.\.venv\Scripts\Activate.ps1` ou executar diretamente `.\.venv\Scripts\python.exe`.
- Depois da ativacao, o prompt deve iniciar com `(.venv)` e devem ser repetidos `python -m django --version` e `python manage.py check`.

## 26/09/2026 - Django instalado na .venv, mas PowerShell fora do ambiente

### Estado confirmado nesta interacao

- A criacao do ambiente virtual `.venv` foi concluida com sucesso.
- O `requirements.txt` instalou corretamente **Django 5.2.17**, `asgiref 3.12.1`, `sqlparse 0.6.0` e `tzdata 2026.4` dentro de `C:\Users\daniel.gusmao\source\repos\ChaveRadar\.venv`.
- O comando `python -m django --version` executado no Developer PowerShell retornou `No module named django` porque o terminal continuou usando o Python global da Microsoft Store, localizado em `AppData\Local\Microsoft\WindowsApps`, e nao o Python da `.venv`.
- Proxima acao: ativar o ambiente virtual no Developer PowerShell com `.\.venv\Scripts\Activate.ps1` e repetir `python -m django --version` e `python manage.py check`.
- Alternativa de validacao sem ativar o ambiente: `.\.venv\Scripts\python.exe -m django --version`.


# 00 - CHECKPOINT CUMULATIVO

> Este e o arquivo oficial de retomada do projeto. Qualquer LLM deve le-lo antes de propor alterações. Manter cumulativo, sem apagar decisões anteriores. Adicionar as atualizacoes mais recentes no topo.

## 26/09/2026 - Criacao do ambiente virtual no Visual Studio

### Estado confirmado nesta interacao

- O Visual Studio abriu a tela **Adicionar ambiente** para o projeto **ChaveRadar**.
- Tipo selecionado: **Ambiente virtual**.
- Interpretador de base confirmado: **Python 3.11**.
- O campo **Instalar pacotes do arquivo** ja aponta para `C:\Users\daniel.gusmao\source\repos\ChaveRadar\requirements.txt`.
- A opcao **Definir como ambiente atual** esta marcada e deve permanecer assim.
- Nao e necessario marcar **Definir como ambiente padrao para novos projetos**, **Exibir na janela de ambientes do Python** ou **Torne esse ambiente disponivel globalmente** para o MVP.
- Nome recomendado do ambiente: `.venv` em vez de `env`, para manter o padrao comum do projeto. Se o Visual Studio impedir o ponto, `env` tambem funciona.
- Proxima acao: clicar em **Criar**, aguardar a instalacao do Django a partir de `requirements.txt` e depois validar no Developer PowerShell com `python -m django --version` e `python manage.py check`.


## 26/09/2026 - Projeto criado no Visual Studio 2026

### Estado confirmado nesta interacao

- O projeto **ChaveRadar** foi criado com sucesso no Visual Studio 2026 Community.
- O Visual Studio esta usando **Python 3.11**.
- O template gerado pelo Visual Studio indica **Django 2.1.2**, uma versao antiga e inadequada para seguirmos no projeto atual.
- Nao instalar as dependencias antigas do template antes de atualizar `requirements.txt`.
- Padrao definido para o MVP: **Django 5.2 LTS**, compativel com Python 3.11.
- Primeiro passo apos a criacao: alterar `requirements.txt` para `Django>=5.2,<5.3` e somente depois criar o ambiente virtual pelo aviso **Criar ambiente virtual** do Visual Studio.
- Banco local continua sendo **SQLite** nesta fase; PostgreSQL sera configurado no deploy/hospedagem.
- Depois da criacao do ambiente virtual, validar com `python -m django --version` e executar o servidor local antes de iniciar telas ou modelos.

## 26/09/2026 - Nome definitivo e inicio no Visual Studio

### Decisao desta interacao

- O nome do projeto foi definido como **ChaveRadar**.
- Substituir o nome provisório **ChaveSinal** por **ChaveRadar** em documentação, interface e base técnica.
- Nome do pacote interno Django recomendado: `chaveradar`.
- O usuário está no Visual Studio 2026 Community, na tela **Criar um novo projeto**, com os templates Python/Django disponíveis.
- Para iniciar do zero pelo Visual Studio, selecionar **Projeto Web em Branco do Django** (não o template com páginas de exemplo), clicar em **Próximo** e usar **ChaveRadar** como nome do projeto e da solução.
- Próximo checkpoint esperado: confirmar a tela seguinte do Visual Studio e então configurar local, ambiente Python e criação do projeto sem avançar várias etapas de uma vez.

### Regra permanente de documentação

- `docs/00_CHECKPOINT.md` continua sendo o ponto oficial de retomada.
- Atualizar este arquivo **a cada interação do projeto**, colocando a atualização mais recente no topo e preservando o histórico necessário para qualquer LLM retomar o trabalho.

## 26/09/2026 - Checkpoint inicial consolidado

### Estado atual

- Projeto em fase de definicao e inicio do desenvolvimento.
- Naquele momento, o nome de trabalho/preferido era **ChaveSinal**; posteriormente o nome definitivo do projeto passou a ser **ChaveRadar**. O domínio ainda precisa ser registrado/validado.
- Ambiente do usuário: Windows + Visual Studio 2026 Community.
- Direcao escolhida: sistema **web responsivo**, acessível por computador e celular, sem depender de uma máquina Windows ligada para funcionar em produção.
- Primeiro formato mobile: **PWA/site responsivo**. Aplicativo Android nativo pode ser criado futuramente, reaproveitando o mesmo backend.
- Stack escolhida para o MVP: **Python + Django + Bootstrap**.
- Banco local: **SQLite** para facilitar o desenvolvimento.
- Banco hospedado: **PostgreSQL**.
- Versionamento: **GitHub**.
- Hospedagem inicial considerada: **Render**. Supabase foi considerado como opção de PostgreSQL gerenciado. Planos/preços devem ser revalidados antes do deploy.
- DNS: manter inicialmente no **Registro.br** e apontar diretamente para o Render. GitHub não recebe o DNS do sistema. Cloudflare e opcional e pode ser incluido depois.

### Objetivo do produto

Criar um sistema que receba comentários públicos relacionados a publicações imobiliarias, identifique sinais de interesse comercial e organize leads qualificados para compra, aluguel, financiamento, investimento, visita ou solicitacao de informações comerciais sobre imóveis.

O sistema deve funcionar como um pipeline auditavel:

`coleta/importacao -> publicação/imóvel -> comentário bruto -> classificação -> revisão -> lead -> relatorio`

### Regras de privacidade e operação

1. Trabalhar somente com dados públicos ou dados fornecidos legitimamente ao sistema.
2. Não procurar/enriquecer telefone, e-mail, renda, idade, profissão, localização pessoal ou outros dados fora do comentário público.
3. Não enviar mensagens, seguir usuários ou interagir automaticamente com perfis.
4. Comentario original deve ser preservado exatamente como capturado.
5. Não inventar nome, data, bairro, tipo de imóvel ou qualquer dado ausente.
6. Datas relativas exibidas pelo Instagram, como `4d`, `1w`, `56 sem` ou `3 min`, devem ser preservadas em campo proprio. Não converter para data exata como se fosse fato.
7. Se o nome de exibição não existir, usar o handle quando necessário para exibição.
8. Evitar duplicacao do mesmo comentário na mesma publicação.
9. O mesmo usuário pode gerar registros separados se comentar sobre imóveis/publicações diferentes.
10. O sistema precisa diferenciar **sem leads** de **sem dados suficientes**.

### Coleta de dados - decisão atual

A arquitetura e hibrida.

**Contas próprias/conectadas:** usar API oficial da Meta para contas profissionais quando configurada. Existem fluxos de Instagram Login e Facebook Login; a necessidade de Pagina do Facebook depende do fluxo utilizado. Quando aplicavel, usar coleta incremental e futuramente webhooks.

**Perfis de terceiros:** não projetar scraping automatizado. Entrada por importacao manual (colar, CSV ou Excel) ou por provedor licenciado que entregue os dados de forma compativel.

Conectores previstos:

- `InstagramOfficialConnector`
- `ManualImportConnector`
- `LicensedProviderConnector` (futuro)

### Regra central de modelagem

**Imovel/região pertencem a PUBLICACAO, não ao lead.**

Uma publicação pode representar, por exemplo:

- Tipo: Apartamento 2 quartos
- Regiao: Costa Azul
- Finalidade: Locacao

Todos os comentários daquela publicação herdam esse contexto, evitando que a IA tente adivinhar o imóvel apenas pelo texto do comentário.

### Entidades principais

- `Profile`: perfil imobiliário/corretor monitorado.
- `Publication`: post/reel e contexto do imóvel.
- `Comment`: comentário bruto imutavel.
- `Classification`: intenções, nivel, evidencia, confiança e revisão.
- `CollectionRun`: auditoria das coletas/importacoes.

### Classificacao de leads

**Alto**
- solicita visita/agendamento;
- pergunta se ainda está disponivel;
- manifestá interesse direto em comprar/alugar;
- informa que tentou contato.

**Médio**
- pergunta preço/valor;
- financiamento, FGTS, entrada;
- condomínio/IPTU;
- localização;
- quartos, metragem, garagem ou características.

**Baixo**
- pede informações genéricas sem demonstrar intenção clara.

**Não Lead**
- elogio sem intenção;
- marcacao generica de amigos;
- emojis isolados;
- corretor/imobiliaria/parceiro do setor;
- spam/publicidade/automatizado;
- comentário sem relação com o imóvel;
- duvida exclusivamente institucional;
- logística de evento sem intenção comercial.

### Intencoes sugeridas

`PRICE`, `CONDOMINIUM`, `IPTU`, `FINANCING`, `FGTS`, `DOWN_PAYMENT`, `LOCATION`, `BEDROOMS`, `AREA`, `GARAGE`, `AVAILABILITY`, `PHOTOS`, `FLOOR_PLAN`, `VISIT`, `SCHEDULING`, `DIRECT_PURCHASE_INTENT`, `DIRECT_RENT_INTENT`, `INVESTMENT`, `CONTACT_ATTEMPT`, `GENERIC_INFO`, `PROPERTY_FEATURE`.

A IA/regras detectam intenções. O nivel Alto/Médio/Baixo e calculado por regra de negocio determinística. `confidence` e separado do nivel do lead.

### Revisão humana

Estados previstos:

- Auto-aprovado
- Pendente de revisão
- Aprovado manualmente
- Rejeitado manualmente

A interface devera mostrar comentário, publicação/imóvel, intenção detectada, evidencia, nivel sugerido e confiança.

### Estratégia do classificador

Pipeline preferido:

`filtros baratos -> regras/regex -> IA apenas em casos ambiguos -> qualificação determinística`

Não enviar handle/nome/link do usuário ao modelo de IA quando o texto e contexto do imóvel forem suficientes. Associar o resultado ao comentário localmente.

### Importacao manual

O sistema devera permitir:

- colar comentários;
- importar CSV;
- importar Excel.

Antes de confirmar uma importacao, exibir contagem de registros novos, duplicados e inválidos.

Formato desejado de entrada:

- perfil_origem
- link_publicação
- data_publicação
- tipo_publicação
- descricao_publicação
- tipo_imóvel
- região
- finalidade
- handle_usuário
- nome_usuário
- comentário
- data_comentário

### Deduplicacao

1. API oficial: preferir `platform_comment_id`.
2. Importacoes sem ID: gerar `fingerprint` com perfil + publicação + handle + comentário original + data exibida original.

### Dashboard desejado

- perfis monitorados;
- publicações analisadas;
- comentários coletados/processados;
- leads encontrados;
- Alto/Médio/Baixo;
- pendentes de revisão;
- filtros por perfil, nivel e período;
- cobertura/ultima coleta por perfil;
- exportação Excel.

Exportacao futura sugerida com abas: `Resumo`, `Leads`, `Excluidos`, `Cobertura_Coleta`.

### Cobertura e limitacoes

Cada perfil deve registrar status de coleta/importacao, ultima atualização, quantidades encontradas, novas, duplicadas e falhas. Nunca interpretar falta de acesso como ausência de leads.

### Caso @danielgusmao1

O perfil `@danielgusmao1` foi informado para uma tentativa de análise publica. O ambiente não conseguiu acessar comentários verificáveis do Instagram. Nenhum dos comentários de referencia abaixo foi atribuido a esse perfil. Estado correto: **dados insuficientes/não verificáveis**, e não "perfil sem leads".

### Hospedagem e domínio

Fluxo inicial previsto:

`Registro.br -> DNS do Registro.br -> Render -> Django -> PostgreSQL`

- GitHub guarda o código e não recebe o DNS.
- Cloudflare e opcional; pode ser adicionado depois sem reconstruir o sistema.
- O Render foi escolhido como primeira opção por simplicidade para o MVP.
- Para desenvolvimento/teste, pode-se usar camada gratuita quando disponivel; para produção, revalidar limites e preços antes da contratacao.

### Mobile

Primeira etapa: site responsivo/PWA, instalavel na tela inicial do celular e reutilizando a mesma aplicação web.

Futuro Android nativo: criar interface em Flutter (ou equivalente) consumindo o mesmo backend/API Django. Não duplicar regras de negocio no aplicativo.

### Nomes discutidos

- ChaveSinal - nome provisório anterior
- ImobSinal
- IntenCasa
- ChaveRadar - **nome definido**
- RadarMorar
- MoraSinal
- ImobIntent

O nome do projeto já foi definido como **ChaveRadar**; a disponibilidade do domínio e a situação da marca ainda devem ser validadas antes do uso público.

### Ordem de implementacao aprovada

**MVP 1 - cérebro do produto**

Importacao manual -> banco -> contexto do imóvel -> classificador -> revisão -> dashboard -> Excel.

**MVP 2 - Meta API**

Contas próprias/conectadas -> coleta oficial automatizada -> mesmo pipeline.

**MVP 3 - operação**

Webhooks, provedor licenciado, autenticação completa, CRM, relatórios recorrentes e app nativo se houver necessidade.

### Proximo passo recomendado

Executar está base localmente no Visual Studio, validar o dashboard inicial e depois implementar a primeira tela real: **Importar comentários**.

## Regra permanente de documentacao

A partir deste checkpoint:

1. `docs/00_CHECKPOINT.md` e a fonte principal para retomada por humanos ou LLMs.
2. Toda interação do projeto deve adicionar uma nova entrada no topo com data, decisões, alterações, pendências e próximo passo.
3. Não apagar contexto histórico necessário para entender decisões anteriores.
4. Alteracoes de arquitetura devem ser refletidas também nos documentos temáticos da pasta `docs/`.
5. Se o chat for perdido, qualquer LLM deve conseguir continuar lendo `README.md` e `docs/00_CHECKPOINT.md`.
