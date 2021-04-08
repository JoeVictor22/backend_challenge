from app import db, fieldsFormatter

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

    def __init__(self, nome: str, pis: str, cpf: str, cep: str, rua: str, numero: str, complemento: str, cidade_id: int):
        self.nome = nome
        self.pis = pis
        self.cpf = cpf
        self.cep = cep
        self.rua = rua
        self.numero = numero
        self.complemento = complemento
        self.cidade_id = cidade_id

    # --------------------------------------------------------------------------------------------------#

    def to_dict(self):
        data = {
            "id": self.id,
            "nome": self.nome,
            "pis": fieldsFormatter.PisFormatter().format(self.pis),
            "cpf": fieldsFormatter.CpfFormatter().format(self.cpf),
            "cep": fieldsFormatter.CepFormatter().format(self.cep),
            "rua": self.rua,
            "numero": self.numero,
            "complemento": self.complemento,
            "cidade_id": self.cidade_id
            }
        return data

    # --------------------------------------------------------------------------------------------------#

    def __repr__(self):
        return "<Perfil %r %r %r %r %r %r %r %r %r>" %(self.id, self.nome, self.pis, self.cpf, self.cep, self.rua,
                                                       self.numero, self.complemento, self.cidade_id)
