import { useState } from 'react'
import { zodResolver } from '@hookform/resolvers/zod'
import { Controller, useForm } from 'react-hook-form'

import { Button } from '../../../components/ui/button'
import { Input } from '../../../components/ui/input'
import { Label } from '../../../components/ui/label'
import { Spinner } from '../../../components/ui/spinner'
import { Textarea } from '../../../components/ui/textarea'
import type { VoiceCloneFormValues } from '../types/schema'
import { voiceCloneSchema } from '../types/schema'

interface VoiceCloneFormProps {
  onSubmit: (values: VoiceCloneFormValues) => Promise<void> | void
  isSubmitting: boolean
}

export function VoiceCloneForm({ onSubmit, isSubmitting }: VoiceCloneFormProps) {
  const [fileName, setFileName] = useState<string | null>(null)

  const {
    control,
    handleSubmit,
    register,
    reset,
    formState: { errors },
  } = useForm<VoiceCloneFormValues>({
    resolver: zodResolver(voiceCloneSchema),
    defaultValues: {
      text: '',
      reference: undefined,
    },
  })

  const handleFormSubmit = handleSubmit(async (values) => {
    await onSubmit(values)
    reset()
    setFileName(null)
  })

  return (
    <form className="space-y-6" onSubmit={handleFormSubmit}>
      <div className="space-y-2">
        <Label htmlFor="voice-text">Texto a sintetizar</Label>
        <Textarea
          id="voice-text"
          placeholder="Escribe aqui el mensaje que quieres escuchar..."
          {...register('text')}
        />
        {errors.text && <p className="text-sm text-rose-300">{errors.text.message}</p>}
        <p className="text-xs text-slate-500">Consejo: frases de 2-3 lineas generan mejores resultados.</p>
      </div>

      <div className="space-y-2">
        <Label htmlFor="voice-reference">Sube un audio o video de referencia</Label>
        <Controller
          control={control}
          name="reference"
          render={({ field: { onChange } }) => (
            <Input
              id="voice-reference"
              type="file"
              accept="audio/*,video/*"
              onChange={(event) => {
                const file = event.target.files?.[0]
                onChange(file)
                setFileName(file?.name ?? null)
              }}
            />
          )}
        />
        <p className="text-xs text-slate-500">
          Max. 20MB. Ideal: fragmentos de 10-20 segundos sin ruido de fondo.
        </p>
        {fileName && <p className="text-xs text-slate-400">Seleccionado: {fileName}</p>}
        {errors.reference && <p className="text-sm text-rose-300">{errors.reference.message}</p>}
      </div>

      <div className="flex items-center justify-end gap-3">
        <Button type="submit" disabled={isSubmitting} variant="primary" size="lg">
          {isSubmitting ? (
            <span className="flex items-center gap-2">
              <Spinner size={18} /> Generando...
            </span>
          ) : (
            'Generar voz clonada'
          )}
        </Button>
      </div>
    </form>
  )
}
