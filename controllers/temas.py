from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Tema, Repertorio, Tema_repertorio
from utils import db
from flask_login import current_user, login_required
from functools import wraps

bp_temas = Blueprint('temas', __name__ , template_folder='templates')


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            # Se não for admin, redireciona para uma página de erro ou página inicial
            return redirect(url_for('temas.meustemas'))  # Ou redirecionar para outra página
        return f(*args, **kwargs)
    return decorated_function

@bp_temas.route("/cadastro", methods = ['GET', 'POST'])
def tema_cadastro():
  if request.method == 'GET':
    
    return render_template("tema_cadastro.html")
  

  else:
    
    titulo = request.form.get('titulo_tema')
    descricao = request.form.get('descricao')

    # Verifique se o usuário está autenticado
    if current_user.is_authenticated:
        # Se estiver autenticado, associe o usuário ao tema
        tema = Tema(titulo=titulo, descricao=descricao)
        tema.usuario = current_user

        db.session.add(tema)
        db.session.commit()

        flash('Tema cadastrado com sucesso!', 'success')  # Flash de sucesso
        return redirect(url_for('index')) 
    
    else:
      return current_user
    
      

@bp_temas.route("/gerenciar", methods = ['GET', 'POST'])
@login_required  # Garante que o usuário está logado
@admin_required  # Garante que o usuário tem o papel de admin
def gerenciar_tema():
  temas = Tema.query.all()
  return render_template('ger_temas.html', temas = temas)


@bp_temas.route('/pesquisa', methods = ['GET'])
def pesquisa():
  if current_user.is_authenticated:
    tema = Tema.query.all()
    return render_template('pesquisa.html', tema = tema)
  else:
    return redirect('/usuario/login')
  
  return render_template('pesquisa.html', tema = tema)


@bp_temas.route("/update/<int:id>", methods = ['GET', 'POST'])
def tema_update(id):
  
  tema = Tema.query.get(id)
  
  if request.method == 'GET':
    
    return render_template('tema_update.html', tema = tema)

  if request.method == "POST":
    titulo = request.form.get('titulo')
    descricao = request.form.get('descricao')

    tema.titulo = titulo
    tema.descricao = descricao


    db.session.add(tema)
    db.session.commit()
    if current_user.is_admin:
      return redirect(url_for("temas.gerenciar_tema"))
    else:
      return redirect(url_for("temas.meustemas"))


@bp_temas.route("/delete/<int:id>", methods = ['GET', 'POST'])
def tema_delete(id):
  
  tema = Tema.query.get(id)

  if request.method == 'GET':
    return render_template('tema_delete.html', tema = tema)

  else:
    
    db.session.delete(tema)
    db.session.commit()

    flash('Tema deletado com sucesso!', 'success') 
    if current_user.is_admin:
      return redirect(url_for("temas.gerenciar_tema"))
    else:
      return redirect(url_for("temas.meustemas"))

  
@bp_temas.route("/abrir/<int:id>", methods = ['GET', 'POST'])
def tema_abrir(id):


  tema = Tema.query.get(id)
  #repertorio = db.session.query(
  #    Repertorio,
  #    Tema,
  #).join(
  #    Tem_reper, Repertorio.id == Tem_reper.c.repertorio_id  # Junção com a tabela associativa
  #).join(
  #    Tema, Tem_reper.c.tema_id == tema.id  # Sem aspas em "tema"
  #).filter(
  #    Repertorio.id == id,
  #).all()

  '''repertorio = db.session.query(
      Repertorio,
      Tem_reper,
  ).join(
      Tem_reper, Repertorio.id == Tem_reper.c.repertorio_id  # Junção com a tabela associativa
  ).filter(
      Tem_reper.tema_id == id,
  ).all()
'''

  repertorio = db.session.query(Repertorio).join(Tema_repertorio).filter(Tema_repertorio.tema_id == id).all()
  print(repertorio)
  return render_template('repertorios_temas.html', tema = tema, repertorio = repertorio)


@bp_temas.route("/meustemas", methods=['GET'])
@login_required
def meustemas():
    temas_usuario = Tema.query.filter_by(id_usuario=current_user.id).all()

    return render_template('meustemas.html', temas=temas_usuario)