# Progresso

Gerado por `scripts/progresso.py` em 15/10/2026. O escopo está em
`scripts/plano.py`; os números de **meta** são estimativas do tamanho de cada série, não
contagens oficiais. Séries encerradas (decretos-leis, leis delegadas) marcam 100%.

**331.490 de ~11.525.718 normas — 2.9%**

![progresso](progresso.svg)

## Fase 1 — esfera federal completa

Fonte única (normas.leg.br, Planalto, Senado). **328.001 de ~573.632 — 57.2%**

### Constituição Federal — 180 / ~180 (100%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| ✅ | Constituição de 1988 (texto vigente) | 1 | 1 | `constituicao.md` | https://www.planalto.gov.br |
| ✅ | Constituições históricas (1824, 1891, 1934, 1937, 1946, 1967, 1969) | 7 | 7 | `federal/constituicoes-historicas` | https://www.planalto.gov.br |
| ✅ | Emendas constitucionais e de revisão | 172 | 172 | `federal/emendas-constitucionais` | https://normas.leg.br |

### Leis federais — 29.184 / ~29.200 (100%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| ✅ | Leis ordinárias (1822–hoje) | 16.684 | 16.700 | `federal/leis-ordinarias` | Senado (índice) + normas.leg.br (texto) |
| ✅ | Leis complementares | 237 | 237 | `federal/leis-complementares` | normas.leg.br |
| ✅ | Leis delegadas (série encerrada) | 13 | 13 | `federal/leis-delegadas` | normas.leg.br |
| ✅ | Decretos-leis (série encerrada em 1988) | 12.250 | 12.250 | `federal/decretos-lei` | normas.leg.br |

### Atos do Congresso — 3.968 / ~37.448 (11%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| 🟦 | Decretos legislativos | 3.158 | 21.775 | `federal/decretos-legislativos` | normas.leg.br |
| 🟦 | Medidas provisórias (originais e reedições) | 810 | 7.497 | `federal/medidas-provisorias` | Planalto + normas.leg.br |
| ⬜️ | Resoluções do Senado Federal | 0 | 6.578 | `federal/resolucoes-senado` | normas.leg.br |
| ⬜️ | Resoluções da Câmara dos Deputados | 0 | 1.500 | `federal/resolucoes-camara` | camara.leg.br |
| ⬜️ | Resoluções do Congresso Nacional e da Revisão Constitucional | 0 | 95 | `federal/resolucoes-congresso` | normas.leg.br |
| ⬜️ | Regimentos internos (Senado, Câmara, Congresso) | 0 | 3 | `federal/regimentos` | senado.leg.br, camara.leg.br |

### Decretos do Executivo federal — 5 / ~153.657 (0%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| ⬜️ | Decretos numerados (1889–hoje, as duas séries) | 0 | 139.127 | `federal/decretos` | normas.leg.br + Planalto |
| ⬜️ | Decretos não numerados | 0 | 14.510 | `federal/decretos-nao-numerados` | Planalto |
| 🟦 | Regulamentos consolidados (RIR, RIPI, Aduaneiro, RPS, PAF) | 5 | 20 | `federal/regulamentos` | Planalto |

### Tratados internacionais — 0 / ~5.680 (0%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| ⬜️ | Decretos de promulgação de tratados | 0 | 4.000 | `tratados/decretos` | Concórdia/MRE + Planalto |
| ⬜️ | Tratados de direitos humanos (status constitucional/supralegal) | 0 | 40 | `tratados/direitos-humanos` | MRE + Planalto |
| ⬜️ | Convenções da OIT ratificadas | 0 | 100 | `tratados/oit` | ilo.org + MTE |
| ⬜️ | Acordos de bitributação | 0 | 40 | `tratados/bitributacao` | RFB |
| ⬜️ | Normas do Mercosul internalizadas | 0 | 1.500 | `tratados/mercosul` | mercosur.int |

