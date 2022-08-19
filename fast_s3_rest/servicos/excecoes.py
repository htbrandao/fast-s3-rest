from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from fast_s3_rest import excecoes as e


def excecoes_handler(app: FastAPI):
    """
    Realiza a injeção das exceções para tratamento pela aplicação.
    """

    @app.exception_handler(e.FastS3RestBaseException)
    async def handler_excecao_base(requisicao: Request, excecao: e.FastS3RestBaseException):
        """
        Handler para FastAPI para erro básico da aplicação.
        """
        return JSONResponse(
            status_code=excecao.status_code,
            content={
                'status': excecao.status_code,
                'mensagem': excecao.mensagem
            }
        )

    @app.exception_handler(e.ObjetoNaoEncontradoException)
    async def handler_excecao_objeto_nao_encontrado(requisicao: Request, excecao: e.ObjetoNaoEncontradoException):
        """
        Handler para FastAPI para erro de objeto não encontrado.
        """
        return JSONResponse(
            status_code=excecao.status_code,
            content={
                'status': excecao.status_code,
                'mensagem': excecao.mensagem,
            }
        )

    @app.exception_handler(e.TokenAcessoInvalido)
    async def handler_excecao_token_acesso_invalido(requisicao: Request, excecao: e.TokenAcessoInvalido):
        """
        Handler para FastAPI para erro na invalidação do token.
        """
        return JSONResponse(
            status_code=excecao.status_code,
            content={
                'status': excecao.status_code,
                'mensagem': excecao.mensagem
            }
        )
