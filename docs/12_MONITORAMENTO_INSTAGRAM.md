# 12 - Monitoramento de perfis do Instagram

## Objetivo

Permitir ao administrador manter uma lista independente de contas que o ChaveRadar pretende acompanhar diariamente.

## Cadastro

Cada alvo de monitoramento possui:

- handle do Instagram;
- nome/apelido opcional;
- ativo/pausado;
- alertas habilitados/desabilitados;
- palavras-chave adicionais por perfil;
- observacoes;
- ultima verificacao e status tecnico da coleta.

## Edicao e exclusao

A lista pode ser editada e excluida pela interface. A exclusao remove apenas o **alvo de monitoramento**. Nao apaga `Profile`, publicacoes, comentarios, classificacoes ou leads historicos ja armazenados.

Essa separacao e intencional para evitar perda de historico por uma simples alteracao na lista de contas acompanhadas.

## Alertas

`alerts_enabled` prepara o perfil para gerar alertas quando uma coleta real encontrar comentario relevante. O mecanismo de alerta sera ligado ao conector de coleta e ao classificador.

## Limitacao atual

Cadastrar `@perfil` na lista nao concede acesso automatico aos comentarios dessa conta. A coleta real dependera de uma fonte permitida: API oficial Meta quando aplicavel ou provedor licenciado. O sistema nao deve usar scraping nao autorizado.
