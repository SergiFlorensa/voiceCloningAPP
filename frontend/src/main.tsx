import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

import App from './app/app'
import './styles/global.css'

const rootElement = document.getElementById('root')

if (!rootElement) {
  throw new Error('Root element not found. Unable to mount the application')
}

createRoot(rootElement).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
