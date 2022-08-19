from fastapi import APIRouter
from fastapi.responses import Response
from prometheus_client import generate_latest

from fast_s3_rest import logger

roteador = APIRouter()


@roteador.get('/metrics', summary='Métricas do microsserviço')
def metrics():
    """
    Endpoint. Métricas do microsserviço.

    :return: Response com métricas geradas pelo Prometheus
    :rtype: Response
    """
    logger.info('Request recebida @ /metrics')
    return Response(content=generate_latest(), status_code=200)
