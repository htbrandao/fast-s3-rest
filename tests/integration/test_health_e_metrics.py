import unittest

from requests.models import Response

from tests.integration import test_cli

from fast_s3_rest import __version__


class TestEndpointDefault(unittest.TestCase):

    resposta_esperada = {
        'versão': __version__,
        'swagger': '/swagger',
        '@timestamp': '22-02-2022 20:08:02'
    }
    chaves_esperadas = [*resposta_esperada.keys()]

    endpoint = '/'
    response = test_cli.get(endpoint)

    def test_response(self):
        self.assertIsInstance(self.response, Response)
        self.assertIsInstance(self.response.status_code, int)

    def test_conteudo_response(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertIsNotNone(self.response.content)

    def test_consistencia_response(self):
        self.assertIn(self.endpoint, self.response.url)
        self.assertEqual(self.response.ok, True)

    def test_congruencia_response(self):
        self.assertIsInstance(self.response.json(), dict)
        for chave in self.chaves_esperadas:
            self.assertIn(chave, self.response.json().keys())
            self.assertIsInstance(chave, str)
            self.assertIsNotNone(chave)
            if chave != '@timestamp':
                self.assertEqual(self.response.json().get(chave), self.resposta_esperada.get(chave))


class TestEndpointHealthHealth(unittest.TestCase):

    endpoint = '/health/health'
    response = test_cli.get(endpoint)

    def test_response(self):
        self.assertIsInstance(self.response, Response)
        self.assertIsInstance(self.response.status_code, int)

    def test_conteudo_response(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertIsNotNone(self.response.content)

    def test_consistencia_response(self):
        self.assertIn(self.endpoint, self.response.url)
        self.assertEqual(self.response.ok, True)

    def test_congruencia_response(self):
        self.assertIsInstance(self.response._content, bytes)
        self.assertEqual(self.response.text, 'true')


class TestEndpointHealthReady(unittest.TestCase):

    endpoint = '/health/ready'
    response = test_cli.get(endpoint)

    def test_response(self):
        self.assertIsInstance(self.response, Response)
        self.assertIsInstance(self.response.status_code, int)

    def test_conteudo_response(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertIsNotNone(self.response.content)

    def test_consistencia_response(self):
        self.assertIn(self.endpoint, self.response.url)
        self.assertEqual(self.response.ok, True)

    def test_congruencia_response(self):
        self.assertIsInstance(self.response._content, bytes)
        self.assertEqual(self.response.text, 'true')


class TestEndpointMetrics(unittest.TestCase):

    endpoint = '/metrics'
    response = test_cli.get(endpoint)

    def test_response(self):
        self.assertIsInstance(self.response, Response)
        self.assertIsInstance(self.response.status_code, int)

    def test_conteudo_response(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertIsNotNone(self.response.content)

    def test_consistencia_response(self):
        self.assertIn(self.endpoint, self.response.url)
        self.assertEqual(self.response.ok, True)

    def test_congruencia_response(self):
        self.assertIsInstance(self.response._content, bytes)

    def test_texto(self):
        tx = [linha for linha in self.response.text.split('\n')]
        for linha in tx:
            self.assertIsNotNone(linha)
            self.assertIsInstance(linha, str)
