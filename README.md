# Legislação brasileira em Markdown

Constituição Federal, legislação federal e legislação estadual/distrital convertidas para Markdown, a partir das fontes oficiais.

> **Aviso:** os textos têm caráter informativo e **não substituem a publicação no Diário Oficial**. Conversões
> automáticas (e, em alguns casos, OCR de PDFs escaneados) podem conter erros. Confira sempre a fonte indicada em
> cada arquivo.

## Estrutura

```
constituicao.md                      Constituição Federal de 1988 (texto vigente, Planalto)
federal/
  leis-ordinarias/AAAA/*.md          Leis federais (1821–hoje)
  leis-complementares/AAAA/*.md
  leis-delegadas/ leis-constitucionais/ decretos-lei/
  _indice/  _fonte/  _falhas.jsonl   índices, HTML bruto (gzip) e registro do que não foi baixado
estaduais/UF/
  constituicao/  emendas-constitucionais/  leis-ordinarias/  leis-complementares/
  leis-delegadas/  decretos-lei/                             (quando a UF os tem)
  _indice/  _fonte/  _falhas.jsonl
scripts/                             código que baixa e converte tudo
COBERTURA.md                         quantas normas há por esfera/tipo e o que ficou faltando
```

Os nomes de pasta são sempre os mesmos em todas as esferas. Algumas UFs têm pastas a mais, porque a
fonte distingue instrumentos que as outras não têm: `leis-promulgadas` (AM, PB),
`decretos-lei-complementares` (SP), `leis-constitucionais` (MG), `constituicoes-historicas` (BA),
`lei-organica` e `emendas-lei-organica` (DF).

Cada arquivo começa com um cabeçalho YAML, com os campos nesta ordem:

```yaml
---
titulo: "Lei nº 10.406 de 10/01/2002"
uf: "SP"                 # ausente nas normas federais
tipo: "Lei Ordinária"
numero: "10406"
data: 2002-01-10         # sempre presente; vazia quando a fonte não informa
ano: "2002"              # só quando a fonte dá apenas o ano (PA, PE)
ementa: "Institui o Código Civil."
situacao: "Em vigor"
revogada: false          # federal: só marca true quando o portal registra a revogação
versao_texto: "compilada (texto vigente)"
publicacao: "DOU de 11/01/2002"
data_publicacao: 2002-01-11
urn: "urn:lex:br:federal:lei:2002-01-10;10406"
fonte: "https://normas.leg.br/?urn=urn:lex:br:federal:lei:2002-01-10;10406"
arquivo: "https://…/lei10406.pdf"   # quando o texto veio de um PDF
baixado_em: 2026-10-13
---
```

Depois do cabeçalho, o corpo sempre abre com o título em `#` e então o texto da norma:

```markdown
---
… cabeçalho …
---
# Lei nº 10.406 de 10/01/2002

LEI Nº 10.406, DE 10 DE JANEIRO DE 2002

Institui o Código Civil.
```

Cinco arquivos trazem, no lugar do texto, um aviso em citação: a fonte oficial serve um documento
vazio para eles e só os metadados foram preservados (também registrados nos `_falhas.jsonl`). A
`constituicao.md` na raiz é o único arquivo sem cabeçalho, por ser o documento único de topo.

`titulo`, `tipo`, `numero`, `data`, `versao_texto`, `fonte` e `baixado_em` existem em todos os
arquivos; os demais aparecem quando a fonte os fornece. O campo `tipo` usa um vocabulário fechado de
onze valores: `Constituição Estadual`, `Emenda Constitucional`, `Lei Ordinária`, `Lei Complementar`,
`Lei Delegada`, `Lei Constitucional`, `Lei Promulgada`, `Decreto-Lei`, `Decreto-Lei Complementar`,
`Lei Orgânica` e `Emenda à Lei Orgânica`.

O vocabulário vive em `CANONICO`, em `scripts/comum.py`, e vale tanto para quem baixa quanto para
`scripts/normalizar.py`, que reaplica o mapa ao acervo já gravado.

## Fontes

| Esfera | Fonte | Texto |
| --- | --- | --- |
| Constituição Federal | Planalto | vigente, sem trechos revogados |
| Federal | API de dados abertos do Senado (índice) + normas.leg.br (texto) | compilado vigente quando existe; senão a publicação original |
| AC, AL, AM, PB, PI, RO, RR, TO | SAPL das Assembleias (API REST) | PDF anexado (OCR quando escaneado) |
| AP | e-Legis da Assembleia | texto integral (PDF) + Constituição consolidada |
| BA | Portal de Legislação (Casa Civil) | HTML |
| CE | BELT – Banco Eletrônico de Leis Temáticas (Assembleia) | HTML |
| DF | SINJ-DF | texto compilado |
| ES, SE | sistema de legislação das Assembleias | HTML (compilado quando disponível) |
| GO | Legisla Goiás (Casa Civil) | HTML |
| MA | GED da Assembleia | PDF |
| MG | Dados abertos da ALMG | texto atualizado quando existe |
| MS | Legislação da Governadoria (Lotus Notes) | HTML |
| MT | Assembleia Legislativa | redação atual (PDF gerado pelo site) |
| PA | Banco de Leis da ALEPA | PDF (OCR quando escaneado) |
| PE | Alepe Legis | texto atualizado quando existe |
| PR | Sistema Estadual de Legislação (Casa Civil) | compilado — ver pendências |
| RJ | Legislação Estadual da ALERJ (Lotus Notes) | HTML — ver pendências |
| RN | Assembleia Legislativa | PDF (acervo a partir de 1994) |
| RS | Sistema LEGIS da Assembleia; Constituição no portal do DAL | PDF (recentes) ou HTML (antigas) |
| SC | Legislação SC (ALESC) | texto anotado |
| SP | ALESP (dados abertos + API) | texto atualizado quando existe |

