import unittest

from fast_s3_rest.modelos import BodyObjetoB64Str
from fast_s3_rest.utils import bytes_para_base64str, base64str_para_bytes


class TestModeloBodyObjetoB64Str(unittest.TestCase):

    arquivo_bytes = open('README.md', 'rb').read()
    arquivo_b64str = bytes_para_base64str(arquivo_bytes)

    def test_modelo_body_objeto_b64str(self):
        body = BodyObjetoB64Str
        body.base64str_objeto = self.arquivo_b64str

        self.assertIsNotNone(body)
        self.assertIsNotNone(body.base64str_objeto)
        self.assertIsInstance(body.base64str_objeto, str)
        self.assertEqual(body.base64str_objeto, self.arquivo_b64str)
        self.assertEqual(base64str_para_bytes(body.base64str_objeto), self.arquivo_bytes)
