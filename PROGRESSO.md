# Progresso

Gerado por `scripts/progresso.py` em 15/10/2026. O escopo está em
`scripts/plano.py`; os números de **meta** são estimativas do tamanho de cada série, não
contagens oficiais. Séries encerradas (decretos-leis, leis delegadas) marcam 100%.

**323.849 de ~11.491.181 normas — 2.8%**

![progresso](progresso.svg)

## Fase 1 — esfera federal completa

Fonte única (normas.leg.br, Planalto, Senado). **323.849 de ~539.321 — 60.0%**

### Constituição Federal — 1 / ~151 (1%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| ✅ | Constituição de 1988 (texto vigente) | 1 | 1 | `constituicao.md` | https://www.planalto.gov.br |
| ⬜️ | Constituições históricas (1824, 1891, 1934, 1937, 1946, 1967, 1969) | 0 | 7 | `federal/constituicoes-historicas` | https://www.planalto.gov.br |
| ⬜️ | Emendas constitucionais e de revisão | 0 | 143 | `federal/emendas-constitucionais` | https://normas.leg.br |

### Leis federais — 29.184 / ~29.200 (100%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| ✅ | Leis ordinárias (1822–hoje) | 16.684 | 16.700 | `federal/leis-ordinarias` | Senado (índice) + normas.leg.br (texto) |
| ✅ | Leis complementares | 237 | 237 | `federal/leis-complementares` | normas.leg.br |
| ✅ | Leis delegadas (série encerrada) | 13 | 13 | `federal/leis-delegadas` | normas.leg.br |
| ✅ | Decretos-leis (série encerrada em 1988) | 12.250 | 12.250 | `federal/decretos-lei` | normas.leg.br |

### Atos do Congresso — 0 / ~29.303 (0%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| ⬜️ | Decretos legislativos | 0 | 20.000 | `federal/decretos-legislativos` | normas.leg.br |
| ⬜️ | Medidas provisórias (originais e reedições) | 0 | 3.500 | `federal/medidas-provisorias` | Planalto + normas.leg.br |
| ⬜️ | Resoluções do Senado Federal | 0 | 4.000 | `federal/resolucoes-senado` | normas.leg.br |
| ⬜️ | Resoluções da Câmara dos Deputados | 0 | 1.500 | `federal/resolucoes-camara` | camara.leg.br |
| ⬜️ | Resoluções do Congresso Nacional | 0 | 300 | `federal/resolucoes-congresso` | normas.leg.br |
| ⬜️ | Regimentos internos (Senado, Câmara, Congresso) | 0 | 3 | `federal/regimentos` | senado.leg.br, camara.leg.br |

### Decretos do Executivo federal — 0 / ~127.520 (0%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| ⬜️ | Decretos numerados (1889–hoje, as duas séries) | 0 | 112.500 | `federal/decretos` | normas.leg.br + Planalto |
| ⬜️ | Decretos não numerados | 0 | 15.000 | `federal/decretos-nao-numerados` | Planalto |
| ⬜️ | Regulamentos consolidados (RIR, RIPI, Aduaneiro, RPS, RGPS) | 0 | 20 | `federal/regulamentos` | Planalto |

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

Uma fonte por órgão, agência ou tribunal. **0 de ~619.150 — 0.0%**

### Infralegal — tributário — 0 / ~35.600 (0%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| ⬜️ | Instruções normativas da Receita Federal | 0 | 2.600 | `reguladores/rfb/instrucoes-normativas` | normas.receita.fazenda.gov.br |
| ⬜️ | Portarias e atos declaratórios da RFB | 0 | 9.000 | `reguladores/rfb/portarias` | normas.receita.fazenda.gov.br |
| ⬜️ | Soluções de consulta e divergência (COSIT) | 0 | 8.000 | `reguladores/rfb/solucoes-cosit` | normas.receita.fazenda.gov.br |
| ⬜️ | Pareceres normativos | 0 | 200 | `reguladores/rfb/pareceres-normativos` | normas.receita.fazenda.gov.br |
| ⬜️ | Súmulas e resoluções do CARF | 0 | 300 | `reguladores/carf` | carf.fazenda.gov.br |
| ⬜️ | Convênios, protocolos e ajustes SINIEF (CONFAZ) | 0 | 12.000 | `reguladores/confaz` | confaz.fazenda.gov.br |
| ⬜️ | Portarias e instruções da STN | 0 | 2.000 | `reguladores/stn` | tesouro.fazenda.gov.br |
| ⬜️ | Normas da PGFN | 0 | 1.500 | `reguladores/pgfn` | pgfn.fazenda.gov.br |

