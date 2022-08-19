class FastS3RestBaseException(Exception):
    """
    Exceção base da aplicação.

    :param status_code int: status_code
    :param mensagem str: mensagem de erro
    :return: IATextoS3BaseException
    :rtype: IATextoS3BaseException
    """
    def __init__(self, status_code: int, mensagem: str):
        self.status_code = status_code
        self.mensagem = mensagem


class ObjetoNaoEncontradoException(FastS3RestBaseException):
    """
    Exceção ao não encontrar objeto no.

    :param status_code int: status_code
    :param mensagem str: mensagem de exceção boto3
    :param objeto str: nome/path do objeto
    :return: ObjetoNaoEncontradoException
    :rtype: ObjetoNaoEncontradoException
    """
    def __init__(self, mensagem):
        super().__init__(status_code=404, mensagem=mensagem)


class TokenAcessoInvalido(FastS3RestBaseException):
    """
    Exceção ao invalidar token de acesso.

    :param status_code int: status_code
    :param mensagem str: mensagem de erro
    :return: ObjetoNaoEncontradoException
    :rtype: ObjetoNaoEncontradoException
    """
    def __init__(self):
        super().__init__(status_code=403, mensagem='Token de acesso inválido')
