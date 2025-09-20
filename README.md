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

------------------------------------------------------
🎙 Proyecto: Clonador de Voz AI (estilo NoteGPT, solo Voice Cloning)
📌 Descripción

Aplicación web para clonar voces a partir de un audio/vídeo subido por el usuario.
Flujo básico:

El usuario sube un archivo de audio/vídeo.

El backend extrae el audio limpio.

El modelo open-source genera un embedding de hablante (las características únicas de esa voz).

El usuario escribe un texto → el sistema lo sintetiza con la voz clonada.

Se devuelve un archivo de audio reproducible/descargable.

⚠️ Uso personal/divertido. Respeta derechos de voz/imágenes si decides compartir resultados.

🛠️ Tecnologías principales
Frontend

React + Vite → interfaz rápida, moderna y fácil de desplegar.

TailwindCSS → estilos responsivos y limpios.

react-dropzone → para subir archivos.

Reproductor de audio nativo <audio> de HTML5.

Backend

Python 3.10+

FastAPI → para exponer endpoints (subir audio, clonar voz, generar TTS).

Uvicorn → servidor ASGI rápido.

ffmpeg → extraer audio de vídeos y convertir formatos.

librosa o pydub → análisis y preprocesamiento de audio.

Modelos open-source

OpenVoice (MyShell) o Coqui TTS (XTTS-v2) → clonación de voz + TTS multilingüe.

HiFi-GAN (ya integrado en Coqui) → vocoder para audio natural.

webrtcvad → detección de voz (para limpiar silencios).

Infraestructura

Docker → contenedores para backend/modelos.

GPU NVIDIA con CUDA (opcional, pero recomendado para inferencias rápidas).

Almacenamiento: inicio en local, posibilidad de S3/MinIO si lo escalas.
