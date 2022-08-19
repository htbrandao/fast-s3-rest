from fastapi import File, UploadFile, APIRouter, Depends

from fast_s3_rest import logger
from fast_s3_rest.modulo import sec, crud
from fast_s3_rest.modelos import BodyObjetoB64Str

roteador = APIRouter(dependencies=[Depends(sec.verifica_token)])


@roteador.get('/listar', summary='Lista todos os objetos no bucket.')
def listar():
    """
    Endpoint. Lista objetos no bucket.

    :return: HTTP Response
    :rtype: Response
    """
    logger.info('Request recebida @ /listar')
    return crud.listar_objetos()


@roteador.get('/pesquisar', summary='Pesquisa por um objeto no bucket')
def pesquisar(path_objeto: str):
    """
    Endpoint. Efetua uma pesquisa dentre os objetos do bucket.

    :param str path_objeto: path_objeto
    :return: HTTP Response
    :rtype: Response
    """
    logger.info(f'Request recebida @ /pesquisar: {path_objeto}')
    return crud.pesquisar_objeto(path_objeto)


@roteador.get('/download/b64str', summary='Converte um arquivo para b64str')
def download_b64str(path_objeto: str):
    """
    Endpoint. Retonar os bytes de um objeto do bucket como str base 64.

    :param str path_objeto: path_objeto
    :return: HTTP Response
    :rtype: Response
    """
    logger.info(f'Request recebida @ /download/b64str: {path_objeto}')
    return crud.download_b64str_objeto(path_objeto)


@roteador.get('/download/arquivo', summary='Realiza o download de um objeto para o disco.')
def download_arquivo(path_objeto: str, path_arquivo: str):
    """
    Endpoint. Retona os bytes de um objeto do bucket para arquivo no file system.

    :param str path_objeto: path_objeto
    :param str path_arquivo: path_arquivo
    :return: HTTP Response
    :rtype: Response
    """
    logger.info(f'Request recebida @ /download/arquivo: {path_objeto}')
    return crud.download_arquivo_objeto(path_objeto, path_arquivo)


@roteador.put('/upload', summary='Efetua o upload de um arquivo para o bucket.')
def upload(path_objeto: str, arquivo: UploadFile = File(...)):
    """
    Endpoint. Efetua o upload de um arquivo para o bucket.

    :param str path_objeto: path_objeto
    :param fastapi.File arquivo: arquivo
    :return: HTTP Response
    :rtype: Response
    """
    logger.info(f'Request recebida @ /upload: {path_objeto}')
    return crud.upload_objeto(path_objeto, arquivo)


@roteador.post('/gravar', summary='Converte str b64 eealiza a escrita de bytes no bucket.')
def gravar(path_objeto: str, base64str_objeto: BodyObjetoB64Str):
    """
    Endpoint. Converte str b64 eealiza a escrita de bytes no bucket.

    :param str path_objeto: path_objeto
    :param str base64str_objeto: str base64 dos bytes do objeto a ser escrito
    :return: HTTP Response
    :rtype: Response
    """
    logger.info(f'Request recebida @ /gravar: {path_objeto}')
    return crud.grava_bytes(path_objeto, base64str_objeto.base64str_objeto)


@roteador.delete('/apagar', summary='Apaga um arquivo do bucket.')
def apagar(path_objeto: str):
    """
    Endpoint. Apaga um objeto do bucket.

    :param str path_objeto: path_objeto
    :return: HTTP Response
    :rtype: Response
    """
    logger.info(f'Request recebida @ /apagar: {path_objeto}')
    return crud.apagar_objeto(path_objeto)


@roteador.get('/stream', summary='Lista todos os objetos no bucket.')
def stream(path_objeto: str):
    """
    Endpoint. Realiza o streamming de um objeto do bucket.

    :param str path_objeto: path_objeto
    :return: HTTP Response
    :rtype: Response
    """
    return crud.stream_objeto(path_objeto)
