from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.rutas_clonador import router as clonador_router

app = FastAPI(title="Clonador de Voz (personal)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ajústalo si quieres más seguridad
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {"ok": True}

app.include_router(clonador_router, prefix="/api/clonador", tags=["clonador"])
