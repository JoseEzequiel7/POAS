from fastapi import FastAPI
import requests

app = FastAPI()

API_KEY = "bee0cd372afdda92a865788982299c40"

HEADERS = {
    "chave-api-dados": API_KEY
}

BASE_URL = "https://api.portaldatransparencia.gov.br/api-de-dados"


def buscar_dados(endpoint, params):
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code == 200:
        return response.json()
    
    return []


@app.get("/cpf/{cpf}")
def consultar_cpf(cpf: str):

    pessoa = buscar_dados("pessoa_fisica", {"cpf": cpf})

    if not pessoa:
        return {"erro": "CPF não encontrado"}

    p = pessoa[0]

    nome = p.get("nome")
    cpf_formatado = p.get("cpfFormatado")
    situacao = p.get("situacaoCadastral")
    nis = p.get("nis")

    viagens = buscar_dados("viagens_por_cpf", {"cpf": cpf})

    lista_viagens = []
    for v in viagens:
        lista_viagens.append({
            "destino": v.get("destino"),
            "valor": v.get("valorTotal"),
            "periodo": f"{v.get('dataInicio')} até {v.get('dataFim')}"
        })

    lista_peti = []
    if nis:
        peti = buscar_dados("peti_por_cpf_nis", {"nis": nis})

        for p in peti:
            lista_peti.append({
                "valor": p.get("valor"),
                "mes": p.get("mesReferencia")
            })

    lista_bpc = []
    if nis:
        bpc = buscar_dados("bpc_por_cpf_nis", {"nis": nis})

        for b in bpc:
            lista_bpc.append({
                "valor": b.get("valor"),
                "mes": b.get("mesReferencia")
            })

    return {
        "pessoa": {
            "nome": nome,
            "cpf": cpf_formatado,
            "situacao": situacao
        },
        "resumo": {
            "total_viagens": len(lista_viagens),
            "recebe_peti": len(lista_peti) > 0,
            "recebe_bpc": len(lista_bpc) > 0
        },
        "detalhes": {
            "viagens": lista_viagens,
            "peti": lista_peti,
            "bpc": lista_bpc
        }
    }
