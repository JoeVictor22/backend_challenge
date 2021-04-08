from app import db

class Estado(db.Model):
	__tablename__ = "estado"

	id = db.Column(db.Integer, primary_key = True)
	nome = db.Column(db.String(255), nullable=False)
	sigla = db.Column(db.String(2), nullable=False, unique=True)
	pais_id = db.Column(db.Integer, db.ForeignKey('pais.id'), nullable=False)

	cidades = db.relationship('Cidade', backref='uf', lazy=True)

	#--------------------------------------------------------------------------------------------------#
	
	def __init__(self, nome: str, sigla: str, pais_id: int):
		self.nome = nome
		self.sigla = sigla
		self.pais_id = pais_id

	#--------------------------------------------------------------------------------------------------#
		
	def __repr__(self):
		return "<Estado %r %r %r %r>" %(self.id, self.nome, self.sigla, self.pais_id)
