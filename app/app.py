<!-- login.html -->
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <title>Login</title>
</head>
<body>
  <h2>Login</h2>
  <form onsubmit="return login()">
    <input type="text" id="usuario" placeholder="Usuário" required />
    <input type="password" id="senha" placeholder="Senha" required />
    <button type="submit">Entrar</button>
  </form>
  <p id="erro" style="color:red; display:none;">Usuário ou senha inválidos.</p>

  <script>
    // Simulação de banco de dados local (em memória)
    const usuarios = [
      { usuario: "paciente1", senha: "1234", tipo: "paciente" },
      { usuario: "psicologo2", senha: "1234", tipo: "psicologo" }
    ];

    function login() {
      const user = document.getElementById('usuario').value.trim();
      const pass = document.getElementById('senha').value;

      const encontrado = usuarios.find(u => u.usuario === user && u.senha === pass);
      if (encontrado) {
        // Armazenar sessão simulada no localStorage
        localStorage.setItem("usuario_logado", user);
        window.location.href = "painel-paciente.html";
      } else {
        document.getElementById("erro").style.display = "block";
      }
      return false;
    }
  </script>
</body>
</html>
