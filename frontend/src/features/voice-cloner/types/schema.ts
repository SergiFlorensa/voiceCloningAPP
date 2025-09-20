import { z } from 'zod'

const MAX_FILE_SIZE = 20 * 1024 * 1024

export const voiceCloneSchema = z.object({
  text: z
    .string()
    .trim()
    .min(1, 'Introduce el texto que quieres sintetizar')
    .max(500, 'El texto no puede superar los 500 caracteres'),
  reference: z
    .any()
    .refine((file): file is File => file instanceof File, 'Selecciona un archivo de audio o v?deo')
    .refine((file) => file.size <= MAX_FILE_SIZE, 'El archivo no puede superar los 20MB'),
})

export type VoiceCloneFormValues = z.infer<typeof voiceCloneSchema>
