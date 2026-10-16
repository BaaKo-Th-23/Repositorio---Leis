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

## Checkpoint de publicação e correções — 15/10/2026 à noite

- Último lote publicado: `808531961dd`, 25.489 novos atos do DOU. O relatório
  publicado registra 423.667 documentos; ainda não comprova cobertura integral.
- Federal e jurisprudência anteriores publicados em `8dc1d518aea` e `8431a0f1642`.
- Próximo lote estadual: correções de datas comprovadas na própria epígrafe,
  revogação de SC conferida com os HTML originais, recuperação de imagens/Word e
  constituições oficiais com edição explicitada. Dois decretos PA (3.323 e 3.324/2023)
  continuam com binários oficiais corrompidos e aviso explícito de texto indisponível.
- PDF Vision: reprocessamento integral pendente; simulação antiga foi interrompida
  após colisões no mapa de originais. O mapa agora inclui a jurisdição. O serviço
  nativo ANE estava preso; não substituir textos existentes em massa sem validação.
- Filas federais: decretos PID 7371 a 3 rps; complementos ausentes em cliente separado
  limitado a 1 rps. DOU PID 87026, fila 87017. Confirmar processos antes de retomadas.
- Filas estaduais retomadas com cache; SP/PE tiveram DNS restabelecido. O agente
  estadual controla substituição de SP para carregar suporte a PDF. Não duplicar.
- Municipal: fila PID 4998; agente confere limites oficiais de circulação antes de
  retomar o filho. Jurisprudência BNP: 7.139 IDs / 7.207 registros, incluindo 68
  variantes ADI preservadas no mesmo documento, conferidos integralmente com caches.
- RFB: catálogo normativo oficial declara 115.238 itens em 23 espécies; índice ainda
  parcial. Coleta retomável e equivalências por corpo integral evitam duplicatas.
- Metas municipais ajustadas ao cadastro oficial IBGE de 5.571 municípios. TNU
  uniformização tem item próprio, separado de súmulas. Nenhuma meta é reduzida ao
  volume coletado para simular conclusão.

## Lotes seguintes — 15/10/2026

- Commit estadual `5fd5a8b4e83`: acréscimo líquido de 124.319 registros; relatório
  de 547.986 / ~11.768.329. Auditoria dos 136.927 Markdown novos/alterados
  encontrou uma data de citação em SC; corrigida para 31/07/1975 conforme metadado,
  epígrafe e assinatura, número 670, corpo preservado. Verificação focada passou.
  Diff completo passou. Datas ausentes permanecem explícitas em 7.487 registros.
- Hook de progresso usa `rtk proxy git add` para evitar calcular novamente o diff
  completo apenas para resumir o comando de inclusão dos dois relatórios.
- Municipal: fila atual 12292/12301, com limites comprovados nos cards oficiais e
  históricos preservados. Nova frente de orgânicas SAPL valida identidade no IBGE;
  descoberta usa catálogo oficial SIGI/Interlegis, sem adivinhar domínios.
- SC retomado com parser corrigido no PID 15440; RJ constitucional PID 15868,
  índice de 84 seções completo, documento final ainda pendente de texto e ADCT.
- Federal: histórico de falhas auditado offline, 2.172 registros já resolvidos e
  6.034 pendências reais naquele snapshot. Relatórios preservados no cache de
  auditorias; preencher URNs equivalentes não altera os corpos. Série Planalto DPL
  de 175 URLs é recorte histórico, não prova cobertura dos 5.831 DPL do índice.
- Próximo lote jurisprudência inclui BNP com decisões variantes preservadas e
  83 súmulas TNU da edição oficial histórica de 2016; situação atual não inferida.

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
