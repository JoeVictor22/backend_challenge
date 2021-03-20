from app import db

class Perfil(db.Model):
    __tablename__ = "perfil"

    id = db.Column(db.BigInteger, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    pis = db.Column(db.String(50), unique=True, nullable=False)
    cpf = db.Column(db.String(50), unique=True, nullable=False)
    cep = db.Column(db.String(20), nullable=False)
    rua = db.Column(db.String(255), nullable=False)
    numero = db.Column(db.String(20), nullable=False)
    complemento = db.Column(db.String(50), nullable=True)

    cidade_id = db.Column(db.BigInteger, db.ForeignKey("cidade.id"), nullable=False)

    # --------------------------------------------------------------------------------------------------#

    def __init__(self, nome, pis, cpf, cep, rua, numero, complemento, cidade_id):
        self.nome = nome
        self.pis = pis
        self.cpf = cpf
        self.cep = cep
        self.rua = rua
        self.numero = numero
        self.complemento = complemento
        self.cidade_id = cidade_id

    # --------------------------------------------------------------------------------------------------#

    def __repr__(self):
        return "<Perfil %r %r %r %r %r %r %r %r %r>" %(self.id, self.nome, self.pis, self.cpf, self.cep, self.rua,
                                                       self.numero, self.complemento, self.cidade_id)
