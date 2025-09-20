import os, uuid
from TTS.api import TTS

# Carga perezosa del modelo (una sola vez)
_tts = None
def _get_tts():
    global _tts
    if _tts is None:
        _tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
    return _tts

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CARPETA_ARCHIVOS = os.path.join(BASE_DIR, "archivos")
os.makedirs(CARPETA_ARCHIVOS, exist_ok=True)

async def generar_voz(texto: str, ruta_referencia: str) -> str:
    tts = _get_tts()
    nombre = f"salida-{uuid.uuid4().hex}.wav"
    ruta_out = os.path.join(CARPETA_ARCHIVOS, nombre)
    # XTTSv2 acepta speaker_wav para clonar timbre
    tts.tts_to_file(text=texto, speaker_wav=ruta_referencia, file_path=ruta_out)
    return f"/api/clonador/descargas/{nombre}"