### Leis estaduais e distritais — 294.664 / ~347.467 (85%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| 🟦 | Constituições estaduais e Lei Orgânica do DF | 23 | 27 | `estaduais/*/constituicao`, `estaduais/*/lei-organica` | Assembleias e Casas Civis |
| 🟦 | Constituições estaduais históricas | 4 | 40 | `estaduais/*/constituicoes-historicas` | Assembleias |
| 🟦 | Emendas constitucionais estaduais | 2.013 | 2.200 | `estaduais/*/emendas-constitucionais` | Assembleias |
| 🟦 | Leis ordinárias estaduais | 273.000 | 330.000 | `estaduais/*/leis-ordinarias` | 19 scripts, uma fonte por UF |
| 🟦 | Leis complementares estaduais | 12.361 | 14.000 | `estaduais/*/leis-complementares` | 19 scripts, uma fonte por UF |
| ✅ | Decretos-leis e leis delegadas estaduais | 6.676 | 600 | `estaduais/*/decretos-lei`, `estaduais/*/leis-delegadas`, `estaduais/*/decretos-lei-complementares` | Assembleias |
| 🟦 | Leis promulgadas, constitucionais e emendas à Lei Orgânica | 587 | 600 | `estaduais/*/leis-promulgadas`, `estaduais/*/leis-constitucionais`, `estaduais/*/emendas-lei-organica` | Assembleias |

## Fase 2 — infralegal e jurisprudência

Uma fonte por órgão, agência ou tribunal. **3.489 de ~619.376 — 0.6%**

### Infralegal — tributário — 24 / ~35.600 (0%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| 🟦 | Instruções normativas da Receita Federal | 1 | 2.600 | `reguladores/rfb/instrucoes-normativas` | Diário Oficial da União (in.gov.br) |
| 🟦 | Portarias e atos declaratórios da RFB | 19 | 9.000 | `reguladores/rfb/portarias` | Diário Oficial da União (in.gov.br) |
| ⬜️ | Soluções de consulta e divergência (COSIT) | 0 | 8.000 | `reguladores/rfb/solucoes-cosit` | normas.receita.fazenda.gov.br |
| ⬜️ | Pareceres normativos | 0 | 200 | `reguladores/rfb/pareceres-normativos` | Diário Oficial da União (in.gov.br) |
| 🟦 | Súmulas e resoluções do CARF | 1 | 300 | `reguladores/carf` | Diário Oficial da União (in.gov.br) |
| ⬜️ | Convênios, protocolos e ajustes SINIEF (CONFAZ) | 0 | 12.000 | `reguladores/confaz` | confaz.fazenda.gov.br |
| 🟦 | Portarias e instruções da STN | 3 | 2.000 | `reguladores/stn` | Diário Oficial da União (in.gov.br) |
| ⬜️ | Normas da PGFN | 0 | 1.500 | `reguladores/pgfn` | Diário Oficial da União (in.gov.br) |

### Infralegal — trânsito e transportes — 226 / ~10.097 (2%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| ⬜️ | Resoluções do CONTRAN | 0 | 1.050 | `reguladores/contran/resolucoes` | Diário Oficial da União (in.gov.br) |
| ⬜️ | Deliberações do CONTRAN | 0 | 300 | `reguladores/contran/deliberacoes` | Diário Oficial da União (in.gov.br) |
| 🟦 | Portarias do DENATRAN/SENATRAN | 32 | 1.500 | `reguladores/senatran` | Diário Oficial da União (in.gov.br) |
| ⬜️ | Manual Brasileiro de Sinalização de Trânsito (volumes I–VII) | 0 | 7 | `reguladores/contran/sinalizacao` | CONTRAN — MBST |
| 🟦 | Resoluções da ANTT | 22 | 6.000 | `reguladores/antt` | Diário Oficial da União (in.gov.br) |
| 🟦 | Resoluções da ANTAQ | 54 | 500 | `reguladores/antaq` | Diário Oficial da União (in.gov.br) |
| 🟦 | Resoluções e RBAC da ANAC | 118 | 700 | `reguladores/anac` | Diário Oficial da União (in.gov.br) |
| ⬜️ | Normas da Autoridade Marítima (NORMAM) | 0 | 40 | `reguladores/normam` | marinha.mil.br/dpc |

