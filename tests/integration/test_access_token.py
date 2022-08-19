import unittest

from requests.models import Response

from tests.integration import test_cli

retorno_esperado = {'status': 403, 'mensagem': 'Token de acesso inválido'}
chaves_esperadas = {'status', 'mensagem'}


class TestExcecaoTokenInvalidoListar(unittest.TestCase):

    endpoint = 's3/listar'
    response = test_cli.get(endpoint, headers={'x-access-token': '...'})

    def test_response(self):
        self.assertIsInstance(self.response, Response)
        self.assertIsInstance(self.response.status_code, int)

    def test_conteudo_response(self):
        self.assertEqual(self.response.status_code, 403)
        self.assertIsNotNone(self.response.content)

    def test_consistencia_response(self):
        self.assertIn(self.endpoint, self.response.url)
        self.assertEqual(self.response.ok, False)

    def test_congruencia_response(self):
        self.assertIsInstance(self.response.json(), dict)
        for chave in chaves_esperadas:
            self.assertIn(chave, self.response.json().keys())
            self.assertIsInstance(chave, str)
            self.assertIsNotNone(chave)
            self.assertEqual(self.response.json().get(chave), retorno_esperado.get(chave))
            self.assertEqual(self.response.json().get(chave), retorno_esperado.get(chave))


class TestExcecaoTokenInvalidoPesquisar(unittest.TestCase):

    endpoint = 's3/pesquisar'
    response = test_cli.get(endpoint, headers={'x-access-token': '...'})

    def test_response(self):
        self.assertIsInstance(self.response, Response)
        self.assertIsInstance(self.response.status_code, int)

    def test_conteudo_response(self):
        self.assertEqual(self.response.status_code, 403)
        self.assertIsNotNone(self.response.content)

    def test_consistencia_response(self):
        self.assertIn(self.endpoint, self.response.url)
        self.assertEqual(self.response.ok, False)

    def test_congruencia_response(self):
        self.assertIsInstance(self.response.json(), dict)
        for chave in chaves_esperadas:
            self.assertIn(chave, self.response.json().keys())
            self.assertIsInstance(chave, str)
            self.assertIsNotNone(chave)
            self.assertEqual(self.response.json().get(chave), retorno_esperado.get(chave))
            self.assertEqual(self.response.json().get(chave), retorno_esperado.get(chave))


class TestExcecaoTokenInvalidoDownloadB64Str(unittest.TestCase):

    endpoint = 's3/download/b64str'
    response = test_cli.get(endpoint, headers={'x-access-token': '...'})

    def test_response(self):
        self.assertIsInstance(self.response, Response)
        self.assertIsInstance(self.response.status_code, int)

    def test_conteudo_response(self):
        self.assertEqual(self.response.status_code, 403)
        self.assertIsNotNone(self.response.content)

    def test_consistencia_response(self):
        self.assertIn(self.endpoint, self.response.url)
        self.assertEqual(self.response.ok, False)

    def test_congruencia_response(self):
        self.assertIsInstance(self.response.json(), dict)
        for chave in chaves_esperadas:
            self.assertIn(chave, self.response.json().keys())
            self.assertIsInstance(chave, str)
            self.assertIsNotNone(chave)
            self.assertEqual(self.response.json().get(chave), retorno_esperado.get(chave))
            self.assertEqual(self.response.json().get(chave), retorno_esperado.get(chave))


class TestExcecaoTokenInvalidoDownloadArquivo(unittest.TestCase):

    endpoint = 's3/download/arquivo'
    response = test_cli.get(endpoint, headers={'x-access-token': '...'})

    def test_response(self):
        self.assertIsInstance(self.response, Response)
        self.assertIsInstance(self.response.status_code, int)

    def test_conteudo_response(self):
        self.assertEqual(self.response.status_code, 403)
        self.assertIsNotNone(self.response.content)

    def test_consistencia_response(self):
        self.assertIn(self.endpoint, self.response.url)
        self.assertEqual(self.response.ok, False)

    def test_congruencia_response(self):
        self.assertIsInstance(self.response.json(), dict)
        for chave in chaves_esperadas:
            self.assertIn(chave, self.response.json().keys())
            self.assertIsInstance(chave, str)
            self.assertIsNotNone(chave)
            self.assertEqual(self.response.json().get(chave), retorno_esperado.get(chave))
            self.assertEqual(self.response.json().get(chave), retorno_esperado.get(chave))


class TestExcecaoTokenInvalidoUploadArquivo(unittest.TestCase):

    endpoint = 's3/upload'
    response = test_cli.put(endpoint, headers={'x-access-token': '...'})

    def test_response(self):
        self.assertIsInstance(self.response, Response)
        self.assertIsInstance(self.response.status_code, int)

    def test_conteudo_response(self):
        self.assertEqual(self.response.status_code, 403)
        self.assertIsNotNone(self.response.content)

    def test_consistencia_response(self):
        self.assertIn(self.endpoint, self.response.url)
        self.assertEqual(self.response.ok, False)

    def test_congruencia_response(self):
        self.assertIsInstance(self.response.json(), dict)
        for chave in chaves_esperadas:
            self.assertIn(chave, self.response.json().keys())
            self.assertIsInstance(chave, str)
            self.assertIsNotNone(chave)
            self.assertEqual(self.response.json().get(chave), retorno_esperado.get(chave))
            self.assertEqual(self.response.json().get(chave), retorno_esperado.get(chave))


class TestExcecaoTokenInvalidoApagar(unittest.TestCase):

    endpoint = 's3/apagar'
    response = test_cli.delete(endpoint, headers={'x-access-token': '...'})

    def test_response(self):
        self.assertIsInstance(self.response, Response)
        self.assertIsInstance(self.response.status_code, int)

    def test_conteudo_response(self):
        self.assertEqual(self.response.status_code, 403)
        self.assertIsNotNone(self.response.content)

    def test_consistencia_response(self):
        self.assertIn(self.endpoint, self.response.url)
        self.assertEqual(self.response.ok, False)

    def test_congruencia_response(self):
        self.assertIsInstance(self.response.json(), dict)
        for chave in chaves_esperadas:
            self.assertIn(chave, self.response.json().keys())
            self.assertIsInstance(chave, str)
            self.assertIsNotNone(chave)
            self.assertEqual(self.response.json().get(chave), retorno_esperado.get(chave))
            self.assertEqual(self.response.json().get(chave), retorno_esperado.get(chave))


class TestExcecaoTokenInvalidoStream(unittest.TestCase):

    endpoint = 's3/stream'
    response = test_cli.get(endpoint, headers={'x-access-token': '...'})

    def test_response(self):
        self.assertIsInstance(self.response, Response)
        self.assertIsInstance(self.response.status_code, int)

    def test_conteudo_response(self):
        self.assertEqual(self.response.status_code, 403)
        self.assertIsNotNone(self.response.content)

    def test_consistencia_response(self):
        self.assertIn(self.endpoint, self.response.url)
        self.assertEqual(self.response.ok, False)

    def test_congruencia_response(self):
        self.assertIsInstance(self.response.json(), dict)
        for chave in chaves_esperadas:
            self.assertIn(chave, self.response.json().keys())
            self.assertIsInstance(chave, str)
            self.assertIsNotNone(chave)
            self.assertEqual(self.response.json().get(chave), retorno_esperado.get(chave))
            self.assertEqual(self.response.json().get(chave), retorno_esperado.get(chave))
