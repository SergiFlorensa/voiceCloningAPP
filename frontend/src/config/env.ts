function normalizeBaseUrl(raw: string) {
  if (!raw) {
    return '/api/v1'
  }
  if (raw.endsWith('/')) {
    return raw.slice(0, -1)
  }
  return raw
}

const rawApiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? '/api/v1'
const apiBaseUrl = normalizeBaseUrl(rawApiBaseUrl)

export const env = {
  apiBaseUrl,
  isDev: import.meta.env.DEV,
}

export function resolveApiUrl(path: string): string {
  if (path.startsWith('http')) {
    return path
  }
  const suffix = path.startsWith('/') ? path : `/${path}`
  return `${apiBaseUrl}${suffix}`
}
