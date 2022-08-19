from fastapi import APIRouter

from fast_s3_rest import logger

roteador = APIRouter()


@roteador.get('/health', summary='Liveness probe')
def live():
    """
    Endpoint. Responde ao liveness probe.

    :return: True
    :rtype: bool
    """
    logger.info('Request recebida @ /health/live')
    return True


@roteador.get('/ready', summary='Readiness probe')
def ready():
    """
    Endpoint. Responde ao readiness probe.

    :return: True
    :rtype: bool
    """
    logger.info('Request recebida @ /health/ready')
    return True
