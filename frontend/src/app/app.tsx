import { AppProviders } from './providers'
import { VoiceClonerPage } from '../features/voice-cloner/components/voice-cloner-page'

export default function App() {
  return (
    <AppProviders>
      <VoiceClonerPage />
    </AppProviders>
  )
}
