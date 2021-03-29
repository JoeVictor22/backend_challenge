from typing import Optional
import re
from pydantic import BaseModel, validator, constr
import ujson

class UsuarioAddSchema(BaseModel):

    email: constr(min_length=5, max_length=255)
    senha: constr(min_length=6, max_length=255)
    cargo_id: int

    perfil_id: Optional[int]

    class Config:
        json_loads = ujson.loads

    @validator('email')
    def email_validator(cls, email):
        email = email.lower()
        if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email) is None:
            raise ValueError('O email informado é invalido.')
        return email


# --------------------------------------------------------------------------------------------------#
class UsuarioEditSchema(BaseModel):

    email: constr(min_length=5, max_length=255)
    senha: Optional[constr(min_length=6, max_length=255)]

    cargo_id: int

    perfil_id: Optional[int]

    class Config:
        json_loads = ujson.loads

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

        return perfil_id


