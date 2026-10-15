# Legislação brasileira em Markdown

**323.849 normas** — a Constituição Federal, a legislação federal e a de 25 estados e do Distrito
Federal — convertidas de fontes oficiais para Markdown, com cabeçalho estruturado e link para a
origem de cada texto.

O histórico do git é a própria linha do tempo: **cada commit é uma norma**, assinada por quem a
promulgou e datada do dia em que foi aprovada.

> [!IMPORTANT]
> Os textos têm caráter informativo e **não substituem a publicação no Diário Oficial**. São
> conversões automáticas e, em 17.016 arquivos, OCR de PDF escaneado. Confira sempre a fonte
> indicada no cabeçalho antes de citar.

---

## O que tem aqui

| Esfera | Normas |
| --- | ---: |
| Constituição Federal | 1 |
| Federal | 29.184 |
| Estadual e distrital | 294.664 |
| **Total** | **323.849** |

Por tipo de instrumento:

| Tipo | Normas | | Tipo | Normas |
| --- | ---: | --- | --- | ---: |
| Lei Ordinária | 289.684 | | Lei Promulgada | 434 |
| Decreto-Lei | 18.366 | | Emenda à Lei Orgânica | 134 |
| Lei Complementar | 12.598 | | Constituição Estadual | 26 |
| Emenda Constitucional | 2.013 | | Decreto-Lei Complementar | 23 |
| Lei Delegada | 550 | | Lei Constitucional | 19 |

As contagens por estado, com o que ficou de fora e por quê, estão em
**[COBERTURA.md](COBERTURA.md)**. Para ver em gráficos — normas por estado, por década, por tema,
as palavras mais frequentes nas ementas e quem mais assinou — abra
**[estatisticas.html](estatisticas.html)** no navegador. É um arquivo único, sem servidor nem
dependência externa, gerado por `scripts/estatisticas.py`.

---

## Estrutura

```
constituicao.md                      Constituição Federal de 1988 (texto vigente, Planalto)
federal/
  leis-ordinarias/AAAA/*.md          Leis federais, de 1822 a hoje
  leis-complementares/AAAA/*.md
  leis-delegadas/  decretos-lei/
estaduais/UF/
  constituicao/                      Constituição estadual
  emendas-constitucionais/
  leis-ordinarias/  leis-complementares/  leis-delegadas/  decretos-lei/
scripts/                             o código que baixa, converte e audita
COBERTURA.md                         números por esfera e tipo, e as lacunas
estatisticas.html                    página com gráficos sobre o acervo
```

Os nomes de pasta são os mesmos em todas as esferas. Algumas unidades têm pastas a mais, porque a
fonte distingue instrumentos que as outras não têm: `leis-promulgadas` (AM, PB),
`decretos-lei-complementares` (SP), `leis-constitucionais` (MG), `constituicoes-historicas` (BA),
`lei-organica` e `emendas-lei-organica` (DF).

Fora do versionamento, porque os scripts os reproduzem: `_fonte/` (27 GB com o HTML e os PDFs
originais, comprimidos), `_indice/` (os índices de cada fonte) e os logs. Os `_falhas.jsonl`, que
registram linha por linha o que não entrou, **estão** versionados.

---

## Formato dos arquivos

Todo arquivo tem cabeçalho YAML e, no corpo, o título em `#` seguido do texto da norma:

```markdown
---
titulo: "Lei nº 10.406 de 10/01/2002"
uf: "SP"                 # ausente nas normas federais
tipo: "Lei Ordinária"
numero: "10406"
data: 2002-01-10         # sempre presente; vazia quando a fonte não informa
ano: "2002"              # só quando a fonte dá apenas o ano (PA, PE)
ementa: "Institui o Código Civil."
situacao: "Em vigor"
revogada: false
versao_texto: "compilada (texto vigente)"
publicacao: "DOU de 11/01/2002"
data_publicacao: 2002-01-11
urn: "urn:lex:br:federal:lei:2002-01-10;10406"
fonte: "https://normas.leg.br/?urn=urn:lex:br:federal:lei:2002-01-10;10406"
arquivo: "https://…/lei10406.pdf"   # quando o texto veio de um PDF
baixado_em: 2026-10-13
---
# Lei nº 10.406 de 10/01/2002

LEI Nº 10.406, DE 10 DE JANEIRO DE 2002

Institui o Código Civil.
```

`titulo`, `tipo`, `numero`, `data`, `versao_texto`, `fonte` e `baixado_em` existem em **todos** os
arquivos; os demais aparecem quando a fonte os fornece. Os campos saem sempre nessa ordem.

