# TODO

## Estado actual
- Backend listo con entorno `backend/.venv` (Python 3.11.5); pruebas `pytest` pasan.
- TTS opcional: falta instalar `TTS`, `torch`, `torchaudio`, `webrtcvad` (requiere Microsoft C++ Build Tools en Windows).
- Frontend compila (`npm run build`) y lint pasa tras añadir `@types/node`.
- Servicios aún no verificados manualmente en modo dev (requiere arrancar backend y frontend).

## Próximas tareas
1. Instalar toolchain C++ + dependencias TTS para habilitar síntesis sin GPU.
2. Levantar backend (`uvicorn`) y frontend (`npm run dev`) manualmente y validar flujo básico.
3. Implementar integración end-to-end: subida, normalización y generación desde la UI.
4. Añadir manejo de estados (loading, errores) y descargas seguras.
5. Ampliar cobertura: tests con mocks de TTS, pruebas UI y scripts de limpieza de artefactos.
