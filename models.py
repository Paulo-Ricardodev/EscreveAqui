from utils import db, lm
from flask_login import  UserMixin
from datetime import datetime


Tem_reper = db.Table('Tema_repertorio',
                    db.Column('tema_id', db.Integer, db.ForeignKey('tema.id')),
                    db.Column('repertorio_id', db.Integer, db.ForeignKey('repertorio.id'))
                    )
Colecao_reper = db.Table('Colecao_repertorio',
                    db.Column('colecao_id', db.Integer, db.ForeignKey('colecao.id')),
                    db.Column('repertorio_id', db.Integer, db.ForeignKey('repertorio.id'))
                    )

class Usuario(UserMixin, db.Model):

  __tablename__= "usuario"
  id = db.Column(db.Integer, primary_key = True)
  nome = db.Column(db.String(80), nullable=True)
  email = db.Column(db.String(100), nullable=True)
  senha = db.Column(db.String(100), nullable=True)
  pontuacao = db.Column(db.Integer, nullable=True)
  admin = db.Column(db.Boolean)

  def __init__(self, nome, email, senha, pontuacao, admin):
    
    self.nome = nome
    self.email = email
    self.senha = senha
    self.pontuacao = pontuacao
    self.admin = admin
    

  def __repr__(self):
    return 'olá, {}!'.format(self.nome)


class Repertorio(db.Model):
  __tablename__= "repertorio"
  id = db.Column(db.Integer, primary_key = True)
  titulo = db.Column(db.String(80), nullable=True)
  conteudo = db.Column(db.String(10000), nullable = True)
  descricao = db.Column(db.String(200), nullable=True)
  referencia = db.Column(db.String(120), nullable=True, default=False)
  tipo = db.Column(db.String(80), nullable=True)
  data = db.Column(db.DateTime, default=datetime.now())
  avaliacao = db.Column(db.Integer, nullable=True)
  id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
  #temas = db.relationship('Tema', secondary='tema_repertorio', backref=db.backref('repertorios', lazy='dynamic'))
  
  usuario = db.relationship('Usuario', foreign_keys = id_usuario)
  colecao = db.relationship('Colecao', secondary=Colecao_reper, backref='repertorios')

  def __init__(self, titulo, conteudo, descricao, referencia, tipo, data, avaliacao ):
    self.titulo = titulo
    self.conteudo = conteudo  
    self.descricao = descricao
    self.referencia = referencia
    self.tipo = tipo
    self.data = data
    self.avaliacao = avaliacao


  def __repr__(self):
    return '{}'.format(self.titulo)

class Tema(db.Model):
  __tablename__= "tema"
  id = db.Column(db.Integer, primary_key = True)
  titulo = db.Column(db.String(80), nullable=True)
  descricao = db.Column(db.String(120), nullable=True)
  id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))

  usuario = db.relationship('Usuario', foreign_keys = id_usuario)

  repertorio = db.relationship('Repertorio', secondary=Tem_reper, backref='temas')

  def __init__(self, titulo, descricao):
    self.titulo = titulo
    self.descricao = descricao

  def __repr__(self):
    return 'tema: {}'.format(self.titulo)

class Colecao(db.Model):
  __tablename__ = "colecao"
  id = db.Column(db.Integer, primary_key = True)
  id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
  nome = db.Column(db.String(80), nullable=True)
  descricao = db.Column(db.String(120), nullable=True)
  tipo = db.Column(db.String(80), nullable=True)

  usuario = db.relationship('Usuario', foreign_keys = id_usuario)
 

  def __init__(self, nome, descricao, tipo):
    self.nome = nome
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
  #id = db.Column(db.Integer, primary_key = True)
  tema_id = db.Column(db.Integer, db.ForeignKey('tema.id'), primary_key=True)
  repertorio_id = db.Column(db.Integer, db.ForeignKey('repertorio.id'), primary_key=True)

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
  
  