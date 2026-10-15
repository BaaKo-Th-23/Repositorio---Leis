"""O plano do acervo: todo tipo de norma brasileira que deve estar aqui, onde fica e de onde vem.

Este arquivo é a única fonte de verdade sobre o escopo. `scripts/progresso.py` o lê, conta o que
já existe em disco e gera `progresso.svg` e `PROGRESSO.md`. Um tipo de norma que não está nesta
lista não é medido; um que está e tem zero arquivos aparece como lacuna aberta.

O campo `meta` passa por três estados, nesta ordem. Começa como **estimativa** do tamanho do
universo de cada tipo, montada a partir da numeração mais recente da série e da ordem de grandeza
que a fonte declara — serve para dimensionar a barra, não para afirmar um número oficial. Quando o
índice da fonte é baixado, vira o **tamanho real do índice**: é o caso das séries federais, todas
contadas em `federal/_indice/`. Quando a coleta termina, vira a **contagem do acervo** — por isso
as séries encerradas (decretos-leis, leis delegadas) marcam 100%.

`caminho` é relativo à raiz do repositório, aceita `*` (um nível) para varrer as 27 unidades
federativas ou os municípios, e aceita vários caminhos separados por vírgula quando um mesmo item
reúne pastas que as fontes distinguem (lei promulgada e lei constitucional, por exemplo).
"""
import collections

Item = collections.namedtuple("Item", "setor nome caminho meta fase fonte")

# As fases são a ordem de ataque, não uma hierarquia jurídica: 1 fecha a esfera federal, que tem
# fonte única e boa; 2 ataca o infralegal e a jurisprudência, onde mora a norma que de fato se
# aplica; 3 é o direito municipal, maior que todo o resto somado e sem fonte centralizada.
FASES = {
    1: ("Fase 1 — esfera federal completa", "fonte única (normas.leg.br, Planalto, Senado)"),
    2: ("Fase 2 — infralegal e jurisprudência", "uma fonte por órgão, agência ou tribunal"),
    3: ("Fase 3 — direito municipal", "5.570 fontes, sem índice central"),
}

