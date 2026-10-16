# Continuação da coleta

Objetivo: completar o escopo de `scripts/plano.py`, preservando as fontes oficiais,
os originais, o vocabulário canônico e a publicação incremental por lote. Metas
estimadas não comprovam cobertura integral; não reduzir metas para declarar 100%.

## Estado atual verificado — 15/10/2026, terceiro lote estadual

- Main publicado anterior: `517db958cd0`, 627.980 documentos, relatório GitHub
  conferido por hash. Novo snapshot estadual: 36.694 Markdown adicionados,
  24 removidos por substituição/migração/duplicação e 57 modificados; saldo
  36.670, total 664.650 documentos. Nenhuma pasta fora do plano.
- Constituições: uma edição selecionada para cada uma das 27 UFs, com fonte
  institucional e original preservado. Fontes melhores de AL/MA/PB/PE/PI/RR/RJ;
  RJ inclui 84 seções e ADCT. Edições anteriores da mesma constituição foram
  arquivadas em _referencias, não contadas como constituições históricas.
  Não afirmar atualização vigente em 2026 para edições antigas ou incertas.
- MA: 54 emendas tiveram metadados próprios corrigidos com corpo verificado
  por SHA; duas duplicatas mal datadas removidas, fontes preservadas. EC74
  migrou de 2006 para 2016 pela assinatura, sem confundir citação de outra lei.
- PR: recuperadas as sete emendas 55–61 por rota pública oficial com originais
  preservados. Essas emendas e as recentes de outras UFs são atos separados;
  incorporação às compilações antigas não foi comprovada.
- Auditoria de 36.753 Markdown encontrou três defeitos: dois corpos vazios de
  MG excluídos com pendências explícitas/cache preservado e dois NUL de cauda
  no DF removidos. Reparos direcionados no índice passaram; seis scripts válidos.
- Scripts estaduais MA/SAPL/SPL/PR/MG/DF corrigem identidade, data própria, calendário
  e escolha da constituição já selecionada. Preservar os coletores ativos.
- Próximo lote: municipal, scripts SAPL e seis súmulas TNU 84–89 conferidas no
  manual oficial CJF, incluindo cancelamento da 86. Agentes continuam federal,
  estadual e municipal/jurisprudência sem operações Git.
- Percentuais usam somente séries com meta. Universo nacional de decretos
  legislativos e resoluções municipais continua desconhecido. Índice completo
  não prova texto completo, e metas estimadas não provam conclusão jurídica.

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
- Jurisprudência commitada em `d23aac7a94a`, relatório de 554.596 documentos,
  sem pastas órfãs. Os 7.048 Markdown novos/alterados passaram no auditor.
- Lote municipal preparado: 10.736 Markdown adicionados, 419 alterados e 135
  caminhos antigos removidos; acréscimo líquido de 10.601. Os 11.155 documentos
  passaram em formato/datas e confronto de município/rota/código com IBGE.
- MG retomado PID 17384, sessão 62271: catálogo de 101.777 atos únicos, quatro
  duplicatas do CSV identificadas; XML bruto e HTML preservados, sem duplicata de
  coletor. Orgânicas SAPL: fila PID 17034, sessão 89650, catálogo SIGI de 1.155
  serviços em 1.151 municípios, identidade IBGE validada antes da coleta.
- RFB revelou limite de janela da API: 1.153 páginas retornaram apenas 50.000 IDs
  únicos de 115.238. Índice segue incompleto; particionar por ano antes de afirmar
  cobertura. Coletor bulk mantém uso exclusivo da quota do host.
- Primeiro push estadual caiu durante preparação do pack; remoto continuava em
  `808531961dd`. Tentativa encerrada e substituída por envio com keepalive SSH,
  janela de deltas desativada e log `_log_push_lotes.txt`, sessão 34699. Confirmar
  conclusão/remoto antes de repetir qualquer envio; não usar force-push.

## Publicação confirmada — 15/10/2026

