# backend/main.py  (FastAPI recommended)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.adme import calculate_adme
from backend.toxicity import predict_toxicity
from backend.predictor import predict_targets
from backend.synthetic_access import calculate_sa_score
from backend.similarity import find_similar
from backend.literature import search_pubmed
from backend.bioactivity import fetch_bioactivity

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

@app.post("/analyze")
def analyze(body: dict):
    smiles = body["smiles"]
    return {
        "targets": predict_targets(smiles),
        "adme": calculate_adme(smiles),
        "toxicity": predict_toxicity(smiles),
        "sa": calculate_sa_score(smiles),
        "similar": find_similar(smiles),
    }

@app.get("/bioactivity/{target}")
def bioactivity(target: str):
    return fetch_bioactivity(target)

@app.get("/literature/{query}")
def literature(query: str):
    return search_pubmed(query)