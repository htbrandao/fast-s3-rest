from base64 import b64encode, b64decode


def bytes_para_base64str(arquivo: bytes):
    """
    Converte um bytearray para uma string b64.

    :param arquivo: Bytearray do arquivo
    :return: str
    """
    return b64encode(arquivo).decode('utf-8')


def base64str_para_bytes(arquivo: str):
    """
    Converte uma string b64 para bytearray.

    :param arquivo: str
    :return: bytes
    """
    return b64decode(arquivo.encode('utf-8'))
