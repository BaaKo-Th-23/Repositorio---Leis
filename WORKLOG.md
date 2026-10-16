# Continuação da coleta

Objetivo: completar o escopo de `scripts/plano.py`, preservando as fontes oficiais,
os originais, o vocabulário canônico e a publicação incremental por lote. Metas
estimadas não comprovam cobertura integral; não reduzir metas para declarar 100%.

## Checkpoint de 15/10/2026

- Início desta continuação em `ce6ebc92fb6`, com arquivos coletados ainda sem commit.
- Coletores existentes confirmados vivos: decretos federais (DEC-sn, seguido de
  DEC-n), DOU 2025 com fila até 2002, DF, GO, SP, MT, RS, PE, BA, PA, ES seguido
  de SE, SC e simulação do reprocessamento de OCR. Não iniciar duplicatas.
- Três agentes Sol Low: federal, estados, municipal/jurisprudência. Coordenação,
  DOU, utilitários compartilhados, auditoria e publicação ficam no agente principal.
- MS encerrou 22.988 itens do índice sem erros, segundo o log local; falta auditar
  o lote antes da publicação.
- Próximas frentes: corrigir lacunas silenciosas do DOU, deduplicar índice de SP,
  alcançar o calendário público municipal e localizar súmulas vinculantes oficiais.
- Publicação: commits normais por lote; preservar histórico e nunca reconstruir ou
  fazer force-push. Não incluir atribuição automática a assistentes em commits.

## Critério de conclusão

Conferir cada item do plano contra o índice oficial disponível, os arquivos e os
registros de falha; verificar formato, datas, proveniência e texto. Fonte bloqueada,
índice incompleto ou universo apenas estimado permanece como pendência explícita.
O último relatório disponível é antigo e será regenerado após a auditoria do lote.

## Publicação e progresso

A pedido do usuário, todo commit deve regenerar `PROGRESSO.md` e `progresso.svg`
contando o index do Git (`scripts/progresso.py --git-index`), para não contabilizar
downloads que ainda não entraram no lote publicado. O hook `.githooks/pre-commit`
faz isso automaticamente; ativar neste clone com `rtk git config core.hooksPath .githooks`.

- Publicado `d33d9207bf8`: 12.206 decretos de MS que ainda não estavam no histórico.
  A auditoria de todos os 22.988 Markdown de MS passou; oito não têm data na fonte.
- DOU antigo foi encerrado e retomado com correções de índice, tipos descartados e
  colisão de nomes. Fila ativa 2026–2002: Python PID 87026, fila PID 87017.
- Lacunas novas resolvidas pelos agentes: Câmara/Senado via Legin, três regimentos,
  temas repetitivos STJ, súmulas TCU, calendário municipal histórico, constituições
  PA/TO, edição histórica CE e portal histórico de leis TO. Validar antes de publicar.
