import { useMutation } from '@tanstack/react-query'
import { HTTPError } from 'ky'

import { generateVoice } from '../api/generate-voice'
import type { VoiceCloneFormValues } from '../types/schema'
import type { VoiceCloneResponse } from '../types/api'

interface MutationPayload {
  text: string
  file: File
}

async function mutationFn({ text, file }: MutationPayload): Promise<VoiceCloneResponse> {
  const formData = new FormData()
  formData.append('text', text)
  formData.append('reference', file)

  try {
    return await generateVoice(formData)
  } catch (error) {
    if (error instanceof HTTPError) {
      let detail = 'No se pudo generar la voz'
      try {
        const data = (await error.response.json()) as { detail?: string }
        if (typeof data.detail === 'string' && data.detail.length > 0) {
          detail = data.detail
        }
      } catch {
        // ignored
      }
      throw new Error(detail)
    }

    if (error instanceof Error) {
      throw error
    }

    throw new Error('Error inesperado al generar la voz')
  }
}

export function useVoiceClone() {
  return useMutation<VoiceCloneResponse, Error, VoiceCloneFormValues>({
    mutationFn: async (values) => mutationFn({ text: values.text, file: values.reference }),
  })
}