- `5fd5a8b4e83`, `d23aac7a94a` e `6e5a9d618c9` enviados normalmente ao main.
  Primeiro retry concluiu até jurisprudência; envio incremental municipal concluiu
  depois. API GitHub confirmou PROGRESSO idêntico ao blob do HEAD
  `b218aa489221a6c14ad3deecdbfefbc2c301fbdb`: 565.197 / ~11.768.329 (4,8%).
  Os três commits contêm PROGRESSO.md e progresso.svg. Nenhuma reescrita publicada.
- Coletas verificadas vivas após publicação: municipal 12292, orgânicas 17034,
  MG 17384, RJ constitucional 15868 e RFB 20649. Revalidar antes de retomar.
- RFB agora indexa partições anuais, uso exclusivo de 4 rps; mais de 61 mil IDs
  únicos no snapshot, ainda sem comprovar todos os 115.238. Não declarar completo.
- Federal: relatório durável mais recente
  `federal/_fonte/auditorias/falhas-federais-20261015-224658.json.gz` registra 5.992
  pendências reais naquele snapshot. LCP e LCT resolvidas; lote ainda não publicado.
- Próximo passo de publicação: federal/RFB novos, correções de URN, oito decretos
  MA e novos lotes MG/SP/SC e municipais, sempre auditoria do index antes do commit.
  Agentes continuam em RFB/federal, RJ/estados e legislação municipal via SAPL.

## Publicação e progresso

### Lote federal seguinte — 15/10/2026

- Preparado acréscimo líquido de 14.642 Markdown: federal 14.692 adicionados,
  756 alterados e 78 caminhos antigos removidos; tratados 28 adicionados. Auditoria
  de 15.476 documentos passou, com 28 datas ausentes explícitas. Diff passou e seis
  scripts preparados têm sintaxe válida; nenhum caminho fora do plano.
- Leis constitucionais da Carta de 1937 incluídas no plano com meta oficial 21:
  catálogo Planalto Quadro_Lct.htm contém exatamente LCT001–LCT021 e coincide com
  o índice Senado. Não é meta reduzida ao volume coletado.
- DOU segue no PID 96622; saída atual é sessão 17222, não `_log_dou.txt` antigo.
  Poll confirmado até 23/02/2025, 1.645 novos e zero erros naquele snapshot.
  O log antigo tem mtime anterior ao processo e não serve para diagnosticar parada.
- RFB índice anual ainda em progresso, mais de 74 mil IDs únicos; não confundir
  resultado parcial com cobertura completa de 115.238. Corpo já salvo é publicável.
- Próxima correção de metadados federais: explicitar complemento/reedição no número
  oficial sem alterar corpos. Publicação atual conserva títulos/URNs corretos.

### Lote estadual seguinte e catálogo RFB

- Federal publicado em `6b9308d1da3`, push confirmado até esse SHA.
- Lote estadual preparado: 34.488 Markdown novos e quatro com data de obtenção
  atualizada; auditoria de 34.492 encontrou somente a publicação 02/03/2054 no
  cadastro PE 76732. Valor bruto/publicação original preservados, data_publicacao
  vazia sem inferir 2024; caso corrigido revalidado. Diff passou; parsers preparados
  têm sintaxe válida, incluindo proteção PE contra calendário inválido/futuro.
- Metas federais atualizadas pelos registros e URNs únicos dos índices oficiais:
  LEI 16.883 (16.749 numeradas + 134 não numeradas), LCP 239, DEL 12.378
  (12.369 DEL + nove DEL-mpv). Não usar estimativas antigas inferiores ao acervo.
- RFB índice anual agora cobre 115.238 IDs únicos em 227 anos e declara completo;
  isso é índice, não 115.238 textos convertidos. Publicação do lote de textos está
  retida para revisar deduplicação: exige identidade oficial além de corpo/DOU
  da publicação própria. URL meramente citada no corpo não prova equivalência.
- Novas categorias municipais (decretos legislativos e resoluções) precisam de
  suporte a universo nacional desconhecido no progresso; não extrapolar de duas
  Câmaras nem baixar as metas existentes. Próximo ciclo espera orgânicas 17034,
  PID 28620/sessão 37711, abortando se os caminhos ainda não estiverem no plano.

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
