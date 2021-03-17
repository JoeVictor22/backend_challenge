from typing import Optional
import re
from pydantic import BaseModel, validator, constr
from app import Usuario
from validate_docbr import CPF, PIS

class PessoaAddSchema(BaseModel):
    # mandatory field
    nome: constr(min_length=5, max_length=255)
    pis: constr(min_length=11, max_length=50)
    cpf: constr(min_length=11, max_length=50)
    cep: constr(min_length=2, max_length=20)
    rua: constr(min_length=5, max_length=255)
    numero: constr(min_length=1, max_length=20)
    complemento: Optional[constr(min_length=5, max_length=50)]

    cidade_id: int

    # custom validation on email field
    @validator('cpf')
    def cpf_valid(cls, cpf):
        if CPF().validate(cpf):
            return cpf
        else:
            raise ValueError('O CPF informado é inválido.')


    @validator('pis')
    def pis_valid(cls, pis):
        if PIS().validate(pis):
            return pis
        else:
            raise ValueError('O PIS informado é inválido.')
