# APP_LEANDRO

Aplicação web desenvolvida com Flask para gestão de pacientes e psicólogos.

## Estrutura do Projeto

APP_LEANDRO/
├── static/ # Arquivos estáticos (CSS, JS, imagens)
│ ├── css/
│ │ └── style.css # Estilos da aplicação
│ ├── imagens/ # Imagens utilizadas no site
│ └── js/
│ └── scripts.js # Scripts JavaScript
├── templates/ # Páginas HTML renderizadas pelo Flask
│ ├── agenda.html
│ ├── Área Paciente.html
│ ├── cadastro.html
│ ├── index.html
│ ├── login.html
│ ├── relatorios.html
│ └── Tela Inicial Psicologo.html
├── agenda.db # Banco de dados de agendamentos
├── database.db # Banco de dados principal
├── app.py # Arquivo principal da aplicação Flask
└── ngrok.exe # Utilitário para exposição local via túnel (usado em testes)