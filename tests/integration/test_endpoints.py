import io
import unittest

from unittest.mock import patch
from requests.models import Response
from fastapi.responses import StreamingResponse
from fast_s3_rest.utils import bytes_para_base64str

from tests.integration import test_cli


class TestEndpointListar(unittest.TestCase):

    mock_objetos = ['objeto1', 'path/objeto/2']
    mock_retorno = {'objetos': mock_objetos, 'total': len(mock_objetos)}

    @patch('fast_s3_rest.servicos.s3.sec.valida_token', return_value=True)
    @patch('fast_s3_rest.servicos.s3.crud.listar_objetos', return_value=mock_retorno)
    def test_endpoint_listar(self, *args):

        endpoint = 's3/listar'
        response = test_cli.get(endpoint, headers={'x-access-token': '...'})

        chaves_esperadas = {'objetos', 'total'}

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
            self.assertEqual(response.json().get(chave), self.mock_retorno.get(chave))
            self.assertEqual(response.json().get(chave), self.mock_retorno.get(chave))
        self.assertEqual(response.json(), self.mock_retorno)


class TestEndpointPesquisar(unittest.TestCase):

    mock_objetos = ['path/objeto/1.xpto', 'path/objeto/1.xpto', 'path/objeto/1.jpeg']
    mock_path_objeto = 'xpto'
    mock_match = [o for o in mock_objetos if 'xpto' in o]
    mock_retorno = {'objetos': mock_match, 'total': len(mock_match)}

    @patch('fast_s3_rest.servicos.s3.sec.valida_token', return_value=True)
    @patch('fast_s3_rest.servicos.s3.crud.pesquisar_objeto', return_value=mock_retorno)
    def test_endpoint_pesquisar(self, *args):

        endpoint = 's3/pesquisar'
        q = f'?path_objeto={self.mock_path_objeto}'
        response = test_cli.get(endpoint + q, headers={'x-access-token': '...'})

        chaves_esperadas = {'objetos', 'total'}

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
            self.assertEqual(response.json().get(chave), self.mock_retorno.get(chave))
            self.assertEqual(response.json().get(chave), self.mock_retorno.get(chave))
        self.assertEqual(response.json(), self.mock_retorno)


class TestEndpointDownloadB64str(unittest.TestCase):

    mock_path_objeto = 'xpto'
    mock_b64str = 'xptob64str=='
    mock_retorno = {'objeto': mock_path_objeto, 'b64str': mock_b64str}

    @patch('fast_s3_rest.servicos.s3.sec.valida_token', return_value=True)
    @patch('fast_s3_rest.servicos.s3.crud.download_b64str_objeto', return_value=mock_retorno)
    def test_endpoint_download_b64str(self, *args):

        endpoint = 's3/download/b64str'
        q = f'?path_objeto={self.mock_path_objeto}'
        response = test_cli.get(endpoint + q, headers={'x-access-token': '...'})

        chaves_esperadas = {'objeto', 'b64str'}

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
            self.assertEqual(response.json().get(chave), self.mock_retorno.get(chave))
            self.assertEqual(response.json().get(chave), self.mock_retorno.get(chave))
        self.assertEqual(response.json(), self.mock_retorno)


class TestEndpointDownloadArquivo(unittest.TestCase):

    mock_path_objeto = 'xpto.jpeg'
    mock_path_arquivo = '/path/do/arquivo/' + mock_path_objeto
    mock_retorno = {'objeto': mock_path_objeto, 'arquivo': mock_path_arquivo}

    @patch('fast_s3_rest.servicos.s3.sec.valida_token', return_value=True)
    @patch('fast_s3_rest.servicos.s3.crud.download_arquivo_objeto', return_value=mock_retorno)
    def test_endpoint_download_arquivo(self, *args):

        endpoint = 's3/download/arquivo'
        q = f'?path_objeto={self.mock_path_objeto}' + '&' + f'path_arquivo={self.mock_path_arquivo}'
        response = test_cli.get(endpoint + q, headers={'x-access-token': '...'})

        chaves_esperadas = {'objeto', 'arquivo'}

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
            self.assertEqual(response.json().get(chave), self.mock_retorno.get(chave))
            self.assertEqual(response.json().get(chave), self.mock_retorno.get(chave))
        self.assertEqual(response.json(), self.mock_retorno)


