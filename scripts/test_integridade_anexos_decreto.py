from pathlib import Path
import sys, unittest
from types import SimpleNamespace
sys.path.insert(0,str(Path(__file__).resolve().parent))
from integridade_anexos_decreto import anexo_proprio_ausente as gate

P=SimpleNamespace(visual=[],structure=[])
MAIN='DECRETO Nº 52.677\n\nArtigo único. Fica aprovado o Regimento que com êste baixa.\n\nBrasília, 14 de outubro de 1963; 142º da Independência.\n\nJOÃO GOULART\n\nPaulo de Tarso'
class Anexos(unittest.TestCase):
 def test_somente_assinaturas_ou_nota_retem(self):
  self.assertIsNotNone(gate(MAIN,P))
  self.assertIsNotNone(gate(MAIN+'\n\nO Regimento foi publicado no Diário Oficial de 17 de outubro.',P))
 def test_regimento_presente_nao_retem(self):
  self.assertIsNone(gate(MAIN+'\n\nREGIMENTO DA FACULDADE\n\nArt. 1º A Faculdade...',P))
 def test_citacao_de_outro_decreto_nao_retem(self):
  self.assertIsNone(gate(MAIN.replace('que com êste baixa','anexo ao Decreto nº 1.234 de 1960'),P))
 def test_link_tabela_ou_visual_exige_outra_analise(self):
  self.assertIsNotNone(gate(MAIN+'\n\n[Regimento](https://official/anexo)',P))
  self.assertIsNotNone(gate(MAIN+'\n\n<a href="anexo.pdf">ANEXO</a>',P))
  self.assertIsNotNone(gate(MAIN+'\n\nANEXO',P))
  self.assertIsNone(gate(MAIN+'\n\n[ANEXO](#anexo)\n\nANEXO\n\nArt. 1º Ficam fixados os valores.',P))
  self.assertIsNone(gate(MAIN,SimpleNamespace(visual=[],structure=[('table',())])))
  self.assertIsNone(gate(MAIN,SimpleNamespace(visual=['img'],structure=[])))
 def test_placeholder_escapado_nao_e_conteudo(self):
  for label in ['&lt;&lt;ANEXO&gt;&gt;', '&amp;lt;&amp;lt;ANEXO&amp;gt;&amp;gt;', '«ANEXO»', 'TABELAS.', 'ANEXO I', r'\\\Final do documento.']:
   self.assertIsNotNone(gate(MAIN+'\n\n'+label,P),label)
 def test_aprovacao_na_forma_dos_anexos_retem(self):
  self.assertIsNotNone(gate(MAIN.replace('o Regimento que com êste baixa','o Quadro de Pessoal, na forma dos anexos'),P))
 def test_documento_aprovado_sem_palavra_anexo_exige_revisao(self):
  text=MAIN.replace('o Regimento que com êste baixa','o Manual de Procedimentos do Órgão')
  self.assertEqual(gate(text,P)['estado'],'revisao_documental_necessaria')
 def test_objeto_inline_sem_suplemento_nao_retem(self):
  text=MAIN.replace('o Regimento que com êste baixa','a lotação numérica na forma seguinte:\n\n1 - Oficial de Administração\n\n2 - Escriturários')
  self.assertIsNone(gate(text,P))
 def test_alteracao_atomizada_nao_exige_estatuto_inteiro(self):
  text=MAIN.replace('o Regimento que com êste baixa','a alteração do art. 8º do Estatuto, que passa a ter a seguinte redação:\n\nArt. 8º O capital social é de cem unidades')
  self.assertIsNone(gate(text,P))
 def test_regulamento_antes_do_ultimo_fecho_nao_e_rotulo(self):
  text=MAIN.replace('Brasília, 14','Brasília (DF), 14')+'\n\nREGIMENTO\n\nArt. 1º A Faculdade terá cursos.\n\nArt. 2º Os cursos são gratuitos.\n\nBrasília, 14 de outubro de 1963.\n\nMinistro da Educação'
  self.assertIsNone(gate(text,P))
 def test_aprovacao_futura_nao_e_documento_aprovado_agora(self):
  text=MAIN.replace('Fica aprovado o Regimento que com êste baixa','O Diretor exercerá a competência até que seja instalado o Conselho e aprovado o respectivo Regimento')
  self.assertIsNone(gate(text,P))
 def test_relacao_prometida_substituida_por_pontilhado(self):
  text=MAIN.replace('o Regimento que com êste baixa','o enquadramento dos professores, abrangendo os ocupantes a seguir mencionados, a saber:\n\n..........................................\n\nParágrafo único. Permanecem nas cadeiras')
  self.assertIn('pontilhado',gate(text,P)['motivo'])
 def test_relacao_nominal_reproduzida_nao_retem(self):
  text=MAIN.replace('o Regimento que com êste baixa','o enquadramento dos professores, abrangendo os ocupantes a seguir mencionados, a saber:\n\n1. José da Silva - Química\n\n2. Maria dos Santos - Física')
  self.assertIsNone(gate(text,P))
 def test_tabela_depois_da_aprovacao_pode_ser_objeto(self):
  text=MAIN.replace('o Regimento que com êste baixa','a tabela na forma do anexo\n\n<table><tr><td>Valor</td><td>10</td></tr></table>')
  self.assertIsNone(gate(text,SimpleNamespace(visual=[],structure=[('table',())])))
 def test_tabela_anterior_nao_prova_suplemento_posterior(self):
  text='<table><tr><td>Dado anterior</td></tr></table>\n\n'+MAIN
  self.assertIsNotNone(gate(text,SimpleNamespace(visual=[],structure=[('table',())])))
 def test_rotulos_sem_dados_e_nota_de_publicacao_nao_sao_objeto(self):
  text=MAIN+'\n\nQUADRO DE PESSOAL - PARTE PERMANENTE\n\nCONSELHO NACIONAL DE SERVIÇO SOCIAL\n\nSECRETARIA EXECUTIVA\n\n&lt;&lt;TABELA&gt;&gt;\n\nO anexo foi publicado no D.O. de 4-8-72.'
  self.assertIsNotNone(gate(text,P))
 def test_aprovacao_posterior_e_formas_de_anexo(self):
  for obj in ['o anexo Estatuto da Companhia', 'a tabela em anexo', 'as relações nominais anexas', 'o Regimento, de acordo com o texto anexo']:
   text=MAIN.replace('Artigo único. Fica aprovado o Regimento que com êste baixa','Art. 1º Fica aprovado o valor de dez unidades.\n\nArt. 2º Fica aprovado '+obj)
   self.assertIsNotNone(gate(text,P),obj)
 def test_corpo_curto_de_regimento_sem_artigos_e_conteudo(self):
  self.assertIsNone(gate(MAIN+'\n\nREGIMENTO\n\nA Faculdade terá cursos gratuitos.',P))
 def test_inicial_de_assinatura_nao_e_artigo_gramatical(self):
  self.assertIsNotNone(gate(MAIN.replace('JOÃO GOULART','A. COSTA E SILVA'),P))
 def test_eleicao_depois_de_aprovacao_futura_nao_retem(self):
  text=MAIN.replace('Artigo único. Fica aprovado o Regimento que com êste baixa','Art. 2º A eleição se realizará quinze dias depois e aprovado o novo Regimento do HSE')
  self.assertIsNone(gate(text,P))
if __name__=='__main__':unittest.main()
