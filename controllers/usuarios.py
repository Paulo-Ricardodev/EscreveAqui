from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from models import Usuario, Repertorio, Tema
from utils import db, lm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from sqlalchemy import func



bp_usuarios = Blueprint('usuarios', __name__ , template_folder='templates')
bcrypt = Bcrypt()


@bp_usuarios.route('/cadastro', methods = ['GET', 'POST'])
def cadastro_usuario():
  if request.method == 'GET':
    return render_template('cadastro_usuario.html')
  else:
    
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    csenha = request.form.get('csenha')
    pontuacao = 0
    admin = "False"

    # criptografando a senha com o bcrypt
    hashed_senha = bcrypt.generate_password_hash(senha).decode('utf-8')



    if senha == csenha:
      usuario = Usuario(nome,  email, hashed_senha, pontuacao, eval(admin))
      db.session.add(usuario)
      db.session.commit()
      return redirect(url_for('usuarios.login'))
    else:
      return 'As senhas não coincidem'


@bp_usuarios.route('/login', methods = ['GET', 'POST'])
def login():
  if request.method == 'GET':
    
    return render_template('login.html')
  
  if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and bcrypt.check_password_hash(usuario.senha, senha):
          
            # Senha válida, redirecione para a página inicial ou área restrita
            flash('Login bem-sucedido!', 'success')
          
            return 'login concluído'
        else:
          
            return jsonify({"message": "Credenciais inválidas"}), 401

def pontuacao():
  quant_repertorio = int(repertorios_usuario(id))
  for i in quant_repertorio:
     Usuario.pontuacao += 40
     db.session.commit()
  
    
@bp_usuarios.route('/perfil')
def perfil():
    id = current_user.id
    quant_repertorio = int(repertorios_usuario(id))
    quant_tema = int(temas_usuario(id))
    pontuacao = 0

    for i in range(quant_repertorio):
     pontuacao += 40
    for i in range(quant_tema):
       pontuacao = pontuacao - 100

    usuario = Usuario.query.get(id)
    usuario.pontuacao = pontuacao
    db.session.add(usuario)
    db.session.commit()


    if current_user.is_authenticated:
        return render_template('perfil.html', quant_repertorio = quant_repertorio, quant_tema = quant_tema)
    else:
        return redirect('/usuario/login')


@bp_usuarios.route("/recovery")
@login_required
def recovery():


  if not current_user.admin:
    flash("Acesso não permitido")
    return redirect('/login')
  else:
    usuarios = Usuario.query.all()
    return render_template('usuarios_recovery.html', usuarios = usuarios)

@bp_usuarios.route('/gerenciar/<int:id>', methods = ['GET', 'POST'])
@login_required
def gerenciar(id):

  if not current_user.admin:
    flash("Acesso não permitido")
    return redirect('/login')
  else:
  
    usuario = Usuario.query.get(id)
    
    if request.method == 'GET':
      
      return render_template("usuarios_update.html", usuario = usuario)
      
    if request.method == 'POST':
      
      nome = request.form.get('nome')
      email = request.form.get('email')
      admin = request.form.get('admin')
      
      
      usuario.nome = nome
      usuario.email = email
      usuario.admin = eval(admin)
      
      
      db.session.add(usuario)
      db.session.commit()
      return redirect('/usuario/recovery')



@bp_usuarios.route('/update/<int:id>', methods = ['GET', 'POST'])
@login_required
def update(id):

    usuario = Usuario.query.get(id)
    
    if request.method == 'GET':
      
      return render_template("editar_perfil.html", usuario = usuario)
      
    if request.method == 'POST':
      
      nome = request.form.get('nome')
      email = request.form.get('email')
      admin = request.form.get('admin')
      
      
      usuario.nome = nome
      usuario.email = email
      usuario.admin = eval(admin)
      
      
      db.session.add(usuario)
      db.session.commit()
      return redirect('/usuario/update')


@bp_usuarios.route('/delete/<int:id>', methods = ['GET', 'POST'])
@login_required
def delete(id):

  usuario = Usuario.query.get(id)
  
  if request.method == 'GET':
    return render_template('usuario_delete.html', usuario = usuario)
  else:
    db.session.delete(usuario)
    db.session.commit()

    return 'dados deletados'

@lm.user_loader
def load_user(id):
  usuario = Usuario.query.filter_by(id=id).first()
  #usuario = Usuario.query.get(id)
  return usuario

@bp_usuarios.route('/autenticar', methods=['POST'])
def autenticar():
  email = request.form.get('email')
  senha = request.form.get('senha')
  usuario = Usuario.query.filter_by(email = email).first()

  if usuario and bcrypt.check_password_hash(usuario.senha, senha):
    login_user(usuario)
    return redirect(url_for('index'))
  else:
    flash('Credenciais inválidas. Tente novamente.', 'error') 
    return redirect(url_for('usuarios.login'))
  

@bp_usuarios.route('/editar_perfil/<int:id>')
def editar_perfil(id):

  usuario = Usuario.query.filter_by(id=id).first()


@bp_usuarios.route('/nova_senha')
def nova_senha():
  return ''

@bp_usuarios.route("/resultado/<int:id>")
def repertorios_usuario(id):
    quant_repertorio = db.session.query(func.count(Repertorio.id)).\
        filter(Repertorio.id_usuario == id).scalar()

    return quant_repertorio

def temas_usuario(id):
    quant_tema = db.session.query(func.count(Tema.id)).\
        filter(Tema.id_usuario == id).scalar()

    return quant_tema

@bp_usuarios.route('/logoff', methods=['POST'])
def logoff():
    logout_user()  # Usa o Flask-Login para deslogar o usuário
    return redirect(url_for('index'))  # Redireciona para a página inicial