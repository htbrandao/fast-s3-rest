import io
import functools

from botocore.exceptions import ClientError
from fastapi.responses import StreamingResponse

from fast_s3_rest import logger
from fast_s3_rest.config import config_conn
from fast_s3_rest.utils import bytes_para_base64str, base64str_para_bytes
from fast_s3_rest.modulo import meu_cliente_S3, meu_resource_S3, meu_bucket_S3
from fast_s3_rest.excecoes import ObjetoNaoEncontradoException, FastS3RestBaseException


def listar_objetos(bucket=meu_bucket_S3):
    """
    Lista objetos no bucket.

    :param boto3.Resource.Bucket bucket: bucket s3
    :return: dict
    :rtype: dict
    """
    objetos = [o.key for o in bucket.objects.all()]
    return {
        'objetos': objetos,
        'total': len(objetos)
    }


def pesquisar_objeto(path_objeto: str):
    """
    Efetua uma pesquisa dentre os objetos do bucket.

    :param str path_objeto: path_objeto
    :return: dict
    :rtype: dict
    """
    objetos = [o for o in listar_objetos().get('objetos') if path_objeto in o]
    return {
        'objetos': objetos,
        'total': len(objetos)
    }


def objeto_existe(func):
    """
    Wrapper para verificar se objeto existe no bucket.

    :param function func: função a ser decorada
    :return: wrapper
    :rtype: function
    :raises: ObjetoNaoEncontradoException
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if args:
            path_obj = args[0]
            if path_obj in listar_objetos().get('objetos'):
                return func(*args, **kwargs)
            else:
                raise ObjetoNaoEncontradoException(mensagem=f'Objeto não encontrado. Resultado: {path_obj}')
        elif kwargs:
            path_obj = kwargs.get('path_objeto', '')
            if path_obj in listar_objetos().get('objetos'):
                return func(*args, **kwargs)
            else:
                raise ObjetoNaoEncontradoException(mensagem=f'Objeto não encontrado. Resultado: {path_obj}')
    return wrapper


@objeto_existe
def download_b64str_objeto(path_objeto: str, resource=meu_resource_S3):
    """
    Retonar os bytes de um objeto do bucket como str base 64.

    :param str path_objeto: path_objeto
    :param Resource resource: resource s3
    :return: dict
    :rtype: dict
    :raises: ObjetoNaoEncontradoException
    """
    objeto = resource.Object(bucket_name=config_conn.vol_name, key=path_objeto)
    bytes_objeto = objeto.get()['Body'].read()
    bytes_objeto = bytes_para_base64str(bytes_objeto)
    return {
        'objeto': path_objeto,
        'b64str': bytes_objeto
    }


@objeto_existe
def download_arquivo_objeto(path_objeto: str, path_arquivo: str, client=meu_cliente_S3):
    """
    Retona os bytes de um objeto do bucket para arquivo no file system.

    :param str path_objeto: path_objeto
    :param str path_arquivo: path_arquivo
    :param Client client: client s3
    :return: dict
    :rtype: dict
    :raises: ObjetoNaoEncontradoException
    """
    client.download_file(config_conn.vol_name, path_objeto, path_arquivo)
    return {
        'objeto': path_objeto,
        'arquivo': path_arquivo
    }


def upload_objeto(path_objeto: str, arquivo, client=meu_cliente_S3):
    """
    Efetua o upload de um arquivo para o bucket.

    :param str path_objeto: path_objeto
    :param fastapi.File arquivo: arquivo
    :param boto3.Client client: client s3
    :return: dict
    :rtype: dict
    :raises: BBS3BaseException
    """
    arquivo_bytes = arquivo.file._file
    tamanho_objeto = arquivo.file._max_size
    try:
        client.upload_fileobj(arquivo_bytes, config_conn.vol_name, path_objeto)
        return {
           'objeto': path_objeto,
           'tamanho (bytes)': tamanho_objeto,
        }
    except ClientError as e:
        logger.error(e)
        raise FastS3RestBaseException(500, e)


def grava_bytes(path_objeto: str, base64str_objeto: str, client=meu_cliente_S3):
    """
    Converte str b64 eealiza a escrita de bytes no bucket.

    :param str path_objeto: path_objeto
    :param str base64str_objeto: str base64 do objeto
    :param boto3.Client client: client s3
    :return: dict
    :rtype: dict
    :raises: BBS3BaseException
    """
    bytes_objeto = base64str_para_bytes(base64str_objeto)
    try:
        client.upload_fileobj(io.BytesIO(bytes_objeto), config_conn.vol_name, path_objeto)
        return {
            'objeto': path_objeto,
            'tamanho (bytes)': len(bytes_objeto),
        }
    except ClientError as e:
        logger.error(e)
        raise FastS3RestBaseException(500, e)


@objeto_existe
def apagar_objeto(path_objeto: str, client=meu_cliente_S3):
    """
    Apaga um objeto do bucket.

    :param str path_objeto: path_objeto
    :param boto3.Client client: client s3
    :return: dict
    :rtype: dict
    :raises: ObjetoNaoEncontradoException
    """
    retorno = client.delete_object(Bucket=config_conn.vol_name, Key=path_objeto)
    return {
        'objeto': path_objeto,
        'status': retorno.get('ResponseMetadata').get('HTTPStatusCode')
    }


def stream_chunks(body_bytes: bytes, chunk_size=1073741824) -> bytes:  # 1mb
    """
    Iterator que realiza a leitura de um bytearray.

    :param bytes body_bytes: objeto byte-like com .read()
    :returns: iterator
    :rtype: iterator(bytes)
    """
    while body_bytes:
        chunk = body_bytes.read(chunk_size)
        if chunk:
            yield chunk
        else:
            break


@objeto_existe
def stream_objeto(path_objeto: str, resource=meu_resource_S3):
    """
    Realiza o streamming de um objeto do bucket.

    :param str path_objeto: path_objeto
    :param boro3.Resource resource: resource s3
    :return: byte chunk do arquivo
    return StreamingResponse
    :rtype: bytes
    :raises: ObjetoNaoEncontradoException
    """
    body_bytes = resource.Object(bucket_name=config_conn.vol_name, key=path_objeto).get()['Body']
    return StreamingResponse(stream_chunks(body_bytes=body_bytes))
