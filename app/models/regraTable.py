from app import db

class Regra(db.Model):
    __tablename__ = "regra"

    acao = db.Column(db.String(20), nullable=False, primary_key=True)
    cargo_id = db.Column(
        db.Integer, db.ForeignKey("cargo.id"), nullable=False, primary_key=True
    )
    controller_id = db.Column(
        db.Integer, db.ForeignKey("controller.id"), nullable=False, primary_key=True
    )

    permitir = db.Column(db.Boolean, nullable=False)


    # --------------------------------------------------------------------------------------------------#

    def __init__(self, acao, cargo_id, controller_id, permitir):
        self.acao = acao
        self.cargo_id = cargo_id
        self.controller_id = controller_id
        self.permitir = permitir

    # --------------------------------------------------------------------------------------------------#

    def __repr__(self):
        return "<Regra %r, %r, %r, %r>" % (self.acao, self.cargo_id, self.controller_id, self.permitir)
