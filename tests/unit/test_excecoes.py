import unittest

from tests.integration import test_cli

from fast_s3_rest import app
from fast_s3_rest import excecoes
from fast_s3_rest.servicos.excecoes import excecoes_handler


class TestExcecoesAplicacaoIATextoS3BaseException(unittest.TestCase):

    status_code = 400
    mensagem = 'Essa é uma exceção'

    e = excecoes.FastS3RestBaseException(status_code, mensagem)

    def test_status_code(self):
        self.assertEqual(self.e.status_code, self.status_code)

    def test_mensagem(self):
        self.assertEqual(self.e.mensagem, self.mensagem)

    def test_classe(self):
        self.assertIsInstance(self.e, excecoes.FastS3RestBaseException)


class TestExcecoesAplicacaoObjetoNaoEncontradoException(unittest.TestCase):

    status_code = 404
    mensagem = 'Essa é uma exceção'

    e = excecoes.ObjetoNaoEncontradoException(mensagem)

    def test_status_code(self):
        self.assertEqual(self.e.status_code, self.status_code)

    def test_mensagem(self):
        self.assertEqual(self.e.mensagem, self.mensagem)

    def test_classe(self):
        self.assertIsInstance(self.e, excecoes.ObjetoNaoEncontradoException)


class TestExcecoesAplicacaoTokenAcessoInvalido(unittest.TestCase):

    status_code = 403
    mensagem = 'Token de acesso inválido'

    e = excecoes.TokenAcessoInvalido()

    def test_status_code(self):
        self.assertEqual(self.e.status_code, self.status_code)

    def test_mensagem(self):
        self.assertEqual(self.e.mensagem, self.mensagem)

    def test_classe(self):
        self.assertIsInstance(self.e, excecoes.TokenAcessoInvalido)


class TestExcecoesHandler(unittest.TestCase):

    def test_retorno(self):
        self.assertIsNone(excecoes_handler(app))

    def test_raises(self):
        self.assertRaises(AttributeError, excecoes_handler, test_cli)
        self.assertRaises(AttributeError, excecoes_handler, None)