class TestEndpointUpload(unittest.TestCase):

    def gen_bytes():
        return io.BytesIO(bytearray(2))

    mock_path_objeto = 'path/objeto'
    mock_bytes = gen_bytes()
    mock_retorno = {'objeto': mock_path_objeto, 'tamanho (bytes)': len(mock_bytes.read())}

    @patch('fast_s3_rest.servicos.s3.crud.upload_objeto', return_value=mock_retorno)
    @patch('fast_s3_rest.servicos.s3.sec.valida_token', return_value=True)
    def test_endpoint_upload(self, *args):

        endpoint = 's3/upload'
        q = f'?path_objeto={self.mock_path_objeto}'
        response = test_cli.put(endpoint + q, files=[('arquivo', self.mock_bytes.read())], headers={'x-access-token': '...'})

        chaves_esperadas = {'objeto', 'tamanho (bytes)'}

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
            self.assertEqual(response.json().get(chave), self.mock_retorno.get(chave))
            self.assertEqual(response.json().get(chave), self.mock_retorno.get(chave))
        self.assertEqual(response.json(), self.mock_retorno)


class TestEndpointGravar(unittest.TestCase):

    mock_path_objeto = 'path/objeto'
    arquivo_bytes = open('README.md', 'rb').read()
    arquivo_b64str = bytes_para_base64str(arquivo_bytes)
    mock_retorno = {'objeto': mock_path_objeto, 'tamanho (bytes)': len(arquivo_bytes)}

    @patch('fast_s3_rest.servicos.s3.crud.grava_bytes', return_value=mock_retorno)
    @patch('fast_s3_rest.servicos.s3.sec.valida_token', return_value=True)
    def test_endpoint_upload(self, *args):

        endpoint = 's3/gravar'
        q = f'?path_objeto={self.mock_path_objeto}'
        dados = {'base64str_objeto': self.arquivo_b64str}
        response = test_cli.post(endpoint + q, json=dados, headers={'x-access-token': '...'})

        chaves_esperadas = {'objeto', 'tamanho (bytes)'}

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
            self.assertEqual(response.json().get(chave), self.mock_retorno.get(chave))
            self.assertEqual(response.json().get(chave), self.mock_retorno.get(chave))
        self.assertEqual(response.json(), self.mock_retorno)


class TestEndpointApagar(unittest.TestCase):

    mock_path_objeto = 'xpto.jpeg'
    mock_status = 204
    mock_retorno = {'objeto': mock_path_objeto, 'status': mock_status}

    @patch('fast_s3_rest.servicos.s3.sec.valida_token', return_value=True)
    @patch('fast_s3_rest.servicos.s3.crud.apagar_objeto', return_value=mock_retorno)
    def test_endpoint_apagar(self, *args):

        endpoint = 's3/apagar'
        q = f'?path_objeto={self.mock_path_objeto}'
        response = test_cli.delete(endpoint + q, headers={'x-access-token': '...'})

        chaves_esperadas = {'objeto', 'status'}

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
            self.assertEqual(response.json().get(chave), self.mock_retorno.get(chave))
            self.assertEqual(response.json().get(chave), self.mock_retorno.get(chave))
        self.assertEqual(response.json(), self.mock_retorno)


class TestEndpointStream(unittest.TestCase):

    mock_path_objeto = 'xpto.jpeg'
    mock_status = 204

    def mock_bytes_chunks(*args, **kwargs):
        for i in range(2):
            yield io.BytesIO(bytearray(1)).read()

    @patch('fast_s3_rest.servicos.s3.sec.valida_token', return_value=True)
    @patch('fast_s3_rest.modulo.crud.stream_chunks', return_value=mock_bytes_chunks())
    @patch('fast_s3_rest.servicos.s3.crud.stream_objeto', return_value=StreamingResponse(mock_bytes_chunks()))
    def test_endpoint_stream(self, *args):

        endpoint = 's3/stream'
        q = f'?path_objeto={self.mock_path_objeto}'
        response = test_cli.get(endpoint + q, headers={'x-access-token': '...'})

        self.assertIsInstance(response, Response)
        self.assertIsInstance(response.status_code, int)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)
        self.assertIn(endpoint, response.url)
        self.assertEqual(response.ok, True)
        self.assertEqual(response._content, b'\x00\x00')
        self.assertIsInstance(response._content, bytes)
