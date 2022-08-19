import boto3
from botocore.config import Config

from fast_s3_rest import logger
from fast_s3_rest.config import config_conn


params = {
    'service_name': 's3',
    'use_ssl': False,
    'aws_access_key_id': config_conn.key_id,
    'aws_secret_access_key': config_conn.secret,
    'endpoint_url': config_conn.endpoint,
    'config': Config(
            region_name=config_conn.region,
            s3={'addressing_style': 'path'},
            retries={'max_attempts': 1, 'mode': 'standard'}
        )
}


def _client():
    """
    Cria representação de `client`.
    """
    return boto3.client(**params)


def _resource():
    """
    Cria representação de `resource`.
    """
    return boto3.resource(**params)


def _bucket():
    """
    Cria representação de `bucket`.
    """
    return _resource().Bucket(config_conn.vol_name)


def _representacoes():
    """
    Cria as representação dos objetos `client`, `resource` e `bucket`.
    """
    logger.info(f'Criando representação de Client para {config_conn.endpoint}')
    client = _client()
    logger.info(f'Criando representação de Resource para {config_conn.endpoint}')
    resource = _resource()
    logger.info(f'Criando representação de Bucket para {config_conn.url}')
    bucket = _bucket()
    return client, resource, bucket


meu_cliente_S3, meu_resource_S3, meu_bucket_S3 = _representacoes()
