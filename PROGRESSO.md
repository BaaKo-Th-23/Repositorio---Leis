# Progresso

Gerado por `scripts/progresso.py` em 15/10/2026 22:30:44 (America/Recife). O escopo está em
`scripts/plano.py`; os números de **meta** são estimativas do tamanho de cada série, não
contagens oficiais. O percentual mede volume diante das metas; não comprova integralidade
das fontes nem qualidade de cada conversão. Lacunas continuam abertas até verificação.

**547.986 de ~11.768.329 normas — 4.7%**

![progresso](progresso.svg)

## Fase 1 — esfera federal completa

Fonte única (normas.leg.br, Planalto, Senado). **351.905 de ~574.432 — 61.3%**

### Constituição Federal — 180 / ~180 (100.0%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| ✅ | Constituição de 1988 (texto vigente) | 1 | 1 | `constituicao.md` | https://www.planalto.gov.br |
| ✅ | Constituições históricas (1824, 1891, 1934, 1937, 1946, 1967, 1969) | 7 | 7 | `federal/constituicoes-historicas` | https://www.planalto.gov.br |
| ✅ | Emendas constitucionais e de revisão | 172 | 172 | `federal/emendas-constitucionais` | https://normas.leg.br |

### Leis federais — 29.184 / ~29.200 (99.9%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| 🟦 | Leis ordinárias (1822–hoje) | 16.684 | 16.700 | `federal/leis-ordinarias` | Senado (índice) + normas.leg.br (texto) |
| ✅ | Leis complementares | 237 | 237 | `federal/leis-complementares` | normas.leg.br |
| ✅ | Leis delegadas (série encerrada) | 13 | 13 | `federal/leis-delegadas` | normas.leg.br |
| ✅ | Decretos-leis (série encerrada em 1988) | 12.250 | 12.250 | `federal/decretos-lei` | normas.leg.br |

### Atos do Congresso — 20.862 / ~38.248 (54.5%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| 🟦 | Decretos legislativos | 15.928 | 21.775 | `federal/decretos-legislativos` | normas.leg.br |
| 🟦 | Medidas provisórias (originais e reedições) | 3.141 | 7.497 | `federal/medidas-provisorias` | Planalto + normas.leg.br |
| 🟦 | Resoluções do Senado Federal | 698 | 6.578 | `federal/resolucoes-senado` | normas.leg.br |
| 🟦 | Resoluções da Câmara dos Deputados | 1.004 | 2.300 | `federal/resolucoes-camara` | camara.leg.br |
| 🟦 | Resoluções do Congresso Nacional e da Revisão Constitucional | 88 | 95 | `federal/resolucoes-congresso` | normas.leg.br |
| ✅ | Regimentos internos (Senado, Câmara, Congresso) | 3 | 3 | `federal/regimentos` | senado.leg.br, camara.leg.br |

### Decretos do Executivo federal — 5.628 / ~153.657 (3.7%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| ⬜️ | Decretos numerados (1889–hoje, as duas séries) | 0 | 139.127 | `federal/decretos` | normas.leg.br + Planalto |
| 🟦 | Decretos não numerados | 5.619 | 14.510 | `federal/decretos-nao-numerados` | Planalto |
| 🟦 | Regulamentos consolidados (RIR, RIPI, Aduaneiro, RPS, PAF) | 9 | 20 | `federal/regulamentos` | Planalto |

### Tratados internacionais — 133 / ~5.680 (2.3%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| ⬜️ | Decretos de promulgação de tratados | 0 | 4.000 | `tratados/decretos` | Concórdia/MRE + Planalto |
| 🟦 | Tratados de direitos humanos (status constitucional/supralegal) | 12 | 40 | `tratados/direitos-humanos` | MRE + Planalto |
| 🟦 | Convenções da OIT ratificadas | 98 | 100 | `tratados/oit` | ilo.org + MTE |
| 🟦 | Acordos de bitributação | 23 | 40 | `tratados/bitributacao` | RFB |
| ⬜️ | Normas do Mercosul internalizadas | 0 | 1.500 | `tratados/mercosul` | mercosur.int |

