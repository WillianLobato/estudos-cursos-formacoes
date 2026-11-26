"""
app.py - Servidor local do "Painel & Calculadoras Financeiras".

Uso:  python app.py   (abre http://localhost:8000 no navegador)

Rotas:
  GET  /                     -> interface (index.html)
  GET  /api/indicadores      -> Selic e USD/BRL (com fallback seguro)
  POST /api/juros-compostos  -> calculos.juros_compostos
  POST /api/comparador       -> calculos.comparador_investimentos
  POST /api/financiamento    -> calculos.comparar_financiamentos
"""

import json
import math
import threading
import time
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import calculos

HOST, PORT = "127.0.0.1", 8000
PASTA = Path(__file__).resolve().parent
TIMEOUT = 5          # segundos por requisição externa
CACHE_SEGUNDOS = 60  # evita bater nas APIs a cada clique

# Valores usados SOMENTE se as APIs falharem (marcados como "referência").
FALLBACK = {"selic": 15.00, "usd_brl": 5.50}

_cache = {"ts": 0.0, "dados": None}


# ---------------------------------------------------------------------------
# Indicadores externos
# ---------------------------------------------------------------------------
def _buscar_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "painel-financeiro/1.0"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _selic():
    """Meta Selic (% a.a.) - série 432 do Banco Central (SGS)."""
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json"
    item = _buscar_json(url)[0]
    return float(item["valor"]), item["data"]


def _dolar():
    """Cotação USD/BRL (compra) - AwesomeAPI."""
    d = _buscar_json("https://economia.awesomeapi.com.br/json/last/USD-BRL")["USDBRL"]
    return float(d["bid"]), d.get("create_date", "")


def obter_indicadores():
    """Busca cada indicador de forma independente; se um falhar, usa fallback."""
    agora = time.time()
    if _cache["dados"] and agora - _cache["ts"] < CACHE_SEGUNDOS:
        return _cache["dados"]

    dados = {}
    for chave, funcao, fonte in (("selic", _selic, "Banco Central (SGS 432)"),
                                 ("usd_brl", _dolar, "AwesomeAPI")):
        try:
            valor, ref = funcao()
            if not math.isfinite(valor) or valor <= 0:
                raise ValueError("valor inválido")
            dados[chave] = {"valor": valor, "fonte": fonte, "referencia": ref, "ao_vivo": True}
        except Exception as erro:  # rede fora, timeout, JSON inesperado...
            dados[chave] = {"valor": FALLBACK[chave], "fonte": "Valor de referência (offline)",
                            "referencia": "", "ao_vivo": False, "erro": type(erro).__name__}

    _cache.update(ts=agora, dados=dados)
    return dados


# ---------------------------------------------------------------------------
# Servidor
# ---------------------------------------------------------------------------
def _num(corpo, campo, padrao=None):
    """Lê um número do JSON recebido, com mensagem de erro amigável."""
    bruto = corpo.get(campo, padrao)
    try:
        valor = float(bruto)
    except (TypeError, ValueError):
        raise ValueError(f"Campo '{campo}' inválido.")
    if not math.isfinite(valor):
        raise ValueError(f"Campo '{campo}' inválido.")
    return valor


def _rota_juros(c):
    return calculos.juros_compostos(_num(c, "valor_inicial", 0), _num(c, "aporte_mensal", 0),
                                    _num(c, "taxa"), _num(c, "meses"),
                                    c.get("tipo_taxa", "mensal"))


def _rota_comparador(c):
    pref = c.get("taxa_prefixada_anual")
    return calculos.comparador_investimentos(
        _num(c, "valor_inicial", 0), _num(c, "aporte_mensal", 0), _num(c, "meses"),
        _num(c, "selic_anual"), _num(c, "pct_cdi", 100),
        _num(c, "taxa_prefixada_anual") if pref not in (None, "") else None)


def _rota_financiamento(c):
    return calculos.comparar_financiamentos(_num(c, "valor"), _num(c, "taxa_mensal"),
                                            _num(c, "prazo"))


ROTAS_POST = {"/api/juros-compostos": _rota_juros,
              "/api/comparador": _rota_comparador,
              "/api/financiamento": _rota_financiamento}


class Handler(BaseHTTPRequestHandler):
    def _responder(self, status, corpo, tipo="application/json; charset=utf-8"):
        dados = corpo if isinstance(corpo, bytes) else json.dumps(corpo).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(dados)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(dados)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            html = (PASTA / "index.html").read_bytes()
            self._responder(200, html, "text/html; charset=utf-8")
        elif self.path == "/api/indicadores":
            self._responder(200, obter_indicadores())
        else:
            self._responder(404, {"erro": "Rota não encontrada."})

    def do_POST(self):
        rota = ROTAS_POST.get(self.path)
        if not rota:
            return self._responder(404, {"erro": "Rota não encontrada."})
        try:
            tamanho = int(self.headers.get("Content-Length", 0))
            corpo = json.loads(self.rfile.read(tamanho) or b"{}")
            if not isinstance(corpo, dict):
                raise ValueError("O corpo da requisição deve ser um objeto JSON.")
            self._responder(200, rota(corpo))
        except (ValueError, json.JSONDecodeError) as erro:
            self._responder(400, {"erro": str(erro)})
        except Exception as erro:
            self.log_message("Erro interno em %s: %s: %s", self.path, type(erro).__name__, erro)
            self._responder(500, {"erro": "Erro interno ao calcular."})

    def log_message(self, formato, *args):  # log enxuto no terminal
        print(f"[{self.address_string()}] {formato % args}")


def main():
    url = f"http://localhost:{PORT}"
    try:
        servidor = ThreadingHTTPServer((HOST, PORT), Handler)
    except OSError:
        print(f"A porta {PORT} já está em uso. Feche o outro programa e tente de novo.")
        return
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    print(f"Painel rodando em {url}  (Ctrl+C para encerrar)")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nEncerrado.")
    finally:
        servidor.server_close()


if __name__ == "__main__":
    main()
