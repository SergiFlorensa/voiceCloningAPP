from fastapi import APIRouter, UploadFile, File, Form
from app.servicios.audio import guardar_y_normalizar
from app.servicios.tts import generar_voz

router = APIRouter()

@router.post("/generar")
async def generar(texto: str = Form(...), archivo: UploadFile = File(...)):
    # 1) Guardar y convertir a WAV 16k mono limpio
    ruta_ref = await guardar_y_normalizar(archivo)

    # 2) Generar audio salida usando la voz de referencia
    ruta_salida = await generar_voz(texto=texto, ruta_referencia=ruta_ref)

    return {"ok": True, "ruta": ruta_salida}
