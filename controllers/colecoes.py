from flask import Blueprint, render_template, request, redirect
from models import Colecao
from utils import db

bp_colecoes = Blueprint('colecoes', __name__ , template_folder='templates')

@bp_colecoes.route('/criar', methods = ['GET','POST'])
def colecao_cadastro():
  if request.method == "GET":
    
    return render_template('colecao_cadastro.html')

  if request.method == "POST":

    usuario_id = request.form.get('usuario_id')
    repertorio_id = request.form.get('repertorio_id')
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')


    colecao = Colecao(usuario_id, repertorio_id, nome, descricao)

    db.session.add(colecao)
    db.session.commit()

    return 'colecao criada'

@bp_colecoes.route('/recovery')
def colecao_recovery():
  colecao = Colecao.query.all()

  return render_template('colecao_recovery.html', colecao = colecao)

@bp_colecoes.route('/update/<int:id>', methods = ['GET', 'POST'])
def colecao_update(id):
  
  colecao = Colecao.query.get(id)

  if request.method == 'GET':
    return render_template('colecao_update.html', colecao = colecao)

  else:
    
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    tipo = request.form.get('tipo')

    colecao.nome = nome
    colecao.descricao = descricao
    colecao.tipo = tipo

    db.session.add(colecao)
    db.session.commit()

    return 'coleção atualizada'

@bp_colecoes.route('/delete/<int:id>', methods = ['GET', 'POST'])
def colecao_delete(id):

  colecao = Colecao.query.get(id)
  
  if request.method == 'GET':
    return render_template('colecao_delete.html', colecao = colecao)

  else:

    db.session.delete(colecao)
    db.session.commit()
    return 'coleção deletada'

    
    