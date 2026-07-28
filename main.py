import os
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
}

HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Numeração de Propostas</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #f5f5f5;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .card {
      background: white;
      border-radius: 16px;
      padding: 48px 40px;
      text-align: center;
      box-shadow: 0 2px 16px rgba(0,0,0,0.08);
      width: 100%;
      max-width: 420px;
      margin: 16px;
    }
    h1 {
      font-size: 20px;
      font-weight: 600;
      color: #1a1a1a;
      margin-bottom: 8px;
    }
    p.sub {
      font-size: 14px;
      color: #888;
      margin-bottom: 40px;
    }
    .numero {
      font-size: 48px;
      font-weight: 700;
      color: #1a1a1a;
      letter-spacing: 4px;
      min-height: 60px;
      margin-bottom: 12px;
    }
    .numero.loading { color: #ccc; }
    .numero.gerado { color: #0066ff; }
    .label-num {
      font-size: 12px;
      color: #aaa;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 40px;
      min-height: 18px;
    }
    button {
      background: #0066ff;
      color: white;
      border: none;
      border-radius: 10px;
      padding: 14px 32px;
      font-size: 16px;
      font-weight: 600;
      cursor: pointer;
      width: 100%;
      transition: background 0.15s, transform 0.1s;
    }
    button:hover { background: #0052cc; }
    button:active { transform: scale(0.98); }
    button:disabled { background: #ccc; cursor: not-allowed; }
    .copy-btn {
      background: none;
      border: 1.5px solid #ddd;
      color: #555;
      font-size: 13px;
      font-weight: 500;
      padding: 8px 20px;
      border-radius: 8px;
      margin-top: 12px;
      width: auto;
      display: none;
    }
    .copy-btn:hover { background: #f5f5f5; border-color: #bbb; }
    .copy-btn.visible { display: inline-block; }
    .copy-btn.copiado { color: #2e7d32; border-color: #2e7d32; }
    .erro { color: #cc0000; font-size: 13px; margin-top: 8px; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Numeração de Propostas</h1>
    <p class="sub">Cada clique gera um número único e sequencial</p>

    <div class="numero" id="numero">—</div>
    <div class="label-num" id="label"></div>

    <button id="btn" onclick="gerar()">Gerar próximo número</button>
    <button class="copy-btn" id="copy-btn" onclick="copiar()">Copiar</button>
    <div class="erro" id="erro"></div>
  </div>

  <script>
    let ultimoNumero = null;

    async function gerar() {
      const btn = document.getElementById('btn');
      const numEl = document.getElementById('numero');
      const labelEl = document.getElementById('label');
      const copyBtn = document.getElementById('copy-btn');
      const erroEl = document.getElementById('erro');

      btn.disabled = true;
      btn.textContent = 'Gerando...';
      numEl.className = 'numero loading';
      numEl.textContent = '...';
      labelEl.textContent = '';
      copyBtn.className = 'copy-btn';
      erroEl.textContent = '';

      try {
        const res = await fetch('/gerar', { method: 'POST' });
        if (!res.ok) throw new Error('Erro ao gerar número');
        const data = await res.json();
        ultimoNumero = data.numero;
        numEl.textContent = ultimoNumero;
        numEl.className = 'numero gerado';
        labelEl.textContent = 'Número gerado com sucesso';
        copyBtn.className = 'copy-btn visible';
        copyBtn.textContent = 'Copiar';
        copyBtn.classList.remove('copiado');
      } catch (e) {
        numEl.textContent = '—';
        numEl.className = 'numero';
        erroEl.textContent = 'Não foi possível gerar o número. Tente novamente.';
      } finally {
        btn.disabled = false;
        btn.textContent = 'Gerar próximo número';
      }
    }

    function copiar() {
      if (!ultimoNumero) return;
      navigator.clipboard.writeText(ultimoNumero).then(() => {
        const btn = document.getElementById('copy-btn');
        btn.textContent = 'Copiado!';
        btn.classList.add('copiado');
        setTimeout(() => {
          btn.textContent = 'Copiar';
          btn.classList.remove('copiado');
        }, 2000);
      });
    }
  </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def index():
    return HTML

@app.post("/gerar")
def gerar_numero():
    try:
        res = httpx.post(
            f"{SUPABASE_URL}/rest/v1/rpc/gerar_proximo_numero",
            headers=HEADERS,
        )
        res.raise_for_status()
        numero = res.json()
        return {"numero": f"PC{numero:05d}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
