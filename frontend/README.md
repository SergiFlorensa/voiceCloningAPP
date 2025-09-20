# Voice Cloning Frontend

React + Vite interface for the voice cloning backend. It lets you upload a reference
recording, type the desired text, and trigger the inference pipeline to obtain a cloned voice clip.

## Scripts

```bash
npm run dev     # start the dev server
npm run build   # compile TypeScript and bundle with Vite
npm run lint    # execute ESLint across the project
npm run preview # serve the production build locally
```

## Environment variables

Create a `.env` file (based on `.env.example`) with the backend URL:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## Structure

- `src/app`: application composition and global providers
- `src/features/voice-cloner`: feature modules for the cloning flow
- `src/components/ui`: reusable UI components styled with TailwindCSS
- `src/lib`: shared helpers (HTTP client, utilities)
- `src/styles`: global styles (Tailwind v4)

HTTP communication relies on `@tanstack/react-query` and `ky`, using a configurable `prefixUrl`.
