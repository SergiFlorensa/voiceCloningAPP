# TODO

## Current status
- Backend runs via `uvicorn app.main:app`; `/` and `/api/health` respond 200 with status payloads.
- Frontend dev server renders the UI and `npm run build`/`npm run lint` succeed.
- Optional TTS stack (`TTS`, `torch`, `torchaudio`, `webrtcvad`) still pending; requires Microsoft C++ Build Tools on Windows.
- CI workflows (backend/frontend) and documentation (README, SETUP, ARCHITECTURE) are in place.

## Next steps
1. Install the C++ build tools and add the TTS dependencies to unlock voice synthesis on CPU.
2. Implement the full backend flow (upload, normalize, synthesize, serve downloads) with proper error handling and cleanup.
3. Wire the frontend feature end-to-end: file picker, form validation, mutation states, audio preview and download link.
4. Extend automated coverage (backend tests with TTS mocks, frontend component/hook tests) and add maintenance scripts (storage cleanup, model pruning).
5. Prepare deployment enhancements (Docker image tweaks, optional GPU build, environment documentation) once the flow is stable.