### Leis estaduais e distritais — 295.918 / ~347.467 (85.2%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| 🟦 | Constituições estaduais e Lei Orgânica do DF | 25 | 27 | `estaduais/*/constituicao`, `estaduais/*/lei-organica` | Assembleias e Casas Civis |
| 🟦 | Constituições estaduais históricas | 10 | 40 | `estaduais/*/constituicoes-historicas` | Assembleias |
| 🟦 | Emendas constitucionais estaduais | 2.095 | 2.200 | `estaduais/*/emendas-constitucionais` | Assembleias |
| 🟦 | Leis ordinárias estaduais | 274.138 | 330.000 | `estaduais/*/leis-ordinarias` | 19 scripts, uma fonte por UF |
| 🟦 | Leis complementares estaduais | 12.386 | 14.000 | `estaduais/*/leis-complementares` | 19 scripts, uma fonte por UF |
| ✅ | Decretos-leis e leis delegadas estaduais | 6.676 | 600 | `estaduais/*/decretos-lei`, `estaduais/*/leis-delegadas`, `estaduais/*/decretos-lei-complementares` | Assembleias |
| 🟦 | Leis promulgadas, constitucionais e emendas à Lei Orgânica | 588 | 600 | `estaduais/*/leis-promulgadas`, `estaduais/*/leis-constitucionais`, `estaduais/*/emendas-lei-organica` | Assembleias |

## Fase 2 — infralegal e jurisprudência

Uma fonte por órgão, agência ou tribunal. **195.521 de ~861.184 — 22.7%**

### Infralegal — tributário — 1.114 / ~134.038 (0.8%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| 🟦 | Receita Federal: instruções normativas, portarias, atos declaratórios, soluções de consulta e pareceres normativos | 600 | 115.238 | `reguladores/rfb` | RFB — Sijut (23 espécies normativas) e Diário Oficial da União |
| 🟦 | CONFAZ: convênios, protocolos e ajustes SINIEF | 224 | 12.000 | `reguladores/confaz` | Diário Oficial da União (in.gov.br) |
| 🟦 | Tesouro Nacional: portarias e instruções | 56 | 2.000 | `reguladores/stn` | Diário Oficial da União (in.gov.br) |
| 🟦 | Procuradoria-Geral da Fazenda Nacional | 24 | 1.500 | `reguladores/pgfn` | Diário Oficial da União (in.gov.br) |
| 🟦 | CARF: súmulas e resoluções | 9 | 300 | `reguladores/carf` | Diário Oficial da União (in.gov.br) |
| 🟦 | Ministério da Fazenda: demais atos normativos | 201 | 3.000 | `reguladores/fazenda` | Diário Oficial da União (in.gov.br) |

### Infralegal — trânsito e transportes — 2.747 / ~12.857 (21.4%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| 🟦 | CONTRAN: resoluções, deliberações e o Manual Brasileiro de Sinalização | 7 | 1.357 | `reguladores/contran` | Diário Oficial da União (in.gov.br) |
| 🟦 | SENATRAN/DENATRAN: portarias | 355 | 1.500 | `reguladores/senatran` | Diário Oficial da União (in.gov.br) |
| 🟦 | ANTT: resoluções | 375 | 6.000 | `reguladores/antt` | Diário Oficial da União (in.gov.br) |
| ✅ | ANTAQ: resoluções | 501 | 500 | `reguladores/antaq` | Diário Oficial da União (in.gov.br) |
| ✅ | ANAC: resoluções e RBAC | 1.160 | 700 | `reguladores/anac` | Diário Oficial da União (in.gov.br) |
| 🟦 | Ministério dos Transportes: demais atos normativos | 231 | 2.000 | `reguladores/transportes` | Diário Oficial da União (in.gov.br) |
| 🟦 | Ministério de Portos e Aeroportos | 118 | 800 | `reguladores/portos-aeroportos` | Diário Oficial da União (in.gov.br) |

