import { apiClient } from '../../../lib/http/client'
import type { VoiceCloneResponse } from '../types/api'

interface RawVoiceCloneResponse {
  ok: boolean
  download_url: string
}

export async function generateVoice(formData: FormData): Promise<VoiceCloneResponse> {
  const response = await apiClient
    .post('voice-clone/generate', {
      body: formData,
    })
    .json<RawVoiceCloneResponse>()

  return {
    ok: response.ok,
    downloadUrl: response.download_url,
  }
}