### Infralegal — saúde — 219 / ~37.700 (1%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| ⬜️ | Resoluções da diretoria colegiada (RDC) da ANVISA | 0 | 1.100 | `reguladores/anvisa/rdc` | anvisa.gov.br |
| ⬜️ | Instruções normativas e portarias da ANVISA | 0 | 2.000 | `reguladores/anvisa/outros` | Diário Oficial da União (in.gov.br) |
| 🟦 | Portarias do Ministério da Saúde (GM/MS e consolidadas) | 209 | 30.000 | `reguladores/ms/portarias` | saude.gov.br — SAGE/Saúde Legis |
| ⬜️ | Resoluções do Conselho Nacional de Saúde | 0 | 700 | `reguladores/cns` | Diário Oficial da União (in.gov.br) |
| 🟦 | Resoluções normativas da ANS | 10 | 600 | `reguladores/ans` | Diário Oficial da União (in.gov.br) |
| ⬜️ | Resoluções do CFM e pareceres | 0 | 2.500 | `reguladores/cfm` | Diário Oficial da União (in.gov.br) |
| ⬜️ | Resoluções do COFEN | 0 | 800 | `reguladores/cofen` | Diário Oficial da União (in.gov.br) |

### Infralegal — trabalho e previdência — 58 / ~4.598 (1%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| ⬜️ | Normas regulamentadoras (NR-1 a NR-38) | 0 | 38 | `reguladores/mte/nr` | gov.br/trabalho |
| 🟦 | Portarias do Ministério do Trabalho | 6 | 3.000 | `reguladores/mte/portarias` | Diário Oficial da União (in.gov.br) |
| 🟦 | Instruções normativas do INSS | 9 | 160 | `reguladores/inss` | Diário Oficial da União (in.gov.br) |
| 🟦 | Instruções normativas e portarias da SPREV | 13 | 900 | `reguladores/sprev` | Diário Oficial da União (in.gov.br) |
| 🟦 | Resoluções e instruções da PREVIC | 30 | 400 | `reguladores/previc` | Diário Oficial da União (in.gov.br) |
| ⬜️ | Enunciados e súmulas do CRPS | 0 | 100 | `reguladores/crps` | Diário Oficial da União (in.gov.br) |

### Infralegal — meio ambiente — 178 / ~8.620 (2%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| ⬜️ | Resoluções do CONAMA | 0 | 520 | `reguladores/conama` | Diário Oficial da União (in.gov.br) |
| 🟦 | Instruções normativas e portarias do IBAMA | 2 | 1.500 | `reguladores/ibama` | Diário Oficial da União (in.gov.br) |
| 🟦 | Instruções normativas do ICMBio | 11 | 400 | `reguladores/icmbio` | Diário Oficial da União (in.gov.br) |
| 🟦 | Resoluções da ANA e do CNRH | 4 | 3.000 | `reguladores/ana` | Diário Oficial da União (in.gov.br) |
| ⬜️ | Instruções normativas do SFB e do Serviço Florestal | 0 | 200 | `reguladores/sfb` | Diário Oficial da União (in.gov.br) |
| 🟦 | Instruções normativas do MAPA (agropecuária) | 161 | 3.000 | `reguladores/mapa` | gov.br/agricultura — SISLEGIS |

