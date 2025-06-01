from flask import Flask, Blueprint, render_template, request, redirect, session, url_for, flash
from models import db, Usuario, Paciente

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SECRET_KEY'] = 'segredo'
db.init_app(app)

main_routes = Blueprint('main', __name__)

# Rota raiz redireciona para login
@main_routes.route('/')
def index():
    return redirect(url_for('main.login'))

# Rota de login
@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']

        user = Usuario.query.filter_by(usuario=usuario, senha=senha).first()
        if user:
            session['usuario'] = usuario
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('main.painel'))
        else:
            flash('Usuário ou senha inválidos.', 'danger')
            return render_template('login.html')

    return render_template('login.html')

# Rota de logout (corrigida)
@main_routes.route('/logout', methods=['POST'])
def logout():
    session.pop('usuario', None)
    flash('Você saiu com sucesso.', 'info')
    return redirect(url_for('main.login'))

# Rota de cadastro
@main_routes.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']

        # Verifica se usuário já existe
        if Usuario.query.filter_by(usuario=usuario).first():
            flash('Usuário já existe. Escolha outro nome.', 'danger')
            return redirect(url_for('main.cadastrar'))

        novo_usuario = Usuario(usuario=usuario, senha=senha, tipo='paciente')
        db.session.add(novo_usuario)
        db.session.commit()

        flash('Cadastro realizado com sucesso! Faça login.', 'success')
        return redirect(url_for('main.login'))

    return render_template('cadastrar.html')

# Painel do paciente
@main_routes.route('/painel')
def painel():
    if 'usuario' not in session:
        flash('Você precisa estar logado para acessar o painel.', 'warning')
        return redirect(url_for('main.login'))

    usuario = session['usuario']

    # Dados simulados (exemplo)
    dados = {
        'proxima_sessao': '15/06/2025 às 14h00',
        'evolucao': [
            'Sentiu-se mais disposto',
            'Aplicou técnica de respiração',
            'Diminuição da ansiedade relatada'
        ],
        'metas': [
            'Meditar 10 minutos por dia',
            'Evitar redes sociais após as 21h'
        ]
    }

    return render_template('painel-paciente.html', usuario=usuario, dados=dados)

# Registro das rotas
app.register_blueprint(main_routes)

# Execução principal
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Criação de usuários de teste
        if not Usuario.query.filter_by(usuario='paciente1').first():
            novo = Usuario(usuario='paciente1', senha='1234', tipo='paciente')
            db.session.add(novo)
            db.session.commit()

        if not Usuario.query.filter_by(usuario='psicologo2').first():
            novo = Usuario(usuario='psicologo2', senha='1234', tipo='psicologo')
            db.session.add(novo)
            db.session.commit()

    app.run(debug=True)
