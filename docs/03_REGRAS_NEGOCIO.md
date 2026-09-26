# 03 - Regras de negocio

## Alto

Visita/agendamento, disponibilidade, interesse direto em compra/aluguel ou tentativa de contato.

## Médio

Preco, financiamento, FGTS, entrada, condomínio, IPTU, localização, quartos, metragem, garagem e características do imóvel.

## Baixo

Pedido genérico de informações sem intenção mais especifica.

## Excluir

Elogios, marcacoes genéricas, emojis isolados, profissionais/parceiros do setor, spam, comentários sem relação, dúvidas institucionais e logística de eventos sem intenção comercial.

## Preservacao

- `text_original` e imutavel.
- Data relativa fica em `displayed_daté_original`.
- Ausencia de dado permanece ausência; não inferir.
- Imovel/região vem da publicação ou de dado explicitamente importado.

## Reprocessamento

Toda classificação deve registrar versão das regras/classificador para permitir reprocessamento futuro sem recoleta.
