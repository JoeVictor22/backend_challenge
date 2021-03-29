from app import db

class Cargo(db.Model):
    __tablename__ = "cargo"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), unique=True, nullable=False)

    usuarios = db.relationship("Usuario", backref="cargo", lazy=True)

    # --------------------------------------------------------------------------------------------------#

    def __init__(self, nome):
        self.nome = nome

    # --------------------------------------------------------------------------------------------------#

    def __repr__(self):
        return "<Cargo %r>" % self.nome