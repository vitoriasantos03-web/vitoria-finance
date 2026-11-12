from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(title="Controle Financeiro - Vi")

# Serve os arquivos bonitos da pasta static
app.mount("/static", StaticFiles(directory="static"), name="static")

transacoes = [
    {"id": 1, "descricao": "Salário", "valor": 3500.00, "tipo": "receita", "categoria": "Salário", "usuario": "Iago"},
    {"id": 2, "descricao": "Aluguel", "valor": -1200.00, "tipo": "despesa", "categoria": "Moradia", "usuario": "Severina"},
    {"id": 3, "descricao": "Mercado", "valor": -450.00, "tipo": "despesa", "categoria": "Alimentação", "usuario": "Pierre"},
]

class Transacao(BaseModel):
    descricao: str
    valor: float
    tipo: str
    categoria: str
    usuario: str

@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.get("/transacoes")
def listar_transacoes():
    return transacoes

@app.post("/transacoes")
def criar_transacao(t: Transacao):
    novo_id = len(transacoes) + 1
    nova = {"id": novo_id, **t.model_dump()}
    transacoes.append(nova)
    return nova

@app.get("/saldo")
def saldo():
    total = sum(t["valor"] for t in transacoes)
    return {"saldo_total": total}
@app.get("/resumo")
def resumo():
    receitas = sum(t["valor"] for t in transacoes if t["valor"] > 0)
    despesas = sum(t["valor"] for t in transacoes if t["valor"] < 0)
    return {"receitas": receitas, "despesas": despesas, "saldo": receitas + despesas}

@app.delete("/transacoes/{transacao_id}")
def deletar_transacao(transacao_id: int):
    global transacoes
    transacoes = [t for t in transacoes if t["id"] != transacao_id]
    return {"ok": True}