### Infralegal — saúde — 8.868 / ~34.400 (25.8%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| ✅ | ANVISA: RDC, instruções normativas e portarias | 4.763 | 3.100 | `reguladores/anvisa` | Diário Oficial da União (in.gov.br) |
| 🟦 | Ministério da Saúde: portarias GM/MS e consolidadas | 3.947 | 30.000 | `reguladores/ms` | Diário Oficial da União (in.gov.br) |
| 🟦 | Conselho Nacional de Saúde: resoluções | 13 | 700 | `reguladores/cns` | Diário Oficial da União (in.gov.br) |
| 🟦 | ANS: resoluções normativas | 145 | 600 | `reguladores/ans` | Diário Oficial da União (in.gov.br) |

### Infralegal — trabalho e previdência — 676 / ~4.498 (15.0%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| 🟦 | Ministério do Trabalho: normas regulamentadoras (NR-1 a NR-38) e portarias | 134 | 3.038 | `reguladores/mte` | Diário Oficial da União (in.gov.br) |
| 🟦 | INSS: instruções normativas | 88 | 160 | `reguladores/inss` | Diário Oficial da União (in.gov.br) |
| 🟦 | Secretaria de Previdência: instruções normativas e portarias | 79 | 900 | `reguladores/sprev` | Diário Oficial da União (in.gov.br) |
| 🟦 | PREVIC: resoluções e instruções | 375 | 400 | `reguladores/previc` | Diário Oficial da União (in.gov.br) |

### Infralegal — meio ambiente — 3.468 / ~10.720 (32.4%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| 🟦 | CONAMA: resoluções | 2 | 520 | `reguladores/conama` | Diário Oficial da União (in.gov.br) |
| 🟦 | IBAMA: instruções normativas e portarias | 47 | 1.500 | `reguladores/ibama` | Diário Oficial da União (in.gov.br) |
| 🟦 | ICMBio: instruções normativas | 139 | 400 | `reguladores/icmbio` | Diário Oficial da União (in.gov.br) |
| 🟦 | ANA e CNRH: resoluções | 30 | 3.000 | `reguladores/ana` | Diário Oficial da União (in.gov.br) |
| 🟦 | Serviço Florestal Brasileiro: instruções normativas | 7 | 200 | `reguladores/sfb` | Diário Oficial da União (in.gov.br) |
| 🟦 | Ministério da Agricultura: instruções normativas | 2.597 | 3.000 | `reguladores/mapa` | Diário Oficial da União (in.gov.br) |
| 🟦 | Ministério do Meio Ambiente: demais atos normativos | 114 | 1.500 | `reguladores/mma` | Diário Oficial da União (in.gov.br) |
| 🟦 | Ministério da Pesca e Aquicultura | 532 | 600 | `reguladores/pesca` | Diário Oficial da União (in.gov.br) |

### Infralegal — financeiro — 1.721 / ~19.550 (8.8%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| 🟦 | Banco Central e CMN: resoluções e circulares | 207 | 10.200 | `reguladores/bcb` | Diário Oficial da União (in.gov.br) |
| 🟦 | CVM: instruções e resoluções | 43 | 500 | `reguladores/cvm` | Diário Oficial da União (in.gov.br) |
| 🟦 | SUSEP e CNSP: circulares e resoluções | 507 | 1.200 | `reguladores/susep` | Diário Oficial da União (in.gov.br) |
| 🟦 | CADE: resoluções | 15 | 300 | `reguladores/cade` | Diário Oficial da União (in.gov.br) |
| 🟦 | COAF: resoluções | 10 | 150 | `reguladores/coaf` | Diário Oficial da União (in.gov.br) |
| 🟦 | Conselho Federal de Contabilidade: resoluções | 37 | 1.800 | `reguladores/cfc` | Diário Oficial da União (in.gov.br) |
| 🟦 | INMETRO: resoluções e instruções | 364 | 2.000 | `reguladores/inmetro` | Diário Oficial da União (in.gov.br) |
| 🟦 | Ministério do Desenvolvimento, Indústria, Comércio e Serviços | 500 | 3.000 | `reguladores/mdic` | Diário Oficial da União (in.gov.br) |
| 🟦 | Ministério do Empreendedorismo e da Microempresa | 38 | 400 | `reguladores/empreendedorismo` | Diário Oficial da União (in.gov.br) |