Os detalhes de cada fonte estão no cabeçalho de cada script em `scripts/estados/`.

## O que não está aqui

- **Legislação municipal** (mais de 5.500 municípios, sem fonte centralizada).
- Decretos, resoluções, portarias e atos infralegais — o foco são constituições, emendas e leis (ordinárias,
  complementares, delegadas) e decretos-leis.
- Normas cujo texto não existe na fonte oficial ou não pôde ser obtido: veja `COBERTURA.md` e os arquivos
  `_falhas.jsonl` (cada linha explica o motivo).

## Pendências

- **PR** — o WAF do `legislacao.pr.gov.br` responde 403 ao acesso automatizado: a primeira requisição passa e as
  seguintes são bloqueadas. Não há tentativa de contornar o bloqueio. Pendente de outra fonte (p.ex. a Assembleia)
  ou de autorização da Casa Civil.
- **RJ** — o Lotus Notes da ALERJ (`alerjln1.alerj.rj.gov.br`) fecha a conexão ou leva mais de 60 s por página. O
  script existe (`scripts/estados/rj.py`) e já tem retentativas longas; basta rodá-lo quando o servidor voltar.
- **RS** — 5.569 leis antigas estão no índice do LEGIS, mas a página de texto responde "NORMA SEM TEXTO": a
  Assembleia nunca as digitalizou.
- **ES e SE** — 311 e 411 normas em que o servidor da Assembleia derruba a conexão de forma consistente, mesmo
  após repescagem. Rodar o script de novo mais tarde tende a recuperar parte delas.
- **RN** — o acervo da Assembleia só tem PDF a partir de 1994 (1.241 respostas 404 para normas anteriores).
- **AC** (a partir de 2009) e **TO** (antes de 2020) — limites do próprio SAPL dessas Assembleias.
- **OCR** — 13.520 arquivos vêm de PDF escaneado, via framework Vision do macOS. O texto é legível, mas erra a
  ordem de leitura em digitalizações de duas colunas e confunde ordinais (`Art. 19` por `Art. 1º`).

  O erro de ordinal foi corrigido em 1.393 arquivos por `scripts/corrigir_ocr.py`, que só reescreve a corrida
  `19, 29, 39…` quando ela começa em 19, tem ao menos dois termos e a numeração resultante fica coerente —
  assim um `Art. 19` legítimo, ou um `Art. 99` que cita outra lei, não é tocado. O erro de ordem de leitura
  não tem correção automática: precisaria de um modelo com noção de layout.

  `baidu/Unlimited-OCR` foi testado em Apple Silicon (M4, 16 GB) e **não serve localmente**. O código fixa
  `.cuda()` e `autocast("cuda")`, mas isso se contorna redirecionando para MPS, e `use_flash_attn` já é `False`
  por padrão. Os impedimentos reais são dois, ambos medidos:

  - na resolução de treino (1024), o encoder de visão SAM precisa de ~21 GB porque, sem flash-attn, a atenção é
    materializada densa — estoura os 16 GB;
  - numa resolução que caiba (640), o caminho de visão roda, mas só o prefill de uma página leva 221 s (≈830 h
    para o lote) e a saída vem vazia, porque a resolução está fora da especificação do modelo.

  Não é instabilidade numérica: os logits são sãos (sem NaN/Inf). Reprocessar esse lote exige GPU NVIDIA, pelo
  caminho oficial (vLLM ou SGLang).

## Como atualizar

Requisitos: macOS com Python 3 e `pdftotext` (poppler). O OCR usa o framework Vision do macOS
(`swiftc -O scripts/ocr.swift -o scripts/bin/ocr`).

```sh
python3 -I scripts/baixar_federal.py            # federal (retomável: pula o que já existe)
python3 -I scripts/estados/sp.py                # um estado (cada um tem seu script)
python3 -I scripts/estados/sapl.py baixar PB    # estados com SAPL
python3 -I scripts/estados/spl_agape.py ES      # ES e SE
python3 -I scripts/reconverter.py [UF ...]      # regenera os .md a partir de _fonte após mudar o conversor
python3 -I scripts/normalizar.py                # confere pastas/cabeçalhos canônicos (--aplicar grava)
python3 -I scripts/corrigir_ocr.py              # simula a correção de ordinais do OCR (--aplicar grava;
                                                #   repita até relatar 0: um arquivo pode ter várias corridas)
python3 -I scripts/relatorio.py                 # atualiza COBERTURA.md
```

Todos os scripts limitam a taxa de requisições (1–4 por segundo) para não sobrecarregar os servidores públicos.
