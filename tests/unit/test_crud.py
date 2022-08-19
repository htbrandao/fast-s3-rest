import io
import unittest

from types import FunctionType
from unittest.mock import Mock, patch
from botocore.exceptions import ClientError
from fastapi.responses import StreamingResponse

from fast_s3_rest.modulo import crud
from fast_s3_rest.utils import bytes_para_base64str
from fast_s3_rest.excecoes import ObjetoNaoEncontradoException, FastS3RestBaseException

TAM = 2


class TestListarObjetos(unittest.TestCase):

    def test_listar_objetos(self):

        mock_bucket = Mock(objects=Mock(all=lambda *args, **kwargs: [Mock(key=f'path/algum/objeto/{i}') for i in range(TAM)]))
        resultado = crud.listar_objetos(mock_bucket)

        _o = [f'path/algum/objeto/{i}' for i in range(TAM)]
        _t = len(_o)
        resultado_esperado = {'objetos': _o, 'total': _t}
        chaves_esperadas = resultado_esperado.keys()

        self.assertIsNotNone(resultado)
        self.assertIsInstance(resultado, dict)
        for k in resultado:
            self.assertIn(k, chaves_esperadas)
            self.assertIsNotNone(resultado.get(k))
            self.assertEqual(resultado.get(k), resultado_esperado.get(k))
            self.assertEqual(resultado.get(k), resultado_esperado.get(k))
        self.assertIsInstance(resultado.get('objetos'), list)
        self.assertIsInstance(resultado.get('total'), int)
        self.assertEqual(resultado, resultado_esperado)


class TestPesquisarObjetos(unittest.TestCase):

    path_bjeto = 'objeto'
    mock_listar_objetos = {'objetos': [f'path/objeto/{i+10}' for i in range(TAM)]}
    mock_listar_objetos.get('objetos').append('esse/nao/999')

    @patch('fast_s3_rest.modulo.crud.listar_objetos', return_value=mock_listar_objetos)
    def test_pesquisar_objetos(self, *args):

        _o = [o for o in self.mock_listar_objetos.get('objetos') if self.path_bjeto in o]
        resultado_esperado = {'objetos': _o, 'total': len(_o)}
        chaves_esperadas = resultado_esperado.keys()

        resultado = crud.pesquisar_objeto(self.path_bjeto)

        self.assertIsNotNone(resultado)
        self.assertIsInstance(resultado, dict)
        for k in resultado:
            self.assertIn(k, chaves_esperadas)
            self.assertIsNotNone(resultado.get(k))
            self.assertEqual(resultado.get(k), resultado_esperado.get(k))
            self.assertEqual(resultado.get(k), resultado_esperado.get(k))
        self.assertIsInstance(resultado.get('objetos'), list)
        self.assertIsInstance(resultado.get('total'), int)
        self.assertEqual(resultado, resultado_esperado)


class TestObjetoExiste(unittest.TestCase):

    def myfunc(*args, **kwargs):
        if args:
            return args
        elif kwargs:
            return kwargs

    encontrado = 'path/objeto/200'
    nao_encontrado = 'path/objeto/404'

    @patch('fast_s3_rest.modulo.crud.listar_objetos', return_value={'objetos': [encontrado]})
    def test_objeto_existe_sucesso(self, *args):

        resultado_args = crud.objeto_existe(self.myfunc(self.encontrado))
        self.assertIsNotNone(resultado_args)
        self.assertIsInstance(resultado_args, FunctionType)

        resultado_kwargs = crud.objeto_existe(self.myfunc(path_objeto=self.encontrado))
        self.assertIsNotNone(resultado_kwargs)
        self.assertIsInstance(resultado_kwargs, FunctionType)

    @patch('fast_s3_rest.modulo.crud.listar_objetos', return_value={'objetos': []})
    def test_objeto_existe_falha(self, *args):

        resultado_args = crud.objeto_existe(self.myfunc(self.nao_encontrado))
        self.assertIsNotNone(resultado_args)
        self.assertIsInstance(resultado_args, FunctionType)

        resultado_kwargs = crud.objeto_existe(self.myfunc(path_objeto=self.nao_encontrado))
        self.assertIsNotNone(resultado_kwargs)
        self.assertIsInstance(resultado_kwargs, FunctionType)


