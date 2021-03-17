from typing import Optional
import re
from pydantic import BaseModel, validator, constr
from app import Usuario, Pessoa
from werkzeug.security import generate_password_hash
from flask_jwt_extended import get_jwt_identity

class UsuarioAddSchema(BaseModel):

    email: constr(min_length=5, max_length=255)
    senha: constr(min_length=6, max_length=255)
    cargo_id: int

    pessoa_id: Optional[int]

    # todo, validate cpf and pis duplicate
    @validator('email')
    def email_valid(cls, v):

        # todo validate user
        current_user = get_jwt_identity()
        usuario_logado = Usuario.query.get(current_user)
        print(usuario_logado.email)


        email = v.lower()
        if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email) is None:
            raise ValueError('O email informado é invalido.')
        if Usuario.query.filter_by(email=email).first():
            raise ValueError('O email informado já está cadastrado.')
        return email


    @validator('pessoa_id')
    def pessoa_validator(cls, pessoa_id):
        pessoa = Pessoa.query.get(pessoa_id)

        if pessoa is None:
            raise ValueError('O cadastro informado não existe.')

        usuario = Usuario.query.filter(Usuario.pessoa_id == pessoa_id)

        if usuario is None:
            raise ValueError('O cadastro pertence a outro usuário.')

# --------------------------------------------------------------------------------------------------#
class UsuarioEditSchema(BaseModel):

    email: constr(min_length=5, max_length=255)
    cargo_id: int

    pessoa_id: Optional[int]

    # todo, validate cpf and pis duplicate
    @validator('email')
    def email_valid(cls, v):
        email = v.lower()
        if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email) is None:
            raise ValueError('O email informado é invalido.')
        if Usuario.query.filter_by(email=email).first():
            raise ValueError('O email informado já está cadastrado.')
        return email


    @validator('pessoa_id')
    def pessoa_validator(cls, pessoa_id):
        pessoa = Pessoa.query.get(pessoa_id)

        if pessoa is None:
            raise ValueError('O cadastro informado não existe.')

        usuario = Usuario.query.filter(Usuario.pessoa_id == pessoa_id)

        if usuario is None:
            raise ValueError('O cadastro pertence a outro usuário.')

