from flask import Blueprint, render_template, request, redirect, url_for,flash
from models import Repertorio, Tema
from utils import db
from flask_login import current_user, login_required
from datetime import datetime
from functools import wraps


bp_repertorios = Blueprint('repertorios', __name__ , template_folder='templates')
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            # Se não for admin, redireciona para uma página de erro ou página inicial
            return redirect(url_for('repertorios.meusrepertorios'))  # Ou redirecionar para outra página
        return f(*args, **kwargs)
    return decorated_function

@bp_repertorios.route('/cadastro/<int:id>', methods = ['GET', 'POST'])
def repertorio_cadastro(id):
  
  if request.method == 'GET':
    
    return render_template('repertorio_cadastro.html', id=id)

  else:
    titulo = request.form.get('titulo')
    conteudo = request.form.get('conteudo')
    descricao = request.form.get('descricao')
    referencia = request.form.get('referencia')
    data = datetime.now()
    avaliacao = 2

    tema = Tema.query.get(id)

    repertorio = Repertorio(titulo, conteudo, descricao, referencia, data, avaliacao)
    repertorio.usuario = current_user
    
    tema.repertorio.append(repertorio)
    db.session.add(repertorio)
    db.session.commit()

    flash('Repertório cadastrado com sucesso!', 'success')  # Flash de sucesso
    return redirect(url_for('index')) 
    

@bp_repertorios.route("/gerenciar")
@login_required  # Garante que o usuário está logado
@admin_required  # Garante que o usuário tem o papel de admin
def gerenciar_repertorio():
  repertorio = Repertorio.query.all()
  return render_template('ger_repertorio.html', repertorio = repertorio)


@bp_repertorios.route("/update/<int:id>", methods = ['GET', 'POST'])
def repertorio_update(id):
  
  repertorio = Repertorio.query.get(id)
  
  if request.method == 'GET':
    
    return render_template('repertorio_update.html', repertorio = repertorio)

  else:
    titulo = request.form.get('titulo')
    conteudo = request.form.get('conteudo')
    descricao = request.form.get('descricao')
    referencia = request.form.get('referencia')

    repertorio.titulo = titulo
    repertorio.conteudo = conteudo
    repertorio.descricao = descricao
    repertorio.referencia = referencia

    db.session.add(repertorio)
    db.session.commit()
    if current_user.is_admin:
      return redirect(url_for("repertorios.gerenciar_repertorio"))
    else:
      return redirect(url_for("repertorios.meusrepertorios"))



@bp_repertorios.route('/delete/<int:id>', methods = ['GET', 'POST'])
def repertorio_delete(id):

  repertorio = Repertorio.query.get(id)
  
  if request.method == 'GET':
    return render_template('repertorio_delete.html', repertorio = repertorio)
  else:
    db.session.delete(repertorio)
    db.session.commit()
    
    if current_user.is_admin:
      return redirect(url_for("repertorios.gerenciar_repertorio"))
    else:
      return redirect(url_for("repertorios.meusrepertorios"))


@bp_repertorios.route('/abrir/<int:id>', methods = ['GET', 'POST'])
def repertorio_abrir(id):
  repertorio = Repertorio.query.get(id)
  return render_template('repertorio.html', repertorio = repertorio)


@bp_repertorios.route("/meusrepertorios", methods = ['GET'])
@login_required
def meusrepertorios():
  repertorio_usuario = Repertorio.query.filter_by(id_usuario=current_user.id).all()
  return render_template('meus_repertorios.html', repertorios=repertorio_usuario)

