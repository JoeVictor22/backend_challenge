from app import db
from sqlalchemy.orm import validates


class Usuario(db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)

    perfil_id = db.Column(db.BigInteger, db.ForeignKey("perfil.id"), nullable=True)
    cargo_id = db.Column(db.Integer, db.ForeignKey("cargo.id"), nullable=False)

    # --------------------------------------------------------------------------------------------------#

    def __init__(self, email, senha, perfil_id, cargo_id):
        self.email = email
        self.senha = senha
        self.perfil_id = perfil_id
        self.cargo_id = cargo_id

    # --------------------------------------------------------------------------------------------------#

    def __repr__(self):
        return "<Usuario %r %r %r>" %(self.email, self.perfil_id, self.cargo_id)
