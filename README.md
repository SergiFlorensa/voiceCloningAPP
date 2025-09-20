# 🎙️ Clonador de Voz (Proyecto Personal)

Aplicación inspirada en [notegpt.io](https://notegpt.io/ai-voice-cloning), pero hecha desde cero para uso personal y divertido.
Permite **subir un audio o vídeo de referencia** → extraer la voz → escribir cualquier frase → generar la frase con la misma voz usando IA.

---

## 🚀 Objetivo de la App
- Subir un **clip de voz o vídeo** de una persona.
- El sistema normaliza el audio (formato `.wav`, 16kHz, mono).
- Con **XTTSv2 (Coqui TTS)** se entrena de manera instantánea una voz clonada.
- El usuario escribe un texto en un cuadro → el sistema devuelve un audio en la voz clonada.
- Uso **únicamente personal/divertido**.
- **Disclaimer**: toda voz generada debe indicarse como imitación IA.

---

## 🧰 Requisitos técnicos

### Generales
- **Node.js 20+**
- **Python 3.10+**
- **Git** y cuenta en GitHub
- **FFmpeg** (para procesar y normalizar audio/video)
- **Opcional GPU NVIDIA + CUDA** (para aceleración de inferencia)

### Frontend
- **React + Vite + TypeScript**
- **TailwindCSS v4** con `@tailwindcss/vite`
- Estructura **feature-based**:


### Backend
- **FastAPI** (Python)
- Librerías:
- `fastapi`
- `uvicorn`
- `ffmpeg-python`
- `pydub`
- `librosa`
- `webrtcvad`
- `python-multipart`
- `TTS` (Coqui, modelo `xtts_v2`)

---

## 🗂️ Estructura del Proyecto

