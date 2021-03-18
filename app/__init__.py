from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Server, Manager
from flask_migrate import Migrate, MigrateCommand
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object('config')

CORS(app)

jwt = JWTManager(app)

db  = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
server = Server(host="0.0.0.0", port=5000)
manager.add_command("runserver", server)
manager.add_command('db', MigrateCommand)

import Messages
from app.components import fieldsFormatter

from app.models.usuarioTable import Usuario
from app.models.controllerTable import Controller
from app.models.regraTable import Regra
from app.models.cargoTable import Cargo
from app.models.pessoaTable import Pessoa

from app.models.cidadeTable import Cidade
from app.models.estadoTable import Estado
from app.models.paisTable import Pais

from app.validators.modelValidator import ModelValidator
from app.validators.authValidator import AuthValidator
from app.validators.usuarioValidator import UsuarioValidator

from app.model_schema.usuarioSchema import UsuarioAddSchema, UsuarioEditSchema
from app.model_schema.pessoaSchema import PessoaAddSchema
from app.model_schema.authSchema import AuthLoginSchema
from app.model_schema.cadastroSchema import CadastroAddSchema

from app.controllers import usuarioController
from app.controllers import authController
from app.controllers import pessoaController
from app.controllers import cargoController
from app.controllers import cidadeController
from app.controllers import cadastroController