class TestDecoratorObjetoExiste(unittest.TestCase):

    def _myfunc(*args, **kwargs):
        if args:
            return args
        elif kwargs:
            return kwargs

    encontrado = 'path/objeto/200'
    nao_encontrado = 'path/objeto/404'

    @patch('fast_s3_rest.modulo.crud.listar_objetos', return_value={'objetos': [encontrado, encontrado]})
    def test_objeto_existe_sucesso(self, *args):

        @crud.objeto_existe
        def myfunc(*args, **kwargs):
            return self._myfunc(*args, **kwargs)

        resultado_args = crud.objeto_existe(myfunc(self.encontrado))
        self.assertIsNotNone(resultado_args)
        self.assertIsInstance(resultado_args, FunctionType)

        resultado_kwargs = crud.objeto_existe(myfunc(path_objeto=self.encontrado))
        self.assertIsNotNone(resultado_kwargs)
        self.assertIsInstance(resultado_kwargs, FunctionType)

    @patch('fast_s3_rest.modulo.crud.listar_objetos', return_value={'objetos': []})
    def test_objeto_existe_falha(self, *args):

        @crud.objeto_existe
        def myfunc(*args, **kwargs):
            return self._myfunc(*args, **kwargs)

        self.assertRaises(ObjetoNaoEncontradoException, myfunc, self.nao_encontrado)
        self.assertRaises(ObjetoNaoEncontradoException, myfunc, path_objeto=self.nao_encontrado)


class TestDownloadB64strObjetoSucesso(unittest.TestCase):

    path_objeto = 'path/objeto/existe/SIM'
    mock_b64str = bytes_para_base64str(bytearray(TAM))
    mock_listar_objetos = {'objetos': [f'{path_objeto}']}

    @patch('fast_s3_rest.modulo.crud.listar_objetos', return_value=mock_listar_objetos)
    def test_download_b64str_objeto_sucesso(self, *args):

        mock_resource = Mock(Object=lambda *args, **kwargs: Mock(get=lambda *args, **kwargs: {'Body': io.BytesIO(bytearray(TAM))}))
        resultado = crud.download_b64str_objeto(self.path_objeto, mock_resource)

        resultado_esperado = {'objeto': self.path_objeto, 'b64str': self.mock_b64str}
        chaves_esperadas = resultado_esperado.keys()

        self.assertIsNotNone(resultado)
        self.assertIsInstance(resultado, dict)
        for k in resultado:
            self.assertIn(k, chaves_esperadas)
            self.assertIsNotNone(resultado.get(k))
            self.assertEqual(resultado.get(k), resultado_esperado.get(k))
            self.assertEqual(resultado.get(k), resultado_esperado.get(k))
        self.assertIsInstance(resultado.get('objeto'), str)
        self.assertIsInstance(resultado.get('b64str'), str)
        self.assertEqual(resultado, resultado_esperado)


class TestDownloadB64strObjetoFalha(unittest.TestCase):

    path_objeto = 'path/objeto/existe/NÃO'
    mock_listar_objetos = {'objetos': []}

    @patch('fast_s3_rest.modulo.crud.listar_objetos', return_value=mock_listar_objetos)
    def test_download_b64str_objeto_falha(self, *args):

        mock_resource = Mock(Object=lambda *args, **kwargs: Mock(get=lambda *args, **kwargs: {'Body': io.BytesIO(bytearray(TAM))}))

        self.assertRaises(ObjetoNaoEncontradoException, crud.download_b64str_objeto, self.path_objeto, mock_resource)


