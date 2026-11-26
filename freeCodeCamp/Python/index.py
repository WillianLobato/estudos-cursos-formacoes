from http.server import BaseHTTPRequestHandler, HTTPServer

# Página responsiva servida diretamente pelo Python, sem pacotes externos.
PAGE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Hello World | Minha trilha Python</title>
  <style>
    * { box-sizing: border-box; }
    body {
      min-height: 100vh;
      margin: 0;
      display: grid;
      place-items: center;
      padding: 24px;
      color: #f8fafc;
      background: linear-gradient(135deg, #101827, #253b5b);
      font-family: system-ui, sans-serif;
    }
    main {
      width: min(100%, 680px);
      padding: clamp(28px, 7vw, 56px);
      text-align: center;
      background: #ffffff12;
      border: 1px solid #ffffff25;
      border-radius: 24px;
      box-shadow: 0 24px 70px #0005;
    }
    .tag {
      color: #93c5fd;
      font-size: .85rem;
      font-weight: 700;
      letter-spacing: .12em;
      text-transform: uppercase;
    }
    h1 { margin: 16px 0; font-size: clamp(2.5rem, 9vw, 4.5rem); }
    p { color: #d1d9e6; line-height: 1.7; }
    nav {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 14px;
      margin-top: 32px;
    }
    a {
      padding: 13px 20px;
      color: #102033;
      background: #facc15;
      border-radius: 12px;
      font-weight: 700;
      text-decoration: none;
      transition: transform .2s, background .2s;
    }
    a:hover { transform: translateY(-3px); background: #fde047; }
    a:focus-visible { outline: 3px solid white; outline-offset: 4px; }
    a.secondary { color: #f8fafc; background: #ffffff20; }
    a.secondary:hover { background: #ffffff35; }
  </style>
</head>
<body>
  <main>
    <div class="tag">Minha trilha Python · freeCodeCamp</div>
    <h1>Hello World! 🐍</h1>
    <p>Meu primeiro passo na jornada Python: aprendendo, praticando e construindo
       novos projetos com a comunidade freeCodeCamp.</p>
    <nav aria-label="Links de aprendizagem">
      <a href="https://www.python.org/" target="_blank" rel="noopener noreferrer">
        Site oficial do Python
      </a>
      <a class="secondary" href="https://www.freecodecamp.org/"
         target="_blank" rel="noopener noreferrer">
        freeCodeCamp
      </a>
    </nav>
  </main>
</body>
</html>
"""


class HelloWorldHandler(BaseHTTPRequestHandler):
    # Responde às solicitações do navegador com a página HTML.
    def do_GET(self):
        content = PAGE.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


if __name__ == "__main__":
    # Inicia o servidor apenas na máquina local e informa o endereço.
    address = ("localhost", 8000)
    print("Servidor iniciado em http://localhost:8000")
    HTTPServer(address, HelloWorldHandler).serve_forever()
