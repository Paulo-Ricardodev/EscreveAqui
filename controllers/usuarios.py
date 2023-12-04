from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import Usuario
from utils import db, lm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt



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

    # criptografando a senha com o bcrypt
    hashed_senha = bcrypt.generate_password_hash(senha).decode('utf-8')



    if senha == csenha:
      usuario = Usuario(nome,  email, hashed_senha, 0)
      db.session.add(usuario)
      db.session.commit()
      return redirect(url_for('index'))
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

    

  

@bp_usuarios.route("/recovery")
@login_required
def recovery():
  usuarios = Usuario.query.all()
  return render_template('usuarios_recovery.html', usuarios = usuarios)


@bp_usuarios.route('/update/<int:id>', methods = ['GET', 'POST'])
@login_required
def update(id):
  
  usuario = Usuario.query.get(id)
  
  if request.method == 'GET':
    
    return render_template("usuarios_update.html", usuario = usuario)
    
  if request.method == 'POST':
    
    nome = request.form.get('nome')
    email = request.form.get('email')
    
    usuario.nome = nome
    usuario.email = email
    
    db.session.add(usuario)
    db.session.commit()
    return redirect('/usuario/recovery')


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
    return 'Credenciais inválidas'

@bp_usuarios.route('/logoff')
def logoff():
  logout_user()
  return redirect('/')