### Infralegal — infraestrutura e energia — 5.335 / ~8.000 (66.7%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| 🟦 | ANEEL: resoluções normativas e homologatórias | 367 | 2.000 | `reguladores/aneel` | Diário Oficial da União (in.gov.br) |
| 🟦 | ANP: resoluções | 51 | 1.000 | `reguladores/anp` | Diário Oficial da União (in.gov.br) |
| 🟦 | ANATEL: resoluções e atos | 20 | 800 | `reguladores/anatel` | Diário Oficial da União (in.gov.br) |
| 🟦 | ANM: resoluções (mineração) | 39 | 300 | `reguladores/anm` | Diário Oficial da União (in.gov.br) |
| 🟦 | Ministério de Minas e Energia, CNPE e CMSE | 310 | 1.500 | `reguladores/mme` | Diário Oficial da União (in.gov.br) |
| ✅ | Ministério das Comunicações | 1.636 | 800 | `reguladores/comunicacoes` | Diário Oficial da União (in.gov.br) |
| 🟦 | Ministério das Cidades | 296 | 800 | `reguladores/cidades` | Diário Oficial da União (in.gov.br) |
| ✅ | Ministério da Integração e do Desenvolvimento Regional | 2.616 | 800 | `reguladores/integracao` | Diário Oficial da União (in.gov.br) |

### Infralegal — educação e cultura — 4.700 / ~12.300 (38.2%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| 🟦 | Conselho Nacional de Educação: resoluções e pareceres | 153 | 1.500 | `reguladores/cne` | Diário Oficial da União (in.gov.br) |
| 🟦 | Ministério da Educação: portarias | 2.202 | 4.000 | `reguladores/mec` | Diário Oficial da União (in.gov.br) |
| 🟦 | INEP: portarias e instruções normativas | 131 | 1.200 | `reguladores/inep` | Diário Oficial da União (in.gov.br) |
| 🟦 | CAPES: instruções normativas e portarias | 78 | 1.000 | `reguladores/capes` | Diário Oficial da União (in.gov.br) |
| 🟦 | ANCINE: instruções normativas | 18 | 500 | `reguladores/ancine` | Diário Oficial da União (in.gov.br) |
| 🟦 | IPHAN: portarias e instruções normativas | 194 | 400 | `reguladores/iphan` | Diário Oficial da União (in.gov.br) |
| ✅ | Ministério da Cultura | 1.224 | 1.200 | `reguladores/cultura` | Diário Oficial da União (in.gov.br) |
| 🟦 | Ministério do Esporte | 131 | 400 | `reguladores/esporte` | Diário Oficial da União (in.gov.br) |
| 🟦 | Ministério do Turismo | 38 | 600 | `reguladores/turismo` | Diário Oficial da União (in.gov.br) |
| 🟦 | Ministério da Ciência, Tecnologia e Inovação | 531 | 1.500 | `reguladores/mcti` | Diário Oficial da União (in.gov.br) |

