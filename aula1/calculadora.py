from fastapi import FastAPI

app = FastAPI()

@app.get("/soma")
def soma(a: int = 5, b: int = 7):
    return {"operacao": "soma","resultado": a + b}

@app.get("/subtracao")
def subtracao(a: int = 10, b: int = 3):
    return {"operacao": "subtracao","resultado": a - b}

@app.get("/multiplicacao")
def multiplicacao(a: int = 5, b: int = 7):
    return {"operacao": "multiplicacao","resultado": a * b}

@app.get("/divisao")
def divisao(a: int = 15, b: int = 5):
    return {"operacao": "divisao","resultado": a / b}

@app.get("/raiz")
def raiz(a: int = 9):
    return {"operacao": "raiz_quadrada","resultado": a**(1/2)}