### Infralegal — financeiro — 100 / ~17.300 (1%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| ⬜️ | Resoluções do CMN | 0 | 5.200 | `reguladores/bcb/resolucoes-cmn` | Diário Oficial da União (in.gov.br) |
| ⬜️ | Resoluções e circulares do Banco Central | 0 | 5.000 | `reguladores/bcb/resolucoes-bcb` | Diário Oficial da União (in.gov.br) |
| 🟦 | Instruções e resoluções da CVM | 2 | 500 | `reguladores/cvm` | Diário Oficial da União (in.gov.br) |
| 🟦 | Circulares e resoluções da SUSEP e do CNSP | 58 | 1.200 | `reguladores/susep` | Diário Oficial da União (in.gov.br) |
| ⬜️ | Resoluções do CADE e do COAF | 0 | 400 | `reguladores/cade-coaf` | Diário Oficial da União (in.gov.br) |
| ⬜️ | Resoluções e pronunciamentos do CFC e do CPC | 0 | 3.000 | `reguladores/cfc-cpc` | Diário Oficial da União (in.gov.br) |
| 🟦 | Resoluções e instruções do INMETRO | 40 | 2.000 | `reguladores/inmetro` | Diário Oficial da União (in.gov.br) |

### Infralegal — infraestrutura e energia — 17 / ~4.400 (0%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| 🟦 | Resoluções normativas e homologatórias da ANEEL | 10 | 2.000 | `reguladores/aneel` | Diário Oficial da União (in.gov.br) |
| 🟦 | Resoluções da ANP | 4 | 1.000 | `reguladores/anp` | Diário Oficial da União (in.gov.br) |
| 🟦 | Resoluções e atos da ANATEL | 2 | 800 | `reguladores/anatel` | Diário Oficial da União (in.gov.br) |
| 🟦 | Resoluções da ANM (mineração) | 1 | 300 | `reguladores/anm` | gov.br/anm |
| ⬜️ | Resoluções do CNPE e do CMSE | 0 | 300 | `reguladores/cnpe` | Diário Oficial da União (in.gov.br) |

### Infralegal — educação e cultura — 125 / ~7.400 (2%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| 🟦 | Resoluções e pareceres do CNE | 4 | 1.500 | `reguladores/cne` | Diário Oficial da União (in.gov.br) |
| 🟦 | Portarias do MEC e do INEP | 113 | 4.000 | `reguladores/mec` | Diário Oficial da União (in.gov.br) |
| 🟦 | Instruções normativas e portarias da CAPES | 8 | 1.000 | `reguladores/capes` | Diário Oficial da União (in.gov.br) |
| ⬜️ | Instruções normativas da ANCINE e do IPHAN | 0 | 900 | `reguladores/ancine-iphan` | Diário Oficial da União (in.gov.br) |

### Infralegal — justiça e eleições — 0 / ~11.600 (0%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| ⬜️ | Resoluções e instruções do TSE | 0 | 5.000 | `reguladores/tse` | Diário Oficial da União (in.gov.br) |
| ⬜️ | Resoluções, provimentos e recomendações do CNJ | 0 | 1.200 | `reguladores/cnj` | Diário Oficial da União (in.gov.br) |
| ⬜️ | Resoluções e recomendações do CNMP | 0 | 400 | `reguladores/cnmp` | Diário Oficial da União (in.gov.br) |
| ⬜️ | Provimentos e resoluções do Conselho Federal da OAB | 0 | 800 | `reguladores/oab` | Diário Oficial da União (in.gov.br) |
| ⬜️ | Resoluções do CONFEA/CREA e demais conselhos profissionais | 0 | 3.000 | `reguladores/conselhos-profissionais` | Diário Oficial da União (in.gov.br) |
| ⬜️ | Instruções normativas e portarias da CGU | 0 | 1.200 | `reguladores/cgu` | Diário Oficial da União (in.gov.br) |