class TestDownloadArquivoObjetoSucesso(unittest.TestCase):

    path_objeto = 'path/objeto'
    path_arquivo = 'path/arquivo/local'
    mock_listar_objetos = {'objetos': [f'{path_objeto}']}

    @patch('fast_s3_rest.modulo.crud.listar_objetos', return_value=mock_listar_objetos)
    def test_download_arquivo_objeto_sucesso(self, *args):

        mock_client = Mock(download_file=lambda *args, **kwargs: None)
        resultado = crud.download_arquivo_objeto(self.path_objeto, self.path_arquivo, mock_client)

        resultado_esperado = {'objeto': self.path_objeto, 'arquivo': self.path_arquivo}
        chaves_esperadas = resultado_esperado.keys()

        self.assertIsNotNone(resultado)
        self.assertIsInstance(resultado, dict)
        for k in resultado:
            self.assertIn(k, chaves_esperadas)
            self.assertIsNotNone(resultado.get(k))
            self.assertEqual(resultado.get(k), resultado_esperado.get(k))
            self.assertEqual(resultado.get(k), resultado_esperado.get(k))
        self.assertIsInstance(resultado.get('objeto'), str)
        self.assertIsInstance(resultado.get('arquivo'), str)
        self.assertEqual(resultado, resultado_esperado)


class TestDownloadArquivoObjetoFalha(unittest.TestCase):

    path_objeto = 'path/objeto'
    path_arquivo = 'path/arquivo/local'
    mock_listar_objetos = {'objetos': []}

    @patch('fast_s3_rest.modulo.crud.listar_objetos', return_value=mock_listar_objetos)
    def test_download_arquivo_objeto_falha(self, *args):

        mock_client = Mock(download_file=lambda *args, **kwargs: None)

        self.assertRaises(ObjetoNaoEncontradoException, crud.download_arquivo_objeto, self.path_objeto, self.path_arquivo, mock_client)


class TestUploadObjeto(unittest.TestCase):

    class MockArquivo:

        class MockFile:
            _file = io.BytesIO(bytearray(TAM))
            _max_size = TAM

        file = MockFile()

    path_objeto = 'path/objeto'
    mock_arquivo = MockArquivo()

    def test_upload_objeto_sucesso(self):

        mock_client = Mock(upload_fileobj=lambda *args, **kwargs: None)

        resultado = crud.upload_objeto(self.path_objeto, self.mock_arquivo, mock_client)

        resultado_esperado = {'objeto': self.path_objeto, 'tamanho (bytes)': TAM}
        chaves_esperadas = resultado_esperado.keys()

        self.assertIsNotNone(resultado)
        self.assertIsInstance(resultado, dict)
        for k in resultado:
            self.assertIn(k, chaves_esperadas)
            self.assertIsNotNone(resultado.get(k))
            self.assertEqual(resultado.get(k), resultado_esperado.get(k))
            self.assertEqual(resultado.get(k), resultado_esperado.get(k))
        self.assertIsInstance(resultado.get('objeto'), str)
        self.assertIsInstance(resultado.get('tamanho (bytes)'), int)
        self.assertEqual(resultado, resultado_esperado)

    def test_upload_objeto_falha(self):

        class Mockclient:
            def upload_fileobj(self, *args, **kwargs):
                raise ClientError({'Erro': ''}, '')

        mock_client = Mockclient()

        self.assertRaises(FastS3RestBaseException, crud.upload_objeto, self.path_objeto, self.mock_arquivo, mock_client)


class TestGravaObjeto(unittest.TestCase):

    path_objeto = 'path/objeto'
    arquivo_bytes = open('README.md', 'rb').read()
    arquivo_b64str = bytes_para_base64str(arquivo_bytes)
    TAM = len(arquivo_bytes)

    def test_grava_bytes_objeto_sucesso(self):

        mock_client = Mock(upload_fileobj=lambda *args, **kwargs: None)

        resultado = crud.grava_bytes(self.path_objeto, self.arquivo_b64str, mock_client)

        resultado_esperado = {'objeto': self.path_objeto, 'tamanho (bytes)': self.TAM}
        chaves_esperadas = resultado_esperado.keys()

        self.assertIsNotNone(resultado)
        self.assertIsInstance(resultado, dict)
        for k in resultado:
            self.assertIn(k, chaves_esperadas)
            self.assertIsNotNone(resultado.get(k))
            self.assertEqual(resultado.get(k), resultado_esperado.get(k))
            self.assertEqual(resultado.get(k), resultado_esperado.get(k))
        self.assertIsInstance(resultado.get('objeto'), str)
        self.assertIsInstance(resultado.get('tamanho (bytes)'), int)
        self.assertEqual(resultado, resultado_esperado)

    def test_grava_bytes_objeto_falha(self):

        class Mockclient:
            def upload_fileobj(self, *args, **kwargs):
                raise ClientError({'Erro': ''}, '')

        mock_client = Mockclient()

        self.assertRaises(FastS3RestBaseException, crud.grava_bytes, self.path_objeto, self.arquivo_b64str, mock_client)


