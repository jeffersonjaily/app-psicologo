from flask import render_template, Blueprint

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/paciente')
def area_paciente():
    return render_template('paciente.html')

@bp.route('/contato')
def contato():
    return render_template('contato.html')

@bp.route('/login')
def login():
    return render_template('login.html')

@bp.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')@bp.route('/')
def index():  # <- usado como 'main.index'
    return render_template('index.html')

@bp.route('/paciente')
def area_paciente():  # <- usado como 'main.area_paciente'
    return render_template('paciente.html')

@bp.route('/contato')
def contato():  # <- usado como 'main.contato'
    return render_template('contato.html')

@bp.route('/login')
def login():  # <- usado como 'main.login'
    return render_template('login.html')

@bp.route('/cadastro')
def cadastro():  # <- usado como 'main.cadastro'
    return render_template('cadastro.html')