### Infralegal — trânsito e transportes — 0 / ~10.097 (0%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| ⬜️ | Resoluções do CONTRAN | 0 | 1.050 | `reguladores/contran/resolucoes` | gov.br/transportes — CONTRAN |
| ⬜️ | Deliberações do CONTRAN | 0 | 300 | `reguladores/contran/deliberacoes` | gov.br/transportes — CONTRAN |
| ⬜️ | Portarias do DENATRAN/SENATRAN | 0 | 1.500 | `reguladores/senatran` | gov.br/transportes |
| ⬜️ | Manual Brasileiro de Sinalização de Trânsito (volumes I–VII) | 0 | 7 | `reguladores/contran/sinalizacao` | CONTRAN — MBST |
| ⬜️ | Resoluções da ANTT | 0 | 6.000 | `reguladores/antt` | antt.gov.br |
| ⬜️ | Resoluções da ANTAQ | 0 | 500 | `reguladores/antaq` | antaq.gov.br |
| ⬜️ | Resoluções e RBAC da ANAC | 0 | 700 | `reguladores/anac` | anac.gov.br |
| ⬜️ | Normas da Autoridade Marítima (NORMAM) | 0 | 40 | `reguladores/normam` | marinha.mil.br/dpc |

### Infralegal — saúde — 0 / ~37.700 (0%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| ⬜️ | Resoluções da diretoria colegiada (RDC) da ANVISA | 0 | 1.100 | `reguladores/anvisa/rdc` | anvisa.gov.br |
| ⬜️ | Instruções normativas e portarias da ANVISA | 0 | 2.000 | `reguladores/anvisa/outros` | anvisa.gov.br |
| ⬜️ | Portarias do Ministério da Saúde (GM/MS e consolidadas) | 0 | 30.000 | `reguladores/ms/portarias` | saude.gov.br — SAGE/Saúde Legis |
| ⬜️ | Resoluções do Conselho Nacional de Saúde | 0 | 700 | `reguladores/cns` | conselho.saude.gov.br |
| ⬜️ | Resoluções normativas da ANS | 0 | 600 | `reguladores/ans` | ans.gov.br |
| ⬜️ | Resoluções do CFM e pareceres | 0 | 2.500 | `reguladores/cfm` | portal.cfm.org.br |
| ⬜️ | Resoluções do COFEN | 0 | 800 | `reguladores/cofen` | cofen.gov.br |

### Infralegal — trabalho e previdência — 0 / ~4.598 (0%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| ⬜️ | Normas regulamentadoras (NR-1 a NR-38) | 0 | 38 | `reguladores/mte/nr` | gov.br/trabalho |
| ⬜️ | Portarias do Ministério do Trabalho | 0 | 3.000 | `reguladores/mte/portarias` | gov.br/trabalho |
| ⬜️ | Instruções normativas do INSS | 0 | 160 | `reguladores/inss` | inss.gov.br |
| ⬜️ | Instruções normativas e portarias da SPREV | 0 | 900 | `reguladores/sprev` | gov.br/previdencia |
| ⬜️ | Resoluções e instruções da PREVIC | 0 | 400 | `reguladores/previc` | previc.gov.br |
| ⬜️ | Enunciados e súmulas do CRPS | 0 | 100 | `reguladores/crps` | gov.br/previdencia |

### Infralegal — meio ambiente — 0 / ~8.620 (0%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| ⬜️ | Resoluções do CONAMA | 0 | 520 | `reguladores/conama` | gov.br/mma — CONAMA |
| ⬜️ | Instruções normativas e portarias do IBAMA | 0 | 1.500 | `reguladores/ibama` | ibama.gov.br |
| ⬜️ | Instruções normativas do ICMBio | 0 | 400 | `reguladores/icmbio` | icmbio.gov.br |
| ⬜️ | Resoluções da ANA e do CNRH | 0 | 3.000 | `reguladores/ana` | ana.gov.br |
| ⬜️ | Instruções normativas do SFB e do Serviço Florestal | 0 | 200 | `reguladores/sfb` | gov.br/florestal |
| ⬜️ | Instruções normativas do MAPA (agropecuária) | 0 | 3.000 | `reguladores/mapa` | gov.br/agricultura — SISLEGIS |

