from app import db

class Pais(db.Model):
    __tablename__ = "pais"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    iso = db.Column(db.String(5), nullable=False, unique=True)

    estados = db.relationship('Estado', backref='pais', lazy=True)

    # --------------------------------------------------------------------------------------------------#

    def __init__(self, nome: str, iso: str):
        self.nome = nome
        self.iso = iso

    # --------------------------------------------------------------------------------------------------#

    def __repr__(self):
        return "<Pais %r %r %r>" % (self.id, self.nome, self.iso)