O campo `tipo` usa um vocabulário fechado de onze valores, definido em `CANONICO`, em
`scripts/comum.py`. O mesmo mapa vale para quem baixa e para `scripts/normalizar.py`, que o reaplica
ao acervo já gravado — por isso `lei-ordinaria` e `leis-ordinarias`, ou `Lei` e `LEI ORDINARIA`, não
coexistem.

Duas exceções, ambas propositais: a `constituicao.md` na raiz é o único arquivo sem cabeçalho, por
ser o documento único de topo; e cinco arquivos trazem, no lugar do texto, um aviso em citação —
a fonte oficial serve um documento vazio para eles e só os metadados foram preservados.

---

## O histórico do git

Cada commit é uma norma, em ordem cronológica, de 1822 até hoje. São **323.851 commits** e
**5.414 autores**. Os que mais assinaram:

| Normas | Signatário |
| ---: | --- |
| 4.247 | Marconi Ferreira Perillo Júnior |
| 3.795 | Aécio Neves |
| 3.457 | Geraldo Alckmin |
| 3.097 | Ronaldo Caiado |
| 2.654 | Getúlio Vargas |

O autor sai do bloco de assinatura do próprio texto (`scripts/signatarios.py`). Em cerca de 48% dos
casos a assinatura não está na camada de texto do PDF, ou o OCR a perdeu; nesses, o autor é a
instituição — "Estado do Pará", "República Federativa do Brasil". **A mensagem do commit sempre diz
de onde a autoria saiu**, na linha `Autoria:`. Os demais signatários entram como `Co-Authored-By`.

Os e-mails são sintéticos, no formato `nome-sobrenome-NNNNN@exemplo.com`, com os cinco dígitos
derivados do próprio nome — cada pessoa tem uma identidade só no histórico inteiro.

> [!NOTE]
> **Datas anteriores a 1970.** O git conta a data em segundos desde 1970; qualquer data anterior
> vira timestamp negativo, que o `git fsck` reprova como `badDate` e o GitHub rejeita ao receber.
> Como a maior parte do acervo é anterior a 1970, essas normas têm a data do commit fixada em
> 01-01-1970 e a **data real no fim do título, depois de ` | `**, e repetida no corpo. Nos commits
> com data representável o título fica limpo. A ordem cronológica se mantém pela sequência de
> commits, que é linear.

```
Lei nº 86, de 21/04/1880 | 21-04-1880

AUTORIZA O GOVERNO A DISPENSAR DE PROVAS DE CAPACIDADE PARA EXERCER O MAGISTÉRIO…

Data da norma: 1880-04-21
A data do commit está fixada em 01-01-1970: o git não representa data anterior a essa
(vira timestamp negativo, que o GitHub rejeita). A data real da norma é a do título e
a da linha acima.
Autoria: signatário não identificado no texto; autoria institucional.
Fonte: https://www.al.sp.gov.br/norma/139216
```

As 1.595 normas cuja data não existe em nenhuma fonte ficam no fim do histórico, com
`| sem data na fonte` no título.

---

## Fontes

| UF | Fonte | Texto |
| --- | --- | --- |
| — | Planalto | Constituição Federal, texto vigente |
| Federal | Dados abertos do Senado (índice) + normas.leg.br (texto) | compilado vigente quando existe; senão a publicação original |
| AC, AL, AM, PB, PI, RO, RR, TO | SAPL das Assembleias (API REST) | PDF anexado, com OCR quando escaneado |
| AP | e-Legis da Assembleia | texto integral em PDF + Constituição consolidada |
| BA | Portal de Legislação (Casa Civil) | HTML |
| CE | BELT – Banco Eletrônico de Leis Temáticas | HTML |
| DF | SINJ-DF | texto compilado |
| ES, SE | sistema de legislação das Assembleias | HTML, compilado quando disponível |
| GO | Legisla Goiás (Casa Civil) | HTML |
| MA | GED da Assembleia | PDF |
| MG | Dados abertos da ALMG | texto atualizado quando existe |
| MS | Legislação da Governadoria (Lotus Notes) | HTML |
| MT | Assembleia Legislativa | redação atual, PDF gerado pelo site |
| PA | Banco de Leis da ALEPA | PDF, com OCR quando escaneado |
| PE | Alepe Legis | texto atualizado quando existe |
| PR | Sistema Estadual de Legislação | — ver pendências |
| RJ | Legislação Estadual da ALERJ (Lotus Notes) | — ver pendências |
| RN | Assembleia Legislativa | PDF, acervo a partir de 1994 |
| RS | Sistema LEGIS da Assembleia; Constituição no portal do DAL | PDF nas recentes, HTML nas antigas |
| SC | Legislação SC (ALESC) | texto anotado |
| SP | ALESP (dados abertos + API) | texto atualizado quando existe |

Cada script em `scripts/estados/` documenta no cabeçalho a API ou o caminho que usa.

