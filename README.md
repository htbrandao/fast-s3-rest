# Abstração REST para S3

Criada utilizando FastAPI.

## # Cobertura

```bash
coverage run --source=fast_s3_rest -m pytest
coverage report
```

```text
Name                                                Stmts   Miss  Cover
-----------------------------------------------------------------------
fast_s3_rest/__init__.py                               18      0   100%
fast_s3_rest/__main__.py                                0      0   100%
fast_s3_rest/config.py                                 14      0   100%
fast_s3_rest/excecoes/__init__.py                      10      0   100%
fast_s3_rest/modelos/__init__.py                        3      0   100%
fast_s3_rest/modulo/__init__.py                        20      0   100%
fast_s3_rest/modulo/crud.py                            70      1    99%
fast_s3_rest/modulo/sec.py                             11      0   100%
fast_s3_rest/servicos/__init__.py                       0      0   100%
fast_s3_rest/servicos/excecoes.py                      13      2    85%
fast_s3_rest/servicos/observabilidade/__init__.py       0      0   100%
fast_s3_rest/servicos/observabilidade/health.py        11      0   100%
fast_s3_rest/servicos/observabilidade/metrics.py        9      0   100%
fast_s3_rest/servicos/s3/__init__.py                   36      0   100%
fast_s3_rest/utils/__init__.py                          5      0   100%
-----------------------------------------------------------------------
TOTAL                                                 220      3    99%
```

## # Executar localmente

Preencha (ou exporte) as variáveis em [fast_s3_rest/config.py](fast_s3_rest/config.py)

```bash
uvicorn fast_s3_rest:app --host 0.0.0.0 --port 8000 --reload
```