"""Evita publicar errata avulsa como se fosse a norma integral."""
from pathlib import Path
import sys
import unittest
from unittest.mock import patch, Mock
from urllib.error import HTTPError
sys.path.insert(0, str(Path(__file__).resolve().parent))
import baixar_federal as f


class TextoIntegral(unittest.TestCase):
    def test_recusa_http_nao_e_retentada(self):
        error = HTTPError('https://normas.leg.br/', 403, 'Forbidden', {}, None)
        with patch.object(f, 'LIMITE', Mock()), patch.object(f.urllib.request, 'urlopen', side_effect=error) as request:
            with self.assertRaisesRegex(RuntimeError, 'fonte recusou HTTP 403'):
                f.http_get('https://normas.leg.br/')
        self.assertEqual(request.call_count, 1)

    def test_original_antes_da_retificacao_mais_recente(self):
        original = {'contentUrl': 'https://normas.leg.br/original', 'version': 'Original', 'datePublished': '2000-01-01'}
        errata = {'contentUrl': 'https://normas.leg.br/errata', 'version': 'Intermediate', 'datePublished': '2000-02-01'}
        self.assertEqual(f.escolher_texto({'encoding': [original, errata]}), original)

    def test_compilada_antes_do_original(self):
        original = {'contentUrl': 'https://normas.leg.br/original', 'version': 'Original'}
        atual = {'contentUrl': 'https://normas.leg.br/atual', 'version': 'Current'}
        self.assertEqual(f.escolher_texto({'encoding': [original, atual]}), atual)

    def test_artigo_citado_em_errata_nao_e_artigo_proprio(self):
        corpo = 'DECRETO Nº 3.435, DE 25 DE ABRIL DE 2000.\n\nNos arts. 3º e 5º do Anexo, onde se lê A, leia-se B.'
        self.assertIsNotNone(f.motivo_texto_parcial_decreto('DEC-n', corpo))

    def test_retificacao_com_artigo_copiado_continua_errata(self):
        self.assertIsNotNone(f.motivo_texto_parcial_decreto('DEC-n', '**RETIFICAÇÃO**\n\nArt. 1º Onde se lê A, leia-se B.'))

    def test_artigo_normativo_proprio(self):
        self.assertIsNone(f.motivo_texto_parcial_decreto('DEC-n', 'DECRETO Nº 1\n\n**Art**. 1º Fica aprovado o regulamento.\n\nArt. 2º Revogam-se as disposições.'))

    def test_comando_sem_artigos_exige_revisao(self):
        self.assertIsNotNone(f.motivo_texto_parcial_decreto('DEC-n', 'O PRESIDENTE faz públicos os depósitos.\n\nRio de Janeiro.'))


if __name__ == '__main__':
    unittest.main()