Todos limitam a taxa a 1–4 requisições por segundo, são retomáveis (pulam o que já existe) e
guardam o original em `_fonte/`. **Bloqueios de acesso automatizado não são contornados.**

---

## O que não está aqui

- **Legislação municipal.** Mais de 5.500 municípios, sem fonte centralizada.
- **Decretos, resoluções, portarias e atos infralegais.** O foco são constituições, emendas e leis
  (ordinárias, complementares, delegadas) e decretos-leis.
- Normas cujo texto não existe na fonte ou não pôde ser obtido — cada caso tem uma linha, com o
  motivo, no `_falhas.jsonl` da respectiva pasta.

### Pendências

| O quê | Por quê |
| --- | --- |
| **PR** — nada coletado | o WAF de `legislacao.pr.gov.br` devolve 403 a partir da segunda requisição. Não contornado; precisa de outra fonte ou de autorização da Casa Civil |
| **RJ** — nada coletado | o Lotus Notes da ALERJ fecha a conexão ou leva mais de 60 s por página. `scripts/estados/rj.py` está pronto para quando o servidor voltar |
| **AC** — só até 2009 | limite do SAPL da Assembleia |
| **TO** — a partir de 2020 | limite do SAPL da Assembleia |
| **RN** — a partir de 1994 | o acervo da Assembleia não tem PDF anterior |
| **RS** — 5.569 leis antigas | estão no índice, mas a página de texto responde "NORMA SEM TEXTO": nunca foram digitalizadas |
| **ES e SE** — 311 e 411 normas | o servidor da Assembleia derruba a conexão nessas mesmas normas, de forma consistente |

### Qualidade do OCR

17.016 arquivos vêm de PDF escaneado, com OCR pelo framework Vision do macOS. O texto é legível,
mas tem dois defeitos conhecidos:

- **ordem de leitura trocada** em digitalizações de duas colunas — não tem correção automática;
  precisaria de um modelo com noção de layout;
- **ordinais confundidos** (`Art. 19` por `Art. 1º`) — corrigido em 1.509 arquivos por
  `scripts/corrigir_ocr.py`, que só reescreve a corrida `19, 29, 39…` quando ela começa em 19, tem
  ao menos dois termos e a numeração resultante fica coerente. Assim um `Art. 19` legítimo, ou um
  `Art. 99` que cita outra lei, não é tocado.

`baidu/Unlimited-OCR` foi testado em Apple Silicon e não serve localmente: na resolução de treino o
encoder de visão pede ~21 GB, e numa resolução que caiba o prefill leva 221 s por página com saída
vazia. Reprocessar o lote exige GPU NVIDIA.

---

## Reproduzir e atualizar

**Requisitos:** macOS, Python 3 (só biblioteca padrão), `pdftotext` (poppler) e, para o OCR, o
framework Vision via `swiftc -O scripts/ocr.swift -o scripts/bin/ocr`.

```sh
# baixar — todos os scripts são retomáveis: pulam o que já existe
python3 -I scripts/baixar_federal.py
python3 -I scripts/estados/sp.py                # um estado por script
python3 -I scripts/estados/sapl.py baixar PB    # estados com SAPL
python3 -I scripts/estados/spl_agape.py ES      # ES e SE

# manter em ordem
python3 -I scripts/reconverter.py [UF ...]      # regenera os .md a partir de _fonte
python3 -I scripts/normalizar.py                # pastas, tipos e cabeçalhos canônicos
python3 -I scripts/corrigir_ocr.py              # ordinais do OCR
python3 -I scripts/corrigir_datas_invalidas.py  # datas que não existem no calendário
python3 -I scripts/relatorio.py                 # atualiza COBERTURA.md
python3 -I scripts/estatisticas.py              # atualiza estatisticas.html

# remontar o histórico do git
python3 -I scripts/montar_repositorio.py --saida /caminho/do/repo
```

Os quatro scripts de manutenção são **idempotentes** e rodam em simulação por padrão: só gravam com
`--aplicar`. Rodar de novo, depois de aplicado, relata zero mudanças.

### Auditorias que o acervo passa

| Verificação | Resultado |
| --- | --- |
| `git fsck --strict` | zero erros |
| data em todos os arquivos | 323.848 de 323.848 (a Constituição não tem cabeçalho) |
| data que existe no calendário e não está no futuro | 100% |
| nomes de pasta canônicos | 100% |
| `tipo` no vocabulário fechado | 100% |
| cabeçalho + `# título` + texto | 323.843; 5 com aviso de ausência; 1 por desenho |

---

## Licença

Os textos das normas são **atos oficiais do poder público** e, pelo art. 8º, I, da Lei nº 9.610/98,
não são objeto de proteção autoral. Os scripts deste repositório estão sob a licença MIT — veja
[LICENSE](LICENSE).
