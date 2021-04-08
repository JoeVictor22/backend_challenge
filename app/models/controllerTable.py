from app import db

class Controller(db.Model):
    __tablename__ = "controller"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), unique=True, nullable=False)

    regras = db.relationship("Regra", backref="controller", lazy=True)

    # --------------------------------------------------------------------------------------------------#

    def __init__(self, nome: str):
        self.nome = nome

    # --------------------------------------------------------------------------------------------------#

    def __repr__(self):
        return "<Controller %r>" % self.nome