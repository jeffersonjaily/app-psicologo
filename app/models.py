from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(80), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)
    tipo = db.Column(db.String(50))  # 'paciente' ou 'psicologo'

class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(80), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)
    nome = db.Column(db.String(100))
    proxima_sessao = db.Column(db.String(100))
    evolucao = db.Column(db.Text)
    metas = db.Column(db.Text)
