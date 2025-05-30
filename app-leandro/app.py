from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/paciente/<int:paciente_id>")
def paciente(paciente_id):
    paciente = {
        "id": paciente_id,
        "nome": "João",
        "tipo_consulta": "Psicoterapia",
        "valor_sessao": 120,
        "valor_pendente": 240,
        "total_sessoes": 10,
        "comparecimentos": 8,
        "faltas": 2
    }
    return render_template("paciente.html", paciente=paciente)

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

# Inicializa o banco de dados e cria tabela users se não existir
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    # Abre a página index.html sempre que acessar a raiz /
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('index.html'))  # Corrigido para redirecionar para '/'
        else:
            flash("Usuário ou senha inválidos.")
    return render_template('home')


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            conn.close()
            flash("Cadastro realizado! Faça login.")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Nome de usuário já existe.")
    return render_template('cadastro.html')

@app.route('/agenda')
def agenda():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('agenda.html')

@app.route('/relatorios')
def relatorios():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('relatorios.html')

@app.route('/paciente')
def area_paciente():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('Área Paciente.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/paciente/<int:paciente_id>')
def area_paciente(paciente_id):
    paciente = get_paciente_por_id(paciente_id)
    return render_template('Área Paciente.html', paciente=paciente)

@app.route('/registrar_sessao/<int:paciente_id>', methods=['POST'])
def registrar_sessao(paciente_id):
    # atualiza total_sessoes e comparecimentos
    return redirect(url_for('area_paciente', paciente_id=paciente_id))

@app.route('/registrar_falta/<int:paciente_id>', methods=['POST'])
def registrar_falta(paciente_id):
    # atualiza total_sessoes e faltas
    return redirect(url_for('area_paciente', paciente_id=paciente_id))

@app.route('/registrar_pagamento/<int:paciente_id>', methods=['POST'])
def registrar_pagamento(paciente_id):
    # reduz valor_pendente
    return redirect(url_for('area_paciente', paciente_id=paciente_id))
