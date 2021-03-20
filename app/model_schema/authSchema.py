from typing import Optional
import re
from pydantic import BaseModel, validator, constr
from app import Usuario, Perfil
from werkzeug.security import generate_password_hash
from flask_jwt_extended import get_jwt_identity
from app import fieldsFormatter, db, Messages
from sqlalchemy import or_

class AuthLoginSchema(BaseModel):

    email: constr(min_length=2, max_length=255)
    senha: constr(min_length=4, max_length=255)



# --------------------------------------------------------------------------------------------------#