### Infralegal — justiça e controle — 5.377 / ~27.700 (19.4%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| 🟦 | Ministério da Justiça e Segurança Pública | 1.048 | 3.000 | `reguladores/mj` | Diário Oficial da União (in.gov.br) |
| 🟦 | Controladoria-Geral da União: instruções normativas e portarias | 53 | 1.200 | `reguladores/cgu` | Diário Oficial da União (in.gov.br) |
| 🟦 | Advocacia-Geral da União: atos normativos | 109 | 1.500 | `reguladores/agu` | Diário Oficial da União (in.gov.br) |
| 🟦 | Ministério Público da União: resoluções e portarias | 253 | 1.200 | `reguladores/mpu` | Diário Oficial da União (in.gov.br) |
| 🟦 | CNMP: resoluções e recomendações | 18 | 400 | `reguladores/cnmp` | Diário Oficial da União (in.gov.br) |
| 🟦 | Defensoria Pública da União | 22 | 400 | `reguladores/dpu` | Diário Oficial da União (in.gov.br) |
| 🟦 | Tribunal de Contas da União: instruções normativas e resoluções | 30 | 1.500 | `reguladores/tcu` | Diário Oficial da União (in.gov.br) |
| 🟦 | Conselhos federais de fiscalização profissional (CFM, COFEN, CONFEA/CREA e demais) | 1.010 | 7.000 | `reguladores/conselhos-profissionais` | Diário Oficial da União (in.gov.br) |
| 🟦 | Presidência da República: atos normativos | 375 | 2.000 | `reguladores/presidencia` | Diário Oficial da União (in.gov.br) |
| 🟦 | Ministério da Gestão e da Inovação em Serviços Públicos | 651 | 2.500 | `reguladores/gestao` | Diário Oficial da União (in.gov.br) |
| 🟦 | Ministério do Planejamento e Orçamento | 349 | 1.200 | `reguladores/planejamento` | Diário Oficial da União (in.gov.br) |
| 🟦 | Ministério da Defesa e comandos militares | 837 | 2.500 | `reguladores/defesa` | Diário Oficial da União (in.gov.br) |
| 🟦 | Ministério das Relações Exteriores | 84 | 800 | `reguladores/mre` | Diário Oficial da União (in.gov.br) |
| 🟦 | Atos administrativos normativos do Poder Judiciário publicados no DOU | 468 | 1.500 | `reguladores/poder-judiciario` | Diário Oficial da União (in.gov.br) |
| 🟦 | Atos administrativos normativos do Poder Legislativo publicados no DOU | 70 | 600 | `reguladores/poder-legislativo` | Diário Oficial da União (in.gov.br) |
| ⬜️ | BNDES e demais estatais com poder normativo | 0 | 400 | `reguladores/bndes` | Diário Oficial da União (in.gov.br) |

### Infralegal — direitos e desenvolvimento social — 1.902 / ~5.400 (35.2%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| 🟦 | Ministério do Desenvolvimento e Assistência Social | 216 | 2.500 | `reguladores/mds` | Diário Oficial da União (in.gov.br) |
| 🟦 | Ministério dos Direitos Humanos e da Cidadania | 588 | 800 | `reguladores/mdh` | Diário Oficial da União (in.gov.br) |
| 🟦 | Ministério das Mulheres | 15 | 300 | `reguladores/mulheres` | Diário Oficial da União (in.gov.br) |
| 🟦 | Ministério da Igualdade Racial | 31 | 300 | `reguladores/igualdade-racial` | Diário Oficial da União (in.gov.br) |
| 🟦 | Ministério dos Povos Indígenas | 88 | 300 | `reguladores/mpi` | Diário Oficial da União (in.gov.br) |
| 🟦 | Ministério do Desenvolvimento Agrário e Agricultura Familiar | 964 | 1.200 | `reguladores/mda` | Diário Oficial da União (in.gov.br) |

### Jurisprudência vinculante — 4.924 / ~14.667 (33.6%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| ✅ | Súmulas vinculantes do STF | 62 | 62 | `jurisprudencia/stf/sumulas-vinculantes` | CNJ — Pangea/BNP (precedentes do STF) |
| ✅ | Súmulas do STF | 736 | 736 | `jurisprudencia/stf/sumulas` | stf.jus.br |
| 🟦 | Temas de repercussão geral | 550 | 1.489 | `jurisprudencia/stf/repercussao-geral` | CNJ — Pangea/BNP (precedentes do STF) |
| ⬜️ | Controle concentrado com eficácia erga omnes (ADI, ADC, ADPF, ADO) | 0 | 8.000 | `jurisprudencia/stf/controle-concentrado` | stf.jus.br |
| ✅ | Súmulas do STJ | 649 | 649 | `jurisprudencia/stj/sumulas` | stj.jus.br |
| ✅ | Temas de recursos repetitivos (STJ) | 1.474 | 1.474 | `jurisprudencia/stj/repetitivos` | STJ — dados abertos, Temas.csv (números únicos) |
| ✅ | Súmulas e orientações jurisprudenciais do TST | 1.157 | 1.157 | `jurisprudencia/tst` | tst.jus.br |
| 🟦 | Súmulas do TCU, TNU, STM e TSE | 294 | 700 | `jurisprudencia/outros-tribunais` | tcu.gov.br, cjf.jus.br, stm.jus.br, tse.jus.br |
| 🟦 | Regimentos internos dos tribunais superiores | 2 | 6 | `jurisprudencia/regimentos` | portais dos tribunais |
| ⬜️ | Temas de uniformização da TNU, incluindo cancelados | 0 | 394 | `jurisprudencia/tnu/uniformizacao` | CNJ — Pangea/BNP (precedentes da TNU) |

