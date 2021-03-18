from typing import Optional
import re
from pydantic import BaseModel, validator, constr
from app import Usuario, Pessoa, fieldsFormatter

from validate_docbr import CPF, PIS

class CadastroAddSchema(BaseModel):

    email: constr(min_length=5, max_length=255)
    senha: constr(min_length=6, max_length=255)

    nome: constr(min_length=2, max_length=255)
    pis: constr(min_length=11, max_length=50)
    cpf: constr(min_length=11, max_length=50)
    cep: constr(min_length=2, max_length=20)
    rua: constr(min_length=3, max_length=255)
    numero: constr(min_length=1, max_length=20)
    complemento: Optional[constr(min_length=0, max_length=50)]

    cidade_id: int

    # todo, validate cpf and pis duplicate
    @validator('email')
    def email_valid(cls, email):

        email = email.lower()
        if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email) is None:
            raise ValueError('O email informado é invalido.')
        if Usuario.query.filter_by(email=email).first():
            raise ValueError('O email informado já está cadastrado.')
        return email

    @validator('cpf')
    def cpf_valid(cls, cpf):
        if CPF().validate(cpf):
            cpf = fieldsFormatter.PisFormatter().clean(cpf)
            if Pessoa.query.filter_by(cpf=cpf).first():
                raise ValueError('O CPF informado já está cadastrado.')
            return cpf
        else:
            raise ValueError('O CPF informado é inválido.')


    @validator('pis')
    def pis_valid(cls, pis):
        if PIS().validate(pis):
            pis = fieldsFormatter.PisFormatter().clean(pis)
            if Pessoa.query.filter_by(pis=pis).first():
                raise ValueError('O PIS informado já está cadastrado.')
            return pis
        else:
            raise ValueError('O PIS informado é inválido.')
