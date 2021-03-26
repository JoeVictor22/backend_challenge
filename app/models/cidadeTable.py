from app import db

class Cidade(db.Model):
	__tablename__ = "cidade"

	id = db.Column(db.Integer, primary_key = True)
	nome = db.Column(db.String(255), nullable=False)
	ibge = db.Column(db.String(255), nullable=False, unique=True)

	estado_id = db.Column(db.Integer, db.ForeignKey('estado.id'), nullable=False)

	#--------------------------------------------------------------------------------------------------#

	def __init__(self, nome, ibge, estado_id):
		self.nome = nome
		self.ibge = ibge
		self.estado_id = estado_id

	#--------------------------------------------------------------------------------------------------#

	def __repr__(self):
		return "<Cidade %r %r %r %r >" %(self.id, self.nome, self.ibge, self.estado_id)
