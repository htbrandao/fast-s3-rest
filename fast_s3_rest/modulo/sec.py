from time import sleep

from fastapi import Header
from fast_s3_rest.config import config_conn
from fast_s3_rest.excecoes import TokenAcessoInvalido

TOKEN_VERDADE = config_conn.token


def valida_token(token, verdade=TOKEN_VERDADE):
    """
    Efetua a validação do valor do token.

    :returns: True/False se o token for vãlido ou não
    :rtype: bool
    """
    return token == verdade


def verifica_token(x_access_token: str = Header(..., description='Token de acesso')):
    """
    Função de dependência da validação do token de acesso.

    :param str x_access_token:
    :raises: TokenAcessoInvalido
    """
    if not valida_token(x_access_token):
        sleep(1)  # contramedida
        raise TokenAcessoInvalido()
