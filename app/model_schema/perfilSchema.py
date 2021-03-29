from typing import Optional
from pydantic import BaseModel, validator, constr
from validate_docbr import CPF, PIS
import ujson

class PerfilAddSchema(BaseModel):
    # mandatory field
    nome: constr(min_length=2, max_length=255)
    pis: constr(min_length=11, max_length=50)
    cpf: constr(min_length=11, max_length=50)
    cep: constr(min_length=2, max_length=20)
    rua: constr(min_length=3, max_length=255)
    numero: constr(min_length=1, max_length=20)
    complemento: Optional[constr(min_length=0, max_length=50)]

    cidade_id: int

    class Config:
        json_loads = ujson.loads


    @validator('cpf')
    def cpf_validator(cls, cpf):
        if CPF().validate(cpf):
            return cpf
        else:
            raise ValueError('O CPF informado é inválido.')

    @validator('pis')
    def pis_validator(cls, pis):
        if PIS().validate(pis):
            return pis
        else:
            raise ValueError('O PIS informado é inválido.')
