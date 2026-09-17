from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="API Inventaire serveurs", version="1.0.0")

class Serveur(BaseModel):
    hostname: str = Field(min_length=1, examples=["web-prod-01"])
    ip: str
    env: str = "prod"

# "base de données" en mémoire pour l'exemple
serveurs: dict[int, Serveur] = {
    1: Serveur(hostname="web-prod-01", ip="10.0.1.10", env="prod"),
}

@app.get("/serveurs")
def lister_serveurs() -> list[Serveur]:
    return list(serveurs.values())

@app.get("/serveurs/{serveur_id}")
def lire_serveur(serveur_id: int) -> Serveur:
    if serveur_id not in serveurs:
        raise HTTPException(status_code=404, detail="Serveur introuvable")
    return serveurs[serveur_id]

@app.post("/serveurs", status_code=201)
def creer_serveur(serveur: Serveur) -> Serveur:
    nouvel_id = max(serveurs) + 1
    serveurs[nouvel_id] = serveur
    return serveur