### Jurisprudência vinculante — 2.542 / ~14.007 (18%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| ⬜️ | Súmulas vinculantes do STF | 0 | 59 | `jurisprudencia/stf/sumulas-vinculantes` | stf.jus.br — caderno ainda não localizado |
| ✅ | Súmulas do STF | 736 | 736 | `jurisprudencia/stf/sumulas` | stf.jus.br |
| ⬜️ | Temas de repercussão geral | 0 | 1.400 | `jurisprudencia/stf/repercussao-geral` | stf.jus.br |
| ⬜️ | Controle concentrado com eficácia erga omnes (ADI, ADC, ADPF, ADO) | 0 | 8.000 | `jurisprudencia/stf/controle-concentrado` | stf.jus.br |
| ✅ | Súmulas do STJ | 649 | 649 | `jurisprudencia/stj/sumulas` | stj.jus.br |
| ⬜️ | Temas de recursos repetitivos (STJ) | 0 | 1.300 | `jurisprudencia/stj/repetitivos` | stj.jus.br |
| ✅ | Súmulas e orientações jurisprudenciais do TST | 1.157 | 1.157 | `jurisprudencia/tst` | tst.jus.br |
| ⬜️ | Súmulas do TCU, TNU, STM e TSE | 0 | 700 | `jurisprudencia/outros-tribunais` | tcu.gov.br, cjf.jus.br, stm.jus.br, tse.jus.br |
| ⬜️ | Regimentos internos dos tribunais superiores | 0 | 6 | `jurisprudencia/regimentos` | portais dos tribunais |

### Infralegal estadual — 0 / ~468.054 (0%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| ⬜️ | Decretos dos governadores (27 UF) | 0 | 400.000 | `estaduais/*/decretos` | Casas Civis e diários oficiais estaduais |
| ⬜️ | Regulamentos do ICMS (RICMS das 27 UF) | 0 | 27 | `estaduais/*/regulamentos` | Secretarias de Fazenda |
| ⬜️ | Instruções normativas e portarias das SEFAZ | 0 | 50.000 | `estaduais/*/instrucoes-normativas` | Secretarias de Fazenda |
| ⬜️ | Resoluções e decisões normativas dos TCE | 0 | 10.000 | `estaduais/*/resolucoes-tce` | Tribunais de Contas estaduais |
| ⬜️ | Resoluções e provimentos dos TJ e das Corregedorias | 0 | 8.000 | `estaduais/*/resolucoes-tj` | Tribunais de Justiça |
| ⬜️ | Regimentos internos das Assembleias | 0 | 27 | `estaduais/*/regimentos` | Assembleias |

## Fase 3 — direito municipal

5.570 fontes, sem índice central. **0 de ~10.332.710 — 0.0%**

### Legislação municipal — 0 / ~10.332.710 (0%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| ⬜️ | Leis orgânicas municipais | 0 | 5.570 | `municipais/*/*/lei-organica` | portais municipais e Leis Municipais/LeisMunicipais |
| ⬜️ | Planos diretores | 0 | 5.570 | `municipais/*/*/plano-diretor` | portais municipais |
| ⬜️ | Códigos tributários municipais | 0 | 5.570 | `municipais/*/*/codigo-tributario` | portais municipais |
| ⬜️ | Códigos de obras, posturas e zoneamento | 0 | 16.000 | `municipais/*/*/codigos` | portais municipais |
| ⬜️ | Leis ordinárias e complementares municipais (27 capitais primeiro) | 0 | 8.300.000 | `municipais/*/*/leis-ordinarias`, `municipais/*/*/leis-complementares` | Câmaras municipais |
| ⬜️ | Decretos municipais | 0 | 2.000.000 | `municipais/*/*/decretos` | prefeituras e diários oficiais |

---

## Pastas fora do plano

Pastas com `.md` que nenhum item de `scripts/plano.py` cobre. Cada uma é nome fora do
padrão ou tipo de norma não planejado — as duas coisas pedem correção.

