from flask import Flask, render_template, request, redirect
from utils import db, lm
from flask_migrate import Migrate
from controllers.usuarios import bp_usuarios
from controllers.repertorios import bp_repertorios
from controllers.temas import  bp_temas
from controllers.colecoes import bp_colecoes
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from models import Usuario
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ['MYSQL_PASSWORD']

conexao = 'mysql+pymysql://psi2023_paulo:bjIOQQQ3rH-9yOJA@albalopes.tech/psi2023_pi_escreveaqui'
app.config['SQLALCHEMY_DATABASE_URI'] = conexao

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(bp_usuarios, url_prefix = '/usuario')
app.register_blueprint(bp_repertorios, url_prefix = '/repertorio')
app.register_blueprint(bp_temas, url_prefix = '/tema')
app.register_blueprint(bp_colecoes, url_prefix = '/colecao')



db.init_app(app)
lm.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def index():
    return render_template('home.html')


  
@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

@app.route('/pesquisa')
def pesquisa():
  return render_template('pesquisa.html')


@app.errorhandler(401)
def acesso_negado(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.errorhandler(404)
def nao_encontrada(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=3000)
