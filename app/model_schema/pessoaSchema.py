from typing import Optional
import re
from pydantic import BaseModel, validator, constr
from app import Usuario

class PessoaSchema(BaseModel):
    # mandatory field
    email: constr(min_length=5, max_length=255)
    senha: constr(min_length=6, max_length=255)
    cargo_id: int

    # optional denotes the field is optional
    pessoa_id: Optional[int]

    # custom validation on email field
    @validator('email')
    def email_valid(cls, v):
        email = v.lower()
        if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email) is None:
            raise ValueError('email provided is not valid')
        if Usuario.query.filter_by(email=email).first():
            raise ValueError('email already registered')
        return email