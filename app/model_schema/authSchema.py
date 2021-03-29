from pydantic import BaseModel, validator, constr
import json


class AuthLoginSchema(BaseModel):

    email: constr(min_length=2, max_length=255)
    senha: constr(min_length=4, max_length=255)

    class Config:
        json_loads = json.loads

# --------------------------------------------------------------------------------------------------#