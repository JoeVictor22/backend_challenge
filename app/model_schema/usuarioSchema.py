from typing import Optional
import re
from pydantic import BaseModel, validator, constr
from app import Usuario, Perfil
from flask_jwt_extended import jwt_required, get_jwt_identity

class UsuarioAddSchema(BaseModel):

    email: constr(min_length=5, max_length=255)
    senha: constr(min_length=6, max_length=255)
    cargo_id: int

    perfil_id: Optional[int]

    @validator('email')
    def email_validator(cls, email):
        email = email.lower()
        if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email) is None:
            raise ValueError('O email informado é invalido.')
        return email

    @validator('perfil_id')
    def perfil_validator(cls, perfil_id):
        perfil = Perfil.query.get(perfil_id)

        if perfil is None:
            raise ValueError('O cadastro informado não existe.')

        usuario = Usuario.query.filter(Usuario.perfil_id == perfil_id).first()

        if usuario is not None:
            raise ValueError('O cadastro pertence a outro usuário.')

        return perfil_id

# --------------------------------------------------------------------------------------------------#
class UsuarioEditSchema(BaseModel):

    email: constr(min_length=5, max_length=255)
    senha: Optional[constr(min_length=6, max_length=255)]

    cargo_id: int

    perfil_id: Optional[int]

    @validator('email')
    def email_validator(cls, email):
        email = email.lower()
        if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email) is None:
            raise ValueError('O email informado é invalido.')
        return email


    @validator('perfil_id')
    def perfil_validator(cls, perfil_id):

        if perfil_id is None:
            return ""

        perfil = Perfil.query.get(perfil_id)

        if perfil is None:
            raise ValueError('O cadastro informado não existe.')

        current_user = get_jwt_identity()

        usuario = Usuario.query.filter(Usuario.perfil_id == perfil_id, Usuario.id != current_user).first()

        if usuario is not None:
            raise ValueError('O cadastro pertence a outro usuário.')

        return perfil_id