PLANO = [
    # ----------------------------------------------------------------- Constituição e leis federais
    Item("Constituição Federal", "Constituição de 1988 (texto vigente)", "constituicao.md", 1, 1,
         "https://www.planalto.gov.br"),
    Item("Constituição Federal", "Constituições históricas (1824, 1891, 1934, 1937, 1946, 1967, 1969)",
         "federal/constituicoes-historicas", 7, 1, "https://www.planalto.gov.br"),
    Item("Constituição Federal", "Emendas constitucionais e de revisão", "federal/emendas-constitucionais", 172, 1,
         "https://normas.leg.br"),

    Item("Leis federais", "Leis ordinárias (1822–hoje)", "federal/leis-ordinarias", 16700, 1,
         "Senado (índice) + normas.leg.br (texto)"),
    Item("Leis federais", "Leis complementares", "federal/leis-complementares", 237, 1, "normas.leg.br"),
    Item("Leis federais", "Leis delegadas (série encerrada)", "federal/leis-delegadas", 13, 1, "normas.leg.br"),
    Item("Leis federais", "Decretos-leis (série encerrada em 1988)", "federal/decretos-lei", 12250, 1,
         "normas.leg.br"),

    # ------------------------------------------------------------------------- Atos do Congresso
    Item("Atos do Congresso", "Decretos legislativos", "federal/decretos-legislativos", 21775, 1,
         "normas.leg.br"),
    Item("Atos do Congresso", "Medidas provisórias (originais e reedições)", "federal/medidas-provisorias", 7497, 1,
         "Planalto + normas.leg.br"),
    Item("Atos do Congresso", "Resoluções do Senado Federal", "federal/resolucoes-senado", 6578, 1,
         "normas.leg.br"),
    Item("Atos do Congresso", "Resoluções da Câmara dos Deputados", "federal/resolucoes-camara", 1500, 1,
         "camara.leg.br"),
    Item("Atos do Congresso", "Resoluções do Congresso Nacional e da Revisão Constitucional",
         "federal/resolucoes-congresso", 95, 1,
         "normas.leg.br"),
    Item("Atos do Congresso", "Regimentos internos (Senado, Câmara, Congresso)", "federal/regimentos", 3, 1,
         "senado.leg.br, camara.leg.br"),

    # ---------------------------------------------------------- Decretos do Executivo federal
    Item("Decretos do Executivo federal", "Decretos numerados (1889–hoje, as duas séries)",
         "federal/decretos", 139127, 1, "normas.leg.br + Planalto"),
    Item("Decretos do Executivo federal", "Decretos não numerados", "federal/decretos-nao-numerados", 14510, 1,
         "Planalto"),
    Item("Decretos do Executivo federal", "Regulamentos consolidados (RIR, RIPI, Aduaneiro, RPS, PAF)",
         "federal/regulamentos", 20, 1, "Planalto"),

    # ------------------------------------------------------------------ Tratados internacionais
    Item("Tratados internacionais", "Decretos de promulgação de tratados", "tratados/decretos", 4000, 1,
         "Concórdia/MRE + Planalto"),
    Item("Tratados internacionais", "Tratados de direitos humanos (status constitucional/supralegal)",
         "tratados/direitos-humanos", 40, 1, "MRE + Planalto"),
    Item("Tratados internacionais", "Convenções da OIT ratificadas", "tratados/oit", 100, 1, "ilo.org + MTE"),
    Item("Tratados internacionais", "Acordos de bitributação", "tratados/bitributacao", 40, 1, "RFB"),
    Item("Tratados internacionais", "Normas do Mercosul internalizadas", "tratados/mercosul", 1500, 1,
         "mercosur.int"),

    # ------------------------------------------------------------------------------- Tributário
    Item("Infralegal — tributário", "Instruções normativas da Receita Federal", "reguladores/rfb/instrucoes-normativas",
         2600, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — tributário", "Portarias e atos declaratórios da RFB", "reguladores/rfb/portarias", 9000, 2,
         "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — tributário", "Soluções de consulta e divergência (COSIT)", "reguladores/rfb/solucoes-cosit",
         8000, 2, "normas.receita.fazenda.gov.br"),
    Item("Infralegal — tributário", "Pareceres normativos", "reguladores/rfb/pareceres-normativos", 200, 2,
         "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — tributário", "Súmulas e resoluções do CARF", "reguladores/carf", 300, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — tributário", "Convênios, protocolos e ajustes SINIEF (CONFAZ)", "reguladores/confaz", 12000, 2,
         "confaz.fazenda.gov.br"),
    Item("Infralegal — tributário", "Portarias e instruções da STN", "reguladores/stn", 2000, 2,
         "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — tributário", "Normas da PGFN", "reguladores/pgfn", 1500, 2, "Diário Oficial da União (in.gov.br)"),

    # ----------------------------------------------------------------- Trânsito e transportes
    Item("Infralegal — trânsito e transportes", "Resoluções do CONTRAN", "reguladores/contran/resolucoes", 1050, 2,
         "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — trânsito e transportes", "Deliberações do CONTRAN", "reguladores/contran/deliberacoes", 300, 2,
         "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — trânsito e transportes", "Portarias do DENATRAN/SENATRAN", "reguladores/senatran", 1500, 2,
         "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — trânsito e transportes", "Manual Brasileiro de Sinalização de Trânsito (volumes I–VII)",
         "reguladores/contran/sinalizacao", 7, 2, "CONTRAN — MBST"),
    Item("Infralegal — trânsito e transportes", "Resoluções da ANTT", "reguladores/antt", 6000, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — trânsito e transportes", "Resoluções da ANTAQ", "reguladores/antaq", 500, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — trânsito e transportes", "Resoluções e RBAC da ANAC", "reguladores/anac", 700, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — trânsito e transportes", "Normas da Autoridade Marítima (NORMAM)", "reguladores/normam", 40, 2,
         "marinha.mil.br/dpc"),

    # ----------------------------------------------------------------- Saúde e vigilância
    Item("Infralegal — saúde", "Resoluções da diretoria colegiada (RDC) da ANVISA", "reguladores/anvisa/rdc", 1100, 2,
         "anvisa.gov.br"),
    Item("Infralegal — saúde", "Instruções normativas e portarias da ANVISA", "reguladores/anvisa/outros", 2000, 2,
         "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — saúde", "Portarias do Ministério da Saúde (GM/MS e consolidadas)", "reguladores/ms/portarias",
         30000, 2, "saude.gov.br — SAGE/Saúde Legis"),
    Item("Infralegal — saúde", "Resoluções do Conselho Nacional de Saúde", "reguladores/cns", 700, 2,
         "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — saúde", "Resoluções normativas da ANS", "reguladores/ans", 600, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — saúde", "Resoluções do CFM e pareceres", "reguladores/cfm", 2500, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — saúde", "Resoluções do COFEN", "reguladores/cofen", 800, 2, "Diário Oficial da União (in.gov.br)"),

    # ----------------------------------------------------------- Trabalho e previdência
    Item("Infralegal — trabalho e previdência", "Normas regulamentadoras (NR-1 a NR-38)", "reguladores/mte/nr", 38, 2,
         "gov.br/trabalho"),
    Item("Infralegal — trabalho e previdência", "Portarias do Ministério do Trabalho", "reguladores/mte/portarias",
         3000, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — trabalho e previdência", "Instruções normativas do INSS", "reguladores/inss", 160, 2,
         "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — trabalho e previdência", "Instruções normativas e portarias da SPREV", "reguladores/sprev",
         900, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — trabalho e previdência", "Resoluções e instruções da PREVIC", "reguladores/previc", 400, 2,
         "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — trabalho e previdência", "Enunciados e súmulas do CRPS", "reguladores/crps", 100, 2,
         "Diário Oficial da União (in.gov.br)"),

    # ------------------------------------------------------------------- Meio ambiente
    Item("Infralegal — meio ambiente", "Resoluções do CONAMA", "reguladores/conama", 520, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — meio ambiente", "Instruções normativas e portarias do IBAMA", "reguladores/ibama", 1500, 2,
         "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — meio ambiente", "Instruções normativas do ICMBio", "reguladores/icmbio", 400, 2,
         "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — meio ambiente", "Resoluções da ANA e do CNRH", "reguladores/ana", 3000, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — meio ambiente", "Instruções normativas do SFB e do Serviço Florestal", "reguladores/sfb", 200, 2,
         "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — meio ambiente", "Instruções normativas do MAPA (agropecuária)", "reguladores/mapa", 3000, 2,
         "gov.br/agricultura — SISLEGIS"),

    # --------------------------------------------------------- Econômico-financeiro
    Item("Infralegal — financeiro", "Resoluções do CMN", "reguladores/bcb/resolucoes-cmn", 5200, 2,
         "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — financeiro", "Resoluções e circulares do Banco Central", "reguladores/bcb/resolucoes-bcb",
         5000, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — financeiro", "Instruções e resoluções da CVM", "reguladores/cvm", 500, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — financeiro", "Circulares e resoluções da SUSEP e do CNSP", "reguladores/susep", 1200, 2,
         "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — financeiro", "Resoluções do CADE e do COAF", "reguladores/cade-coaf", 400, 2,
         "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — financeiro", "Resoluções e pronunciamentos do CFC e do CPC", "reguladores/cfc-cpc", 3000, 2,
         "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — financeiro", "Resoluções e instruções do INMETRO", "reguladores/inmetro", 2000, 2,
         "Diário Oficial da União (in.gov.br)"),

    # ------------------------------------------------------ Infraestrutura, energia e comunicações
    Item("Infralegal — infraestrutura e energia", "Resoluções normativas e homologatórias da ANEEL",
         "reguladores/aneel", 2000, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — infraestrutura e energia", "Resoluções da ANP", "reguladores/anp", 1000, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — infraestrutura e energia", "Resoluções e atos da ANATEL", "reguladores/anatel", 800, 2,
         "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — infraestrutura e energia", "Resoluções da ANM (mineração)", "reguladores/anm", 300, 2,
         "gov.br/anm"),
    Item("Infralegal — infraestrutura e energia", "Resoluções do CNPE e do CMSE", "reguladores/cnpe", 300, 2,
         "Diário Oficial da União (in.gov.br)"),

    # --------------------------------------------------------------- Educação e cultura
    Item("Infralegal — educação e cultura", "Resoluções e pareceres do CNE", "reguladores/cne", 1500, 2,
         "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — educação e cultura", "Portarias do MEC e do INEP", "reguladores/mec", 4000, 2,
         "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — educação e cultura", "Instruções normativas e portarias da CAPES", "reguladores/capes", 1000, 2,
         "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — educação e cultura", "Instruções normativas da ANCINE e do IPHAN", "reguladores/ancine-iphan",
         900, 2, "Diário Oficial da União (in.gov.br)"),

    # ------------------------------------------------------------- Justiça, eleições e conselhos
    Item("Infralegal — justiça e eleições", "Resoluções e instruções do TSE", "reguladores/tse", 5000, 2,
         "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — justiça e eleições", "Resoluções, provimentos e recomendações do CNJ", "reguladores/cnj", 1200,
         2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — justiça e eleições", "Resoluções e recomendações do CNMP", "reguladores/cnmp", 400, 2,
         "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — justiça e eleições", "Provimentos e resoluções do Conselho Federal da OAB",
         "reguladores/oab", 800, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — justiça e eleições", "Resoluções do CONFEA/CREA e demais conselhos profissionais",
         "reguladores/conselhos-profissionais", 3000, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — justiça e eleições", "Instruções normativas e portarias da CGU", "reguladores/cgu", 1200, 2,
         "Diário Oficial da União (in.gov.br)"),

    # ----------------------------------------------------------------- Jurisprudência vinculante
    Item("Jurisprudência vinculante", "Súmulas vinculantes do STF", "jurisprudencia/stf/sumulas-vinculantes", 59, 2,
         "stf.jus.br — caderno ainda não localizado"),
    Item("Jurisprudência vinculante", "Súmulas do STF", "jurisprudencia/stf/sumulas", 736, 2, "stf.jus.br"),
    Item("Jurisprudência vinculante", "Temas de repercussão geral", "jurisprudencia/stf/repercussao-geral", 1400, 2,
         "stf.jus.br"),
    Item("Jurisprudência vinculante", "Controle concentrado com eficácia erga omnes (ADI, ADC, ADPF, ADO)",
         "jurisprudencia/stf/controle-concentrado", 8000, 2, "stf.jus.br"),
    Item("Jurisprudência vinculante", "Súmulas do STJ", "jurisprudencia/stj/sumulas", 649, 2, "stj.jus.br"),
    Item("Jurisprudência vinculante", "Temas de recursos repetitivos (STJ)", "jurisprudencia/stj/repetitivos", 1300, 2,
         "stj.jus.br"),
    Item("Jurisprudência vinculante", "Súmulas e orientações jurisprudenciais do TST", "jurisprudencia/tst", 1157, 2,
         "tst.jus.br"),
    Item("Jurisprudência vinculante", "Súmulas do TCU, TNU, STM e TSE", "jurisprudencia/outros-tribunais", 700, 2,
         "tcu.gov.br, cjf.jus.br, stm.jus.br, tse.jus.br"),
    Item("Jurisprudência vinculante", "Regimentos internos dos tribunais superiores",
         "jurisprudencia/regimentos", 6, 2, "portais dos tribunais"),

    # ----------------------------------------------------------- Estadual: leis (já coletado)
    Item("Leis estaduais e distritais", "Constituições estaduais e Lei Orgânica do DF", "estaduais/*/constituicao, estaduais/*/lei-organica", 27,
         1, "Assembleias e Casas Civis"),
    Item("Leis estaduais e distritais", "Constituições estaduais históricas", "estaduais/*/constituicoes-historicas",
         40, 1, "Assembleias"),
    Item("Leis estaduais e distritais", "Emendas constitucionais estaduais", "estaduais/*/emendas-constitucionais",
         2200, 1, "Assembleias"),
    Item("Leis estaduais e distritais", "Leis ordinárias estaduais", "estaduais/*/leis-ordinarias", 330000, 1,
         "19 scripts, uma fonte por UF"),
    Item("Leis estaduais e distritais", "Leis complementares estaduais", "estaduais/*/leis-complementares", 14000, 1,
         "19 scripts, uma fonte por UF"),
    Item("Leis estaduais e distritais", "Decretos-leis e leis delegadas estaduais",
         "estaduais/*/decretos-lei, estaduais/*/leis-delegadas, estaduais/*/decretos-lei-complementares", 600, 1,
         "Assembleias"),
    Item("Leis estaduais e distritais", "Leis promulgadas, constitucionais e emendas à Lei Orgânica",
         "estaduais/*/leis-promulgadas, estaduais/*/leis-constitucionais, estaduais/*/emendas-lei-organica",
         600, 1, "Assembleias"),

    # ----------------------------------------------------------- Estadual: infralegal (lacuna)
    Item("Infralegal estadual", "Decretos dos governadores (27 UF)", "estaduais/*/decretos", 400000, 2,
         "Casas Civis e diários oficiais estaduais"),
    Item("Infralegal estadual", "Regulamentos do ICMS (RICMS das 27 UF)", "estaduais/*/regulamentos", 27, 2,
         "Secretarias de Fazenda"),
    Item("Infralegal estadual", "Instruções normativas e portarias das SEFAZ", "estaduais/*/instrucoes-normativas",
         50000, 2, "Secretarias de Fazenda"),
    Item("Infralegal estadual", "Resoluções e decisões normativas dos TCE", "estaduais/*/resolucoes-tce", 10000, 2,
         "Tribunais de Contas estaduais"),
    Item("Infralegal estadual", "Resoluções e provimentos dos TJ e das Corregedorias",
         "estaduais/*/resolucoes-tj", 8000, 2, "Tribunais de Justiça"),
    Item("Infralegal estadual", "Regimentos internos das Assembleias", "estaduais/*/regimentos", 27, 2, "Assembleias"),

    # --------------------------------------------------------------------------- Municipal
    Item("Legislação municipal", "Leis orgânicas municipais", "municipais/*/*/lei-organica", 5570, 3,
         "portais municipais e Leis Municipais/LeisMunicipais"),
    Item("Legislação municipal", "Planos diretores", "municipais/*/*/plano-diretor", 5570, 3, "portais municipais"),
    Item("Legislação municipal", "Códigos tributários municipais", "municipais/*/*/codigo-tributario", 5570, 3,
         "portais municipais"),
    Item("Legislação municipal", "Códigos de obras, posturas e zoneamento", "municipais/*/*/codigos", 16000, 3,
         "portais municipais"),
    Item("Legislação municipal", "Leis ordinárias e complementares municipais (27 capitais primeiro)",
         "municipais/*/*/leis-ordinarias, municipais/*/*/leis-complementares", 8300000, 3,
         "Câmaras municipais"),
    Item("Legislação municipal", "Decretos municipais", "municipais/*/*/decretos", 2000000, 3,
         "prefeituras e diários oficiais"),
]


def por_setor():
    """Agrupa o plano por setor, preservando a ordem em que os setores aparecem."""
    setores = collections.OrderedDict()
    for item in PLANO:
        setores.setdefault(item.setor, []).append(item)
    return setores
