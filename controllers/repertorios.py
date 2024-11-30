from flask import Blueprint, render_template, request, redirect, url_for,flash
from models import Repertorio, Tema
from utils import db
from flask_login import current_user, login_required
from datetime import datetime


bp_repertorios = Blueprint('repertorios', __name__ , template_folder='templates')

@bp_repertorios.route('/cadastro/<int:id>', methods = ['GET', 'POST'])
def repertorio_cadastro(id):
  
  if request.method == 'GET':
    
    return render_template('repertorio_cadastro.html', id=id)

  else:
    titulo = request.form.get('titulo')
    conteudo = request.form.get('conteudo')
    descricao = request.form.get('descricao')
    referencia = request.form.get('referencia')
    tipo = request.form.get('tipo_repertorio')
    data = datetime.now()
    avaliacao = 2

    tema = Tema.query.get(id)

    repertorio = Repertorio(titulo, conteudo, descricao, referencia, tipo, data, avaliacao)
    repertorio.usuario = current_user
    
    tema.repertorio.append(repertorio)
    db.session.add(repertorio)
    db.session.commit()

    flash('Repertório cadastrado com sucesso!', 'success')  # Flash de sucesso
    return redirect(url_for('index')) 
    

@bp_repertorios.route("/recovery")
def repertorio_recovery():
  repertorio = Repertorio.query.all()
  return render_template('repertorio_recovery.html', repertorio = repertorio)


@bp_repertorios.route("/update/<int:id>", methods = ['GET', 'POST'])
def repertorio_update(id):
  
  repertorio = Repertorio.query.get(id)
  
  if request.method == 'GET':
    
    return render_template('repertorio_update.html', repertorio = repertorio)

  else:
    titulo = request.form.get('titulo')
    descricao = request.form.get('descricao')
    referencia = request.form.get('referencia')

    repertorio.titulo = titulo
    repertorio.descricao = descricao
    repertorio.referencia = referencia

    db.session.add(repertorio)
    db.session.commit()
    return 'repertorio atualizado'



@bp_repertorios.route('/delete/<int:id>', methods = ['GET', 'POST'])
def repertorio_delete(id):

  repertorio = Repertorio.query.get(id)
  
  if request.method == 'GET':
    return render_template('repertorio_delete.html', repertorio = repertorio)
  else:
    db.session.delete(repertorio)
    db.session.commit()

    return 'dados deletados'

@bp_repertorios.route('/abrir/<int:id>', methods = ['GET', 'POST'])
def repertorio_abrir(id):
  repertorio = Repertorio.query.get(id)
  return render_template('repertorio.html', repertorio = repertorio)




@bp_repertorios.route("/meusrepertorios", methods = ['GET'])
@login_required
def meusrepertorios():
  repertorio_usuario = Repertorio.query.filter_by(id_usuario=current_user.id).all()
  return render_template('meus_repertorios.html', repertorios=repertorio_usuario)