### Infralegal estadual — 154.689 / ~577.054 (26.8%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| 🟦 | Decretos dos governadores (27 UF) | 93.193 | 400.000 | `estaduais/*/decretos`, `estaduais/*/decretos-nao-numerados` | Casas Civis e diários oficiais estaduais |
| ⬜️ | Regulamentos do ICMS (RICMS das 27 UF) | 0 | 27 | `estaduais/*/regulamentos` | Secretarias de Fazenda |
| 🟦 | Instruções normativas e portarias das SEFAZ | 1.063 | 50.000 | `estaduais/*/instrucoes-normativas` | Secretarias de Fazenda |
| ⬜️ | Resoluções e decisões normativas dos TCE | 0 | 10.000 | `estaduais/*/resolucoes-tce` | Tribunais de Contas estaduais |
| ⬜️ | Resoluções e provimentos dos TJ e das Corregedorias | 0 | 8.000 | `estaduais/*/resolucoes-tj` | Tribunais de Justiça |
| 🟦 | Regimentos internos das Assembleias | 10 | 27 | `estaduais/*/regimentos` | Assembleias |
| 🟦 | Decretos legislativos estaduais | 12.246 | 20.000 | `estaduais/*/decretos-legislativos` | Assembleias (SAPL e sistemas próprios) |
| 🟦 | Resoluções das Assembleias | 24.448 | 25.000 | `estaduais/*/resolucoes` | Assembleias (SAPL e sistemas próprios) |
| 🟦 | Portarias das administrações estaduais e distrital | 23.219 | 60.000 | `estaduais/*/portarias` | SINJ-DF, Legisla Goiás e sistemas equivalentes |
| 🟦 | Deliberações, súmulas administrativas, provimentos e pareceres normativos | 510 | 4.000 | `estaduais/*/deliberacoes`, `estaduais/*/sumulas`, `estaduais/*/provimentos`, `estaduais/*/pareceres-normativos` | SINJ-DF, Legisla Goiás e sistemas equivalentes |

## Fase 3 — direito municipal

5.571 municípios no cadastro do IBGE, sem índice legislativo central. **560 de ~10.332.713 — 0.0%**

### Legislação municipal — 560 / ~10.332.713 (0.0%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| 🟦 | Leis orgânicas municipais e suas emendas | 4 | 5.571 | `municipais/*/*/lei-organica`, `municipais/*/*/emendas-lei-organica` | diários das associações estaduais de municípios |
| ⬜️ | Planos diretores | 0 | 5.571 | `municipais/*/*/plano-diretor` | portais municipais |
| ⬜️ | Códigos tributários municipais | 0 | 5.571 | `municipais/*/*/codigo-tributario` | portais municipais |
| ⬜️ | Códigos de obras, posturas e zoneamento | 0 | 16.000 | `municipais/*/*/codigos` | portais municipais |
| 🟦 | Leis ordinárias e complementares municipais (27 capitais primeiro) | 143 | 8.300.000 | `municipais/*/*/leis-ordinarias`, `municipais/*/*/leis-complementares` | Câmaras municipais |
| 🟦 | Decretos municipais | 413 | 2.000.000 | `municipais/*/*/decretos` | prefeituras e diários oficiais |

---

## Pastas fora do plano

Nenhuma: todo arquivo do repositório está sob um item do plano.
