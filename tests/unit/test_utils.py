import unittest

from base64 import b64encode, b64decode

from fast_s3_rest import utils


class TestUtils(unittest.TestCase):

    _massa_de_teste = bytearray(32)

    _ground_truth_b64str = b64encode(_massa_de_teste).decode('utf-8')
    _ground_truth_bytes = b64decode(_ground_truth_b64str.encode('utf-8'))

    dados_em_b64str = utils.bytes_para_base64str(_massa_de_teste)
    dados_em_bytes = utils.base64str_para_bytes(dados_em_b64str)

    def test_consistencia(self):
        self.assertIsNotNone(self.dados_em_bytes)
        self.assertIsNotNone(self.dados_em_b64str)

    def test_conteudo(self):
        self.assertIsInstance(self.dados_em_bytes, bytes)
        self.assertIsInstance(self.dados_em_b64str, str)

    def test_congruencia(self):
        self.assertEqual(self.dados_em_bytes, self._ground_truth_bytes)
        self.assertEqual(self.dados_em_b64str, self._ground_truth_b64str)

    def test_validacao(self):
        self.assertEqual(self.dados_em_bytes, utils.base64str_para_bytes(self.dados_em_b64str))
        self.assertEqual(self.dados_em_b64str, utils.bytes_para_base64str(self.dados_em_bytes))

    def test_igualdade(self):
        self.assertEqual(utils.base64str_para_bytes(self.dados_em_b64str), self._massa_de_teste)
