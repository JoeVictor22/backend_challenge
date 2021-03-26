from app import db

class Estado(db.Model):
	__tablename__ = "estado"

	id = db.Column(db.Integer, primary_key = True)
	nome = db.Column(db.String(255), nullable=False)
	sigla = db.Column(db.String(2), nullable=False, unique=True)
	pais_id = db.Column(db.Integer, db.ForeignKey('pais.id'), nullable=False)

	cidades = db.relationship('Cidade', backref='uf', lazy=True)

	#--------------------------------------------------------------------------------------------------#
	
	def __init__(self, nome, sigla):
		self.nome = nome
		self.sigla = sigla

	#--------------------------------------------------------------------------------------------------#
		
	def __repr__(self):
		return "<Estado %r %r %r>" %(self.id, self.nome, self.sigla)
