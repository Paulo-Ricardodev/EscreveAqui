from flask import Blueprint, render_template, request, redirect
from models import Colecao, Repertorio
from utils import db
from flask_login import current_user, login_required


bp_colecoes = Blueprint('colecoes', __name__ , template_folder='templates')

@bp_colecoes.route('/criar/<int:id>', methods = ['GET','POST'])
def colecao_cadastro(id):
  repertorio = Repertorio.query.get(id)

  if request.method == "GET":
    
    return render_template('colecao_cadastro.html', repertorio = repertorio)

  if request.method == "POST":


    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    tipo = request.form.get('tipo')

    repertorio = Repertorio.query.get(id)


    colecao = Colecao(nome, descricao, tipo)
    colecao.usuario = current_user

    repertorio.colecao.append(colecao)

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



@bp_colecoes.route('/minhascolecoes', methods = ['GET', 'POST'])
@login_required
def minhascolecoes():
  return render_template('minhascolecoes.html')
    
    