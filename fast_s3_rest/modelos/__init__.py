from pydantic import BaseModel


class BodyObjetoB64Str(BaseModel):
    """
    Classe para representar receber a str base64 de um arquivo no body da requisição.
    """
    base64str_objeto: str
