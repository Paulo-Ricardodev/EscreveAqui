from utils import db, lm
from flask_login import  UserMixin

class Usuario(UserMixin, db.Model):
  __tablename__= "usuario"
  id = db.Column(db.Integer, primary_key = True)
  nome = db.Column(db.String(80), nullable=True)
  email = db.Column(db.String(100), nullable=True)
  senha = db.Column(db.String(100), nullable=True)

  def __init__(self, nome, email, senha):
    
    self.nome = nome
    self.email = email
    self.senha = senha

  def __repr__(self):
    return 'olá, {}!'.format(self.nome)



class Repertorio(db.Model):
  __tablename__= "repertorio"
  id = db.Column(db.Integer, primary_key = True)
  titulo = db.Column(db.String(80), nullable=True)
  descricao = db.Column(db.String(200), nullable=True)
  referencia = db.Column(db.String(120), nullable=True, default=False)
  id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))

  usuario = db.relationship('Usuario', foreign_keys = id_usuario)

  def __init__(self, titulo, descricao, referencia):
    self.titulo = titulo
    self.descricao = descricao
    self.referencia = referencia

  def __repr__(self):
    return '{}'.format(self.titulo)

class Tema(db.Model):
  __tablename__= "tema"
  id = db.Column(db.Integer, primary_key = True)
  titulo = db.Column(db.String(80), nullable=True)
  descricao = db.Column(db.String(120), nullable=True)
  id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))

  usuario = db.relationship('Usuario', foreign_keys = id_usuario)

  def __init__(self, titulo, descricao):
    self.titulo = titulo
    self.descricao = descricao

  def __repr__(self):
    return 'tema: {}'.format(self.titulo)

class Colecao(db.Model):
  __tablename__ = "colecao"
  id = db.Column(db.Integer, primary_key = True)
  id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
  repertorio_id = db.Column(db.Integer, db.ForeignKey('repertorio.id'))
  titulo = db.Column(db.String(80), nullable=True)
  descricao = db.Column(db.String(120), nullable=True)
  tipo = db.Column(db.String(80), nullable=True)

  usuario = db.relationship('Usuario', foreign_keys = id_usuario)
  repertorio = db.relationship('Repertorio', foreign_keys = repertorio_id)

  def __init__(self, usuario_id, repertorio_id, titulo, descricao, tipo):

    self.usuario_id = usuario_id
    self.repertorio_id = repertorio_id
    self.titulo = titulo
    self.descricao = descricao
    self.tipo = tipo

  def __repr__(self):

    return 'Olá, {}! a sua coleção tem esses repertórios: {}'.format(self.usuario.nome, self.repertorio.titulo)
  
class Tipo_repertorio(db.Model):
  __tablename__ = 'tipo_repertorio'
  id = db.Column(db.Integer, primary_key = True)
  repertorio_id = db.Column(db.Integer, db.ForeignKey('repertorio.id'))
  pontuacao = db.Column(db.Integer, nullable = True)
  descricao = db.Column(db.String(200), nullable = True)

  repertorio = db.relationship('Repertorio', foreign_keys = repertorio_id)

  def __init__(self, repertorio_id, pontuacao, descricao):
    self.repertorio_id = repertorio_id
    self.pontuacao = pontuacao
    self.descricao = descricao

class Tema_repertorio(db.Model):
  __tablename__ = 'tema_repertorio'
  id = db.Column(db.Integer, primary_key = True)
  tema_id = db.Column(db.Integer, db.ForeignKey('tema.id'))
  repertorio_id = db.Column(db.Integer, db.ForeignKey('repertorio.id'))

  repertorio = db.relationship('Repertorio', foreign_keys = repertorio_id)
  tema = db.relationship('Tema', foreign_keys = tema_id)

  def __init__(self, tema_id, repertorio_id):
    self.tema_id = tema_id
    self.repertorio_id = repertorio_id

class Comentario(db.Model):
  __tablename__ = 'comentario'
  id = db.Column(db.Integer, primary_key = True)
  usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
  repertorio_id = db.Column(db.Integer, db.ForeignKey('repertorio.id'))
  pontuacao = db.Column(db.Integer)
   
  usuario = db.relationship('Usuario', foreign_keys = usuario_id)
  repertorio = db.relationship('Repertorio', foreign_keys = repertorio_id)
  
  