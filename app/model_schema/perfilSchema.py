from typing import Optional
from pydantic import BaseModel, validator, constr
from validate_docbr import CPF, PIS
from app import fieldsFormatter, Perfil
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


    @validator('cpf')
    def cpf_validator(cls, cpf):
        if CPF().validate(cpf):

            cpf = fieldsFormatter.PisFormatter().clean(cpf)

            perfil = Perfil.query.filter_by(cpf=cpf).first()

            if perfil is not None:
                raise ValueError('O CPF informado já está cadastrado.')
            return cpf
        else:
            raise ValueError('O CPF informado é inválido.')

    @validator('pis')
    def pis_validator(cls, pis):
        if PIS().validate(pis):
            pis = fieldsFormatter.PisFormatter().clean(pis)

            perfil = Perfil.query.filter_by(pis=pis).first()

            if perfil is not None:
                raise ValueError('O PIS informado já está cadastrado.')
            return pis
        else:
            raise ValueError('O PIS informado é inválido.')
