import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

# Página responsiva com paleta petróleo e teal, servida via biblioteca padrão do Python.
PAGE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Hello World | Trilha Python • freeCodeCamp</title>
  <style>
    :root {
      --bg-deep: #07191d;
      --bg-petrol: #0d2b32;
      --surface: rgba(13, 43, 50, 0.86);
      --border: rgba(45, 212, 191, 0.24);
      --text-main: #ecfdf5;
      --text-muted: #99f6e4;
      --teal: #14b8a6;
      --teal-bright: #2dd4bf;
      --ink-dark: #042f2e;
    }

    * {
      box-sizing: border-box;
    }

    body {
      min-height: 100dvh;
      margin: 0;
      display: grid;
      place-items: center;
      padding: clamp(16px, 4vw, 40px);
      color: var(--text-main);
      background:
        radial-gradient(circle at top right, rgba(20, 184, 166, 0.18), transparent 45%),
        linear-gradient(145deg, var(--bg-deep), var(--bg-petrol));
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    .card {
      width: min(100%, 720px);
      padding: clamp(24px, 6vw, 52px);
      text-align: center;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: clamp(16px, 3vw, 28px);
      box-shadow: 0 24px 60px rgba(0, 0, 0, 0.42);
      backdrop-filter: blur(8px);
    }

    .badge {
      display: inline-block;
      padding: 6px 14px;
      border-radius: 999px;
      background: rgba(20, 184, 166, 0.14);
      border: 1px solid rgba(45, 212, 191, 0.35);
      color: var(--teal-bright);
      font-size: clamp(0.72rem, 1.8vw, 0.85rem);
      font-weight: 700;
      letter-spacing: 0.1em;
      text-transform: uppercase;
    }

    h1 {
      margin: clamp(14px, 3vw, 22px) 0 12px;
      font-size: clamp(2.1rem, 8vw, 4.2rem);
      line-height: 1.08;
      letter-spacing: -0.02em;
    }

    p {
      margin: 0 auto;
      max-width: 54ch;
      color: var(--text-muted);
      font-size: clamp(0.95rem, 2.4vw, 1.12rem);
      line-height: 1.65;
    }

    .actions {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: clamp(10px, 2.5vw, 16px);
      margin-top: clamp(24px, 5vw, 36px);
    }

    .btn {
      flex: 1 1 210px;
      max-width: 280px;
      padding: 13px 20px;
      border-radius: 12px;
      text-decoration: none;
      font-weight: 600;
      font-size: clamp(0.9rem, 2vw, 1rem);
      transition: transform 0.18s ease, background-color 0.18s ease, border-color 0.18s ease;
    }

    .btn:hover {
      transform: translateY(-2px);
    }

    .btn-primary {
      background: var(--teal-bright);
      color: var(--ink-dark);
    }

    .btn-primary:hover {
      background: #5eead4;
    }

    .btn-secondary {
      background: rgba(255, 255, 255, 0.04);
      color: var(--text-main);
      border: 1px solid rgba(153, 246, 228, 0.35);
    }

    .btn-secondary:hover {
      border-color: var(--teal-bright);
      background: rgba(20, 184, 166, 0.12);
    }
  </style>
</head>
<body>
  <main class="card">
    <span class="badge">freeCodeCamp &bull; Python</span>
    <h1>Hello, World!</h1>
    <p>
      Servidor local em Python puro com visual em tons de petróleo e teal, layout fluido
      e acesso rápido à documentação oficial e à trilha de estudos.
    </p>
    <nav class="actions" aria-label="Links de estudo">
      <a class="btn btn-primary" href="https://www.python.org/" target="_blank" rel="noopener noreferrer">
        Site oficial do Python
      </a>
      <a class="btn btn-secondary" href="https://www.freecodecamp.org/" target="_blank" rel="noopener noreferrer">
        freeCodeCamp
      </a>
    </nav>
  </main>
</body>
</html>
"""


class HelloWorldHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            content = PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Mantém o terminal limpo, exibindo apenas o aviso inicial e encerramento.
        return


if __name__ == "__main__":
    address = ("localhost", 8000)
    url = f"http://{address[0]}:{address[1]}"
    server = HTTPServer(address, HelloWorldHandler)
    print(f"Servidor iniciado em {url} (pressione Ctrl+C para encerrar)")
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
        server.server_close()
