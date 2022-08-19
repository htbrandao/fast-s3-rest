import unittest

from unittest.mock import patch
from requests.models import Response

from tests.integration import test_cli


class TestExcecoesEndpointDownloadB64str(unittest.TestCase):

    mock_path_objeto = 'xpto'
    mock_retorno = {'status': 404, 'mensagem': f'Objeto não encontrado. Resultado: {mock_path_objeto}'}

    @patch('fast_s3_rest.servicos.s3.sec.valida_token', return_value=True)
    @patch('fast_s3_rest.servicos.s3.crud.download_b64str_objeto', return_value=mock_retorno)
    def test_endpoint_download_b64str(self, *args):

        endpoint = 's3/download/b64str'
        q = f'?path_objeto={self.mock_path_objeto}'
        response = test_cli.get(endpoint + q, headers={'x-access-token': '...'})

        chaves_esperadas = {'status', 'mensagem'}

        self.assertIsInstance(response, Response)
        self.assertIsInstance(response.status_code, int)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)
        self.assertIn(endpoint, response.url)
        self.assertEqual(response.ok, True)
        self.assertIsInstance(response.json(), dict)
        for chave in chaves_esperadas:
            self.assertIn(chave, response.json().keys())
            self.assertIsInstance(chave, str)
            self.assertIsNotNone(chave)
        self.assertEqual(response.json().get('status'), self.mock_retorno.get('status'))
        self.assertEqual(response.json().get('mensagem'), self.mock_retorno.get('mensagem'))


class TestExcecoesEndpointDownloadArquivo(unittest.TestCase):

    mock_path_objeto = 'xpto'
    mock_path_arquivo = '/xptodir/xpto'
    mock_retorno = {'status': 404, 'mensagem': f'Objeto não encontrado. Resultado: {mock_path_objeto}'}

    @patch('fast_s3_rest.servicos.s3.sec.valida_token', return_value=True)
    @patch('fast_s3_rest.servicos.s3.crud.download_arquivo_objeto', return_value=mock_retorno)
    def test_endpoint_download_arquivo(self, *args):

        endpoint = 's3/download/arquivo'
        q = f'?path_objeto={self.mock_path_objeto}' + '&' + f'path_arquivo={self.mock_path_arquivo}'
        response = test_cli.get(endpoint + q, headers={'x-access-token': '...'})

        chaves_esperadas = {'status', 'mensagem'}

        self.assertIsInstance(response, Response)
        self.assertIsInstance(response.status_code, int)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)
        self.assertIn(endpoint, response.url)
        self.assertEqual(response.ok, True)
        self.assertIsInstance(response.json(), dict)
        for chave in chaves_esperadas:
            self.assertIn(chave, response.json().keys())
            self.assertIsInstance(chave, str)
            self.assertIsNotNone(chave)
        self.assertEqual(response.json().get('status'), self.mock_retorno.get('status'))
        self.assertEqual(response.json().get('mensagem'), self.mock_retorno.get('mensagem'))


class TestExcecoesEndpointUpload(unittest.TestCase):
    # TODOO: implementar
    pass


class TestExcecoesEndpointApagar(unittest.TestCase):

    mock_path_objeto = 'xpto'
    mock_retorno = {'status': 404, 'mensagem': f'Objeto não encontrado. Resultado: {mock_path_objeto}'}

    @patch('fast_s3_rest.servicos.s3.sec.valida_token', return_value=True)
    @patch('fast_s3_rest.servicos.s3.crud.apagar_objeto', return_value=mock_retorno)
    def test_endpoint_apagar(self, *args):

        endpoint = 's3/apagar'
        q = f'?path_objeto={self.mock_path_objeto}'
        response = test_cli.delete(endpoint + q, headers={'x-access-token': '...'})

        chaves_esperadas = {'status', 'mensagem'}

        self.assertIsInstance(response, Response)
        self.assertIsInstance(response.status_code, int)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)
        self.assertIn(endpoint, response.url)
        self.assertEqual(response.ok, True)
        self.assertIsInstance(response.json(), dict)
        for chave in chaves_esperadas:
            self.assertIn(chave, response.json().keys())
            self.assertIsInstance(chave, str)
            self.assertIsNotNone(chave)
        self.assertEqual(response.json().get('status'), self.mock_retorno.get('status'))
        self.assertEqual(response.json().get('mensagem'), self.mock_retorno.get('mensagem'))


class TestExcecoesEndpointStream(unittest.TestCase):

    mock_path_objeto = 'xpto'
    mock_retorno = {'status': 404, 'mensagem': f'Objeto não encontrado. Resultado: {mock_path_objeto}'}

    @patch('fast_s3_rest.servicos.s3.sec.valida_token', return_value=True)
    @patch('fast_s3_rest.servicos.s3.crud.stream_objeto', return_value=mock_retorno)
    def test_endpoint_stream(self, *args):

        endpoint = 's3/stream'
        q = f'?path_objeto={self.mock_path_objeto}'
        response = test_cli.get(endpoint + q, headers={'x-access-token': '...'})

        chaves_esperadas = {'status', 'mensagem'}

        self.assertIsInstance(response, Response)
        self.assertIsInstance(response.status_code, int)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)
        self.assertIn(endpoint, response.url)
        self.assertEqual(response.ok, True)
        self.assertIsInstance(response.json(), dict)
        for chave in chaves_esperadas:
            self.assertIn(chave, response.json().keys())
            self.assertIsInstance(chave, str)
            self.assertIsNotNone(chave)
        self.assertEqual(response.json().get('status'), self.mock_retorno.get('status'))
        self.assertEqual(response.json().get('mensagem'), self.mock_retorno.get('mensagem'))