class TestApagarObjetoSucesso(unittest.TestCase):

    path_objeto = 'path/objeto'
    mock_listar_objetos = {'objetos': [f'{path_objeto}']}

    @patch('fast_s3_rest.modulo.crud.listar_objetos', return_value=mock_listar_objetos)
    def test_apagar_objeto_sucesso(self, *args):

        mock_client = Mock(delete_object=lambda *args, **kwargs: {'ResponseMetadata': {'HTTPStatusCode': 204}})
        resultado = crud.apagar_objeto(self.path_objeto, mock_client)

        resultado_esperado = {'objeto': self.path_objeto, 'status': 204}
        chaves_esperadas = resultado_esperado.keys()

        self.assertIsNotNone(resultado)
        self.assertIsInstance(resultado, dict)
        for k in resultado:
            self.assertIn(k, chaves_esperadas)
            self.assertIsNotNone(resultado.get(k))
            self.assertEqual(resultado.get(k), resultado_esperado.get(k))
            self.assertEqual(resultado.get(k), resultado_esperado.get(k))
        self.assertIsInstance(resultado.get('objeto'), str)
        self.assertIsInstance(resultado.get('status'), int)
        self.assertEqual(resultado, resultado_esperado)


class TestApagarObjetoFalha(unittest.TestCase):

    path_objeto = 'path/objeto'
    mock_listar_objetos = {'objetos': []}

    @patch('fast_s3_rest.modulo.crud.listar_objetos', return_value=mock_listar_objetos)
    def test_apagar_objeto_falha(self, *args):

        mock_client = Mock(download_file=lambda *args, **kwargs: None)

        self.assertRaises(ObjetoNaoEncontradoException, crud.apagar_objeto, self.path_objeto, mock_client)


class TestStreamChunks(unittest.TestCase):

    def test_stream_chunks(self):

        def body_bytes():
            return io.BytesIO(bytearray(TAM))

        resultado = crud.stream_chunks(body_bytes=body_bytes())
        resultado_esperado = body_bytes().read()

        self.assertIsNotNone(resultado)
        self.assertEqual([*resultado][0], resultado_esperado)
        for chunk in resultado:
            self.assertIsInstance(chunk, bytes)


class TestStreamObjetoSucesso(unittest.TestCase):

    path_objeto = 'path/objeto'
    mock_listar_objetos = {'objetos': [f'{path_objeto}']}

    @patch('fast_s3_rest.modulo.crud.listar_objetos', return_value=mock_listar_objetos)
    def test_stream_objeto_sucesso(self, *args):

        def body_bytes():
            return io.BytesIO(bytearray(TAM))

        mock_resource = Mock(Object=lambda *args, **kwargs: Mock(get=lambda *args, **kwargs: {'Body': body_bytes()}))
        resultado = crud.stream_objeto(self.path_objeto, mock_resource)

        self.assertIsNotNone(resultado)
        self.assertIsInstance(resultado, StreamingResponse)
        self.assertEqual(resultado.charset, 'utf-8')


class TestStreamObjetoFalha(unittest.TestCase):

    path_objeto = 'path/objeto'
    mock_listar_objetos = {'objetos': []}

    @patch('fast_s3_rest.modulo.crud.listar_objetos', return_value=mock_listar_objetos)
    def test_stream_objeto_falha(self, *args):

        def body_bytes():
            return io.BytesIO(bytearray(TAM))

        mock_resource = Mock(Object=Mock(get=lambda *args, **kwargs: {'Body': body_bytes()}))

        self.assertRaises(ObjetoNaoEncontradoException, crud.stream_objeto, self.path_objeto, mock_resource)