### Infralegal — financeiro — 0 / ~17.300 (0%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| ⬜️ | Resoluções do CMN | 0 | 5.200 | `reguladores/bcb/resolucoes-cmn` | bcb.gov.br — Busca de normas |
| ⬜️ | Resoluções e circulares do Banco Central | 0 | 5.000 | `reguladores/bcb/resolucoes-bcb` | bcb.gov.br |
| ⬜️ | Instruções e resoluções da CVM | 0 | 500 | `reguladores/cvm` | cvm.gov.br |
| ⬜️ | Circulares e resoluções da SUSEP e do CNSP | 0 | 1.200 | `reguladores/susep` | susep.gov.br |
| ⬜️ | Resoluções do CADE e do COAF | 0 | 400 | `reguladores/cade-coaf` | cade.gov.br, gov.br/coaf |
| ⬜️ | Resoluções e pronunciamentos do CFC e do CPC | 0 | 3.000 | `reguladores/cfc-cpc` | cfc.org.br, cpc.org.br |
| ⬜️ | Resoluções e instruções do INMETRO | 0 | 2.000 | `reguladores/inmetro` | inmetro.gov.br |

### Infralegal — infraestrutura e energia — 0 / ~4.400 (0%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| ⬜️ | Resoluções normativas e homologatórias da ANEEL | 0 | 2.000 | `reguladores/aneel` | aneel.gov.br |
| ⬜️ | Resoluções da ANP | 0 | 1.000 | `reguladores/anp` | anp.gov.br |
| ⬜️ | Resoluções e atos da ANATEL | 0 | 800 | `reguladores/anatel` | anatel.gov.br |
| ⬜️ | Resoluções da ANM (mineração) | 0 | 300 | `reguladores/anm` | gov.br/anm |
| ⬜️ | Resoluções do CNPE e do CMSE | 0 | 300 | `reguladores/cnpe` | gov.br/mme |

### Infralegal — educação e cultura — 0 / ~7.400 (0%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| ⬜️ | Resoluções e pareceres do CNE | 0 | 1.500 | `reguladores/cne` | mec.gov.br — CNE |
| ⬜️ | Portarias do MEC e do INEP | 0 | 4.000 | `reguladores/mec` | mec.gov.br, inep.gov.br |
| ⬜️ | Instruções normativas e portarias da CAPES | 0 | 1.000 | `reguladores/capes` | capes.gov.br |
| ⬜️ | Instruções normativas da ANCINE e do IPHAN | 0 | 900 | `reguladores/ancine-iphan` | ancine.gov.br, iphan.gov.br |

### Infralegal — justiça e eleições — 0 / ~11.600 (0%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| ⬜️ | Resoluções e instruções do TSE | 0 | 5.000 | `reguladores/tse` | tse.jus.br |
| ⬜️ | Resoluções, provimentos e recomendações do CNJ | 0 | 1.200 | `reguladores/cnj` | atos.cnj.jus.br |
| ⬜️ | Resoluções e recomendações do CNMP | 0 | 400 | `reguladores/cnmp` | cnmp.mp.br |
| ⬜️ | Provimentos e resoluções do Conselho Federal da OAB | 0 | 800 | `reguladores/oab` | oab.org.br |
| ⬜️ | Resoluções do CONFEA/CREA e demais conselhos profissionais | 0 | 3.000 | `reguladores/conselhos-profissionais` | portais dos conselhos federais |
| ⬜️ | Instruções normativas e portarias da CGU | 0 | 1.200 | `reguladores/cgu` | gov.br/cgu |

### Jurisprudência vinculante — 0 / ~13.781 (0%)

| | Tipo de norma | Tem | Meta | Pasta | Fonte |
| :-: | --- | ---: | ---: | --- | --- |
| ⬜️ | Súmulas vinculantes do STF | 0 | 59 | `jurisprudencia/stf/sumulas-vinculantes` | stf.jus.br |
| ⬜️ | Súmulas do STF | 0 | 736 | `jurisprudencia/stf/sumulas` | stf.jus.br |
| ⬜️ | Temas de repercussão geral | 0 | 1.400 | `jurisprudencia/stf/repercussao-geral` | stf.jus.br |
| ⬜️ | Controle concentrado com eficácia erga omnes (ADI, ADC, ADPF, ADO) | 0 | 8.000 | `jurisprudencia/stf/controle-concentrado` | stf.jus.br |
| ⬜️ | Súmulas do STJ | 0 | 680 | `jurisprudencia/stj/sumulas` | stj.jus.br |
| ⬜️ | Temas de recursos repetitivos (STJ) | 0 | 1.300 | `jurisprudencia/stj/repetitivos` | stj.jus.br |
| ⬜️ | Súmulas e orientações jurisprudenciais do TST | 0 | 900 | `jurisprudencia/tst` | tst.jus.br |
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

Nenhuma: todo arquivo do repositório está sob um item do plano.
