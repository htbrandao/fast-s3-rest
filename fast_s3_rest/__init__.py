__version__ = '1.0.0'

from loguru import logger
from fastapi import FastAPI
from datetime import datetime

from fast_s3_rest.servicos import s3
from fast_s3_rest.servicos.observabilidade import health, metrics
from fast_s3_rest.servicos.excecoes import excecoes_handler

logger.add('log.log', rotation='50 MB')

app = FastAPI(
    title='FAST S3 REST',
    version=__version__,
    docs_url='/swagger',
    redoc_url='/docs'
)


@app.get('/')
def raiz():
    """
    Endpoint raiz do projeto.

    :return: HTTP Response
    :rtype: Response
    """
    logger.info('Request recebida @ /')
    timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    return {
        'versão': f'{__version__}',
        'swagger': '/swagger',
        '@timestamp': timestamp,
    }


app.include_router(s3.roteador, prefix='/s3', tags=['s3'])
app.include_router(health.roteador, prefix='/health', tags=['health'])
app.include_router(metrics.roteador, tags=['metrics'])

excecoes_handler(app)
