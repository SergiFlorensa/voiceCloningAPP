import os, uuid, subprocess
from fastapi import UploadFile

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CARPETA_ARCHIVOS = os.path.join(BASE_DIR, "archivos")
os.makedirs(CARPETA_ARCHIVOS, exist_ok=True)

async def guardar_y_normalizar(archivo: UploadFile) -> str:
    # Guardar original
    ext = (archivo.filename or "input").split(".")[-1].lower()
    nombre_base = f"{uuid.uuid4().hex}"
    ruta_orig = os.path.join(CARPETA_ARCHIVOS, f"{nombre_base}.{ext}")
    with open(ruta_orig, "wb") as f:
        f.write(await archivo.read())

    # Convertir a WAV 16k mono con ffmpeg
    ruta_wav = os.path.join(CARPETA_ARCHIVOS, f"{nombre_base}.wav")
    cmd = [
        "ffmpeg", "-y",
        "-i", ruta_orig,
        "-ac", "1", "-ar", "16000",
        ruta_wav
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return ruta_wav
