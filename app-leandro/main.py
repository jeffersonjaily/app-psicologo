from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet
import re
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or "uma-chave-muito-secreta"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

DATABASE = "app_leandro.db"
KEY_FILE = 'chave.key'

if os.path.exists(KEY_FILE):
    with open(KEY_FILE, 'rb') as f:
        CHAVE_CIFRAGEM = f.read()
else:
    CHAVE_CIFRAGEM = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as f:
        f.write(CHAVE_CIFRAGEM)

cipher_suite = Fernet(CHAVE_CIFRAGEM)

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def criar_tabelas():
    conn = get_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL,
            tipo TEXT NOT NULL CHECK (tipo IN ('paciente', 'psicologo'))
        )''')
    c.execute('''CREATE TABLE IF NOT EXISTS mensagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL,
            mensagem TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
        )''')
    conn.commit()
    conn.close()

class User(UserMixin):
    def __init__(self, id_, nome, email, tipo):
        self.id = id_
        self.nome = nome
        self.email = email
        self.tipo = tipo

@login_manager.user_loader
def load_user(user_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    if user:
        return User(user["id"], user["nome"], user["email"], user["tipo"])
    return None

def validar_email(email):
    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return re.match(regex, email)

def criptografar(texto):
    return cipher_suite.encrypt(texto.encode()).decode()

def descriptografar(texto_criptografado):
    return cipher_suite.decrypt(texto_criptografado.encode()).decode()

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('area_privada'))
    return render_template('index.html')

@app.route('/area-paciente')
@login_required
def area_paciente():
    # Se quiser restringir acesso só para pacientes:
    if current_user.tipo != 'paciente':
        flash("Acesso negado.", "danger")
        return redirect(url_for('index'))
    return render_template('area-Paciente.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        usuario = c.fetchone()
        conn.close()

        if usuario and check_password_hash(usuario["senha_hash"], senha):
            user_obj = User(usuario["id"], usuario["nome"], usuario["email"], usuario["tipo"])
            login_user(user_obj)
            flash(f"Bem-vindo {usuario['nome']}!", "success")
            return redirect(url_for('area_privada'))
        else:
            flash("Email ou senha incorretos.", "danger")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        tipo = request.form.get('tipo')

        if not nome or not email or not senha or not tipo:
            flash("Preencha todos os campos!", "danger")
            return redirect(url_for('cadastro'))

        if not validar_email(email):
            flash("Email inválido!", "danger")
            return redirect(url_for('cadastro'))

        senha_hash = generate_password_hash(senha)

        try:
            conn = get_db()
            c = conn.cursor()
            c.execute("INSERT INTO usuarios (nome, email, senha_hash, tipo) VALUES (?, ?, ?, ?)",
                      (nome, email, senha_hash, tipo))
            conn.commit()
            conn.close()
            flash("Cadastro realizado com sucesso. Faça login.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Email já cadastrado.", "danger")
            return redirect(url_for('cadastro'))

    return render_template('cadastro.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Você saiu.", "info")
    return redirect(url_for('login'))

@app.route('/area_privada')
@login_required
def area_privada():
    return render_template('area_privada.html', nome=current_user.nome, tipo=current_user.tipo)

@app.route('/enviar_mensagem', methods=['POST'])
@login_required
def enviar_mensagem():
    texto = request.form.get('mensagem')
    if texto:
        texto_cripto = criptografar(texto)
        conn = get_db()
        c = conn.cursor()
        c.execute("INSERT INTO mensagens (id_usuario, mensagem) VALUES (?, ?)", (current_user.id, texto_cripto))
        conn.commit()
        conn.close()
        flash("Mensagem enviada!", "success")
    return redirect(url_for('area_privada'))

@app.route('/minhas_mensagens')
@login_required
def minhas_mensagens():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM mensagens WHERE id_usuario = ? ORDER BY timestamp DESC", (current_user.id,))
    mensagens = c.fetchall()
    conn.close()

    mensagens_decodificadas = []
    for msg in mensagens:
        try:
            texto = descriptografar(msg["mensagem"])
        except Exception:
            texto = "[Erro ao descriptografar]"
        mensagens_decodificadas.append({
            "id": msg["id"],
            "texto": texto,
            "timestamp": msg["timestamp"]
        })

    return render_template('minhas_mensagens.html', mensagens=mensagens_decodificadas)

if __name__ == '__main__':
    criar_tabelas()
    app.run(debug=True)
