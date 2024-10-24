from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Tema, Repertorio, Tema_repertorio
from utils import db
from flask_login import current_user, login_required

bp_temas = Blueprint('temas', __name__ , template_folder='templates')




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
    
      

@bp_temas.route("/recovery")
def tema_recovery():
  tema = Tema.query.all()
  return render_template('tema_recovery.html', tema = tema)


@bp_temas.route('/pesquisa', methods = ['GET'])
def pesquisa():
  tema = Tema.query.all()
  return render_template('pesquisa.html', tema = tema)


@bp_temas.route("/update/<int:id>", methods = ['GET', 'POST'])
def tema_update(id):
  
  tema = Tema.query.get(id)
  
  if request.method == 'GET':
    
    return render_template('tema_update.html', tema = tema)

  else:
    titulo = request.form.get('titulo')
    descricao = request.form.get('descricao')

    tema.titulo = titulo
    tema.descricao = descricao


    db.session.add(tema)
    db.session.commit()
    return redirect('/tema/recovery')


@bp_temas.route("/delete/<int:id>", methods = ['GET', 'POST'])
def tema_delete(id):
  
  tema = Tema.query.get(id)

  if request.method == 'GET':
    return render_template('tema_delete.html', tema = tema)

  else:
    
    db.session.delete(tema)
    db.session.commit()

    return 'tema deletado'
  
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

