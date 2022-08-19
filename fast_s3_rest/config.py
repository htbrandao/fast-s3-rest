from os import getenv

from fast_s3_rest import logger


class Config:
    """
    Classe para atributos de configuração da aplicação.
    """

    ambiente = {'d': 'DESENVOLVIMENTO', 'h': 'HOMOLOGAÇÃO', 'p': 'PRODUÇÃO'}

    signature_version: str = getenv('SIGNATURE_VERSION', 'v4')       # preencher/exportar
    region: str = getenv('REGION', 'CQD')                            # preencher/exportar
    vol_name: str = getenv('VOL_NAME', 'des-qdvol001')               # preencher/exportar
    endpoint: str = getenv('ENDPOINT', 'http://storage.cqd.com.br')  # preencher/exportar
    url: str = f'{endpoint}/{vol_name}'
    key_id: str = getenv('ACCESS_KEY_ID', '')                        # preencher/exportar
    secret: str = getenv('SECRET_ACCESS_KEY', '')                    # preencher/exportar
    token: str = getenv('X_ACCESS_TOKEN', '')                        # preencher/exportar

    logger.info(f'Bucket de {ambiente[vol_name[0]]}')


config_conn = Config()