| Pasta | Arquivos |
| --- | ---: |
| `reguladores/anvisa/resolucoes` | 371 |
| `reguladores/integracao/portarias` | 149 |
| `reguladores/comunicacoes/portarias` | 104 |
| `reguladores/cultura/portarias` | 81 |
| `reguladores/mj/portarias` | 71 |
| `reguladores/mda/portarias` | 63 |
| `reguladores/mdh/portarias` | 57 |
| `reguladores/poder-judiciario/portarias` | 50 |
| `reguladores/entidades-de-fiscalizacao-do-exercicio-d/resolucoes` | 48 |
| `reguladores/defesa/portarias` | 47 |
| `reguladores/gestao/portarias` | 40 |
| `reguladores/mdic/portarias` | 34 |
| `reguladores/mcti/portarias` | 24 |
| `reguladores/pesca/portarias` | 23 |
| `reguladores/iphan/portarias` | 18 |
| `reguladores/integracao/resolucoes` | 15 |
| `reguladores/planejamento/portarias` | 14 |
| `reguladores/presidencia/portarias` | 13 |
| `reguladores/entidades-de-fiscalizacao-do-exercicio-d/portarias` | 12 |
| `reguladores/presidencia/resolucoes` | 11 |
| `reguladores/inep/portarias` | 11 |
| `reguladores/mpu/portarias` | 11 |
| `reguladores/transportes/portarias` | 10 |
| `reguladores/mcti/resolucoes` | 10 |
| `reguladores/mme/portarias` | 9 |
| `reguladores/mj/deliberacoes` | 9 |
| `reguladores/esporte/deliberacoes` | 8 |
| `reguladores/controladoria-geral-da-uniao/portarias` | 6 |
| `reguladores/cidades/portarias` | 6 |
| `reguladores/mma/portarias` | 6 |
| `reguladores/mds/portarias` | 6 |
| `reguladores/fazenda/portarias` | 6 |
| `reguladores/tribunal-de-contas-da-uniao/portarias` | 5 |
| `reguladores/mre/portarias` | 5 |
| `reguladores/igualdade-racial/portarias` | 5 |
| `reguladores/mda/resolucoes` | 5 |
| `reguladores/planejamento/resolucoes` | 4 |
| `reguladores/mpi/portarias` | 4 |
| `reguladores/mdic/circulares` | 4 |
| `reguladores/bcb/instrucoes-normativas` | 4 |
| `reguladores/portos-aeroportos/resolucoes` | 4 |
| `reguladores/portos-aeroportos/portarias` | 4 |
| `reguladores/mte/resolucoes` | 4 |
| `reguladores/defensoria-publica-da-uniao/portarias` | 3 |
| `reguladores/entidades-de-fiscalizacao-do-exercicio-d/deliberacoes` | 3 |
| `reguladores/mds/instrucoes-normativas` | 3 |
| `reguladores/conselho-nacional-do-ministerio-publico/portarias` | 3 |
| `reguladores/entidades-de-fiscalizacao-do-exercicio-d/instrucoes-normativas` | 2 |
| `reguladores/transportes/instrucoes-normativas` | 2 |
| `reguladores/cultura/instrucoes-normativas` | 2 |
| `reguladores/esporte/portarias` | 2 |
| `reguladores/poder-judiciario/resolucoes` | 2 |
| `reguladores/mdic/resolucoes` | 2 |
| `reguladores/mds/resolucoes` | 2 |
| `reguladores/bcb/resolucoes` | 2 |
| `reguladores/conselho-nacional-do-ministerio-publico/provimentos` | 2 |
| `reguladores/presidencia/instrucoes-normativas` | 1 |
| `reguladores/ms/resolucoes` | 1 |
| `reguladores/empreendedorismo/resolucoes` | 1 |
| `reguladores/empreendedorismo/portarias` | 1 |
| `reguladores/cade/portarias` | 1 |
| `reguladores/mulheres/portarias` | 1 |
| `reguladores/rfb/resolucoes` | 1 |
| `reguladores/gestao/instrucoes-normativas` | 1 |
| `reguladores/gestao/resolucoes` | 1 |
| `reguladores/mma/resolucoes` | 1 |
| `reguladores/turismo/portarias` | 1 |
| `reguladores/mj/instrucoes-normativas` | 1 |
| `reguladores/mj/resolucoes` | 1 |
