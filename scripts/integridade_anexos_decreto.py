"""Retenção conservadora de objeto/suplemento próprio ausente da transcrição.

Rótulos, links e pontilhado não são conteúdo. A aprovação de um documento pode
exigir revisão mesmo sem a palavra ANEXO; referências a outro ato, alterações
atomizadas e objeto efetivamente reproduzido não bastam para reter.
"""
import html
import re
import unicodedata


def normal(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text.lower())
                   if not unicodedata.combining(c))


def _limpar(corpo):
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', corpo)
    text = re.sub(r'<a\b[^>]*>(.*?)</a>', r'\1', text, flags=re.I | re.S)
    # Double escaping occurs in official Word exports and in the transcription.
    for _ in range(3):
        decoded = html.unescape(text)
        if decoded == text:
            break
        text = decoded
    return normal(re.sub(r'[*_`#]', '', text))


def _rotulo_vazio(text):
    text = text.strip(' <>&«»\\[]()-')
    return bool(re.fullmatch(r'(?:anex[oa]s?|tabelas?|quadros?)(?:\s+[ivxlcdm\d .,–-]+)?\.?', text)) or bool(re.fullmatch(r'\\*final do documento\.?|\d+\s*/\s*\d+', text))


def anexo_proprio_ausente(corpo, parsed):
    if parsed.visual:
        return None  # Separate visual gate retains these; this helper proves no absence.
    clean = _limpar(corpo)
    blocks = [re.sub(r'\s+', ' ', b).strip() for b in clean.split('\n\n') if b.strip()]
    # A regulation can precede its own final signature when the first presidential
    # date has an unusual layout. A second own Art.1 is actual content, not a label.
    if len(re.findall(r'^\s*art(?:igo)?\.?\s*(?:1[º°o.]?(?!\d)|unico\b)', clean, re.M)) > 1:
        return None
    fechamento = next((i for i, b in enumerate(blocks)
                        if re.match(r'^(?:brasilia|rio de janeiro|capital federal)(?:[-,\s]+d\.?f\.?)?[,.;\s]+(?:em\s*)?\d', b)), None)
    if fechamento is None:
        return None
    principal = '\n'.join(blocks[:fechamento])
    explicit = re.search(r'que com est[ea] baixa[m]?|que a est[ea] acompanha|acompanha (?:este|o presente) decreto|anex[oa]s? a este decreto|anex[oa]s? ao presente decreto', principal)
    artigos = [(i, b) for i, b in enumerate(blocks[:fechamento])
               if re.match(r'^art(?:igo)?\.?\s*(?:\d|unico)', b)]
    approvals = [(i, b, m) for i, b in artigos
                     for m in [re.search(r'\b(?:fica[m]?|sao|e)\s+aprovad[oa]s?\b', b)]
                     if m and not re.search(r'\b(?:sera|serao|devera|deverao|ate que|depois|apos|uma vez|quando|elaborado e aprovado|posteriormente)\b', b[:m.end()])]
    approval = next((a for a in approvals if re.search(r'\banex[oa]s?\b|acompanha|com est[ea] baixa', a[1])), approvals[0] if approvals else None)
    remissao = explicit
    document_only = False
    if approval:
        bi, artigo, match = approval
        own_annex = re.search(r'\banex[oa]s?\b|que com est[ea] baixa[m]?|acompanha', artigo)
        # Approval in the own article establishes the referent of 'na forma dos
        # anexos'. An annex explicitly belonging to another numbered act does not.
        if own_annex and not re.search(r'anex[oa]s? ao decreto\s+n', artigo):
            remissao = own_annex
        promised = re.search(r'a seguir mencionad[oa]s?|a saber', artigo)
        if promised:
            following = '\n'.join(blocks[bi + 1:fechamento])
            gap = re.match(r'^\.{15,}(?:\s|$)', following)
            if gap:
                return {'motivo': 'Relação prometida pelo comando próprio substituída por pontilhado, sem os nomes/dados na transcrição.',
                        'remissao': artigo, 'lacuna': gap[0].strip(), 'fecho': blocks[fechamento], 'estado': 'ausencia_na_transcricao'}
        after = artigo[match.end():]
        object_match = re.match(r'\s*(?:[,].{0,100}?[,])?\s*(?:(?:o|a|os|as)\s+)?(?:(?:novo|nova|novos|novas)\s+)?(regulamento|regimento|manual|estatuto|programas?|plano|criterios|quadro|tabela|relacao)\b', after)
        inline = re.search(r'seguinte[s]?\b|nos termos deste decreto|consoante o estabelecido no presente decreto|abaixo|constituido d[oa]s?|compreendendo|constituindo programa', artigo)
        # For short approvals without deixis, hold as a documented question rather
        # than claiming an omitted annex: the object may be defined by the own act.
        if not remissao and object_match and len(artigos) <= 5 and not inline and not re.search(r'anex[oa]s? ao decreto\s+n', artigo):
            document_only = True
            remissao = match
    # A substituted model can be an own annex without an approval formula.
    # A literal placeholder is evidence of a label, never of the promised model.
    if not remissao and any(_rotulo_vazio(b) for b in blocks[fechamento + 1:]):
        for _, artigo in artigos:
            model = re.search(r'\bmodelos?\s+anex[oa]s?\b', artigo)
            external = re.search(r'\bmodelos?\s+anex[oa]s?\s+(?:ao|aos|do|dos)\s+decretos?\s+n', artigo)
            if model and not external:
                remissao = re.search(re.escape(artigo), principal)
                break
    if not remissao:
        return None
    # A table after the approval may be the object itself, including a table placed
    # before the presidential date. A table before the approval proves nothing.
    if parsed.structure:
        table = clean.find('<table')
        command = clean.find(approval[1]) if approval else -1
        if table < 0 or command < 0 or table > command:
            return None
    apos = blocks[fechamento + 1:]
    heading = re.compile(r'^(?:anexo|regulamento|regimento|manual|estatuto|tabela|quadro|relacao|convencao|acordo)\b')
    if any(re.match(r'^art(?:igo)?\.?\s*\d', b) for b in apos):
        return None
    tail = [b for b in apos if not _rotulo_vazio(b) and not heading.match(b)
            and not re.search(r'publicad[oa]|diario oficial|\bdou\b|nao substitui', b)]
    if any(len(b) > 130 or re.search(r'\d|[:;!?=]', b) or len(b.split()) > 16 or re.match(r'^(?:o|a|os|as|cada|este|esta|para|compete|cabe)\s', b) for b in tail) or len(' '.join(tail)) > 650:
        return None
    if document_only:
        # Lists or operative details between the approval and the date may be the
        # complete object; neither a separate annex nor a title is then required.
        bi, artigo, match = approval
        material = '\n'.join(blocks[bi + 1:fechamento])
        if re.search(r'(?m)^(?:\d+[).\\]|[ivx]+\s*[-–]|[a-z]\))', material) or '<table' in material:
            return None
        return {'motivo': 'Aprovação própria de documento sem remissão explícita: fonte só traz aprovação/regras administrativas e fecho; exige revisão do objeto, sem afirmar lacuna comprovada.',
                'remissao': artigo, 'fecho': blocks[fechamento], 'apos_fecho': apos,
                'estado': 'revisao_documental_necessaria'}
    return {'motivo': 'Suplemento próprio referido pelo decreto ausente da transcrição: somente fecho, assinaturas, nota ou rótulo/link vazio, sem corpo do objeto.',
            'remissao': approval[1] if approval else principal[max(0, remissao.start() - 120):remissao.end() + 120],
            'fecho': blocks[fechamento], 'apos_fecho': apos, 'estado': 'ausencia_na_transcricao'}
