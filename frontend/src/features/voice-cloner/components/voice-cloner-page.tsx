import { Alert } from '../../../components/ui/alert'
import { Card } from '../../../components/ui/card'
import { VoiceCloneForm } from './voice-clone-form'
import { GeneratedPreview } from './generated-preview'
import { useVoiceClone } from '../hooks/use-voice-clone'

export function VoiceClonerPage() {
  const mutation = useVoiceClone()

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-950 to-slate-900">
      <div className="mx-auto flex w-full max-w-4xl flex-col gap-8 px-6 py-16">
        <header className="space-y-3 text-center">
          <p className="text-xs uppercase tracking-[0.35em] text-sky-400/80">Personal project</p>
          <h1 className="text-4xl font-semibold tracking-tight text-balance text-slate-100">
            Voice cloning with XTTS v2
          </h1>
          <p className="mx-auto max-w-2xl text-sm text-slate-400">
            Upload a clean voice snippet, type the desired message, and receive a clip in the same voice.
            Built for personal experiments and learning.
          </p>
        </header>

        {mutation.isError && (
          <Alert variant="error">
            {mutation.error?.message ?? 'We could not complete the voice generation. Please try again.'}
          </Alert>
        )}

        <Card className="p-8">
          <VoiceCloneForm
            isSubmitting={mutation.isPending}
            onSubmit={async (values) => {
              await mutation.mutateAsync(values)
            }}
          />
        </Card>

        <GeneratedPreview
          downloadUrl={mutation.data?.downloadUrl ?? null}
          isVisible={mutation.isSuccess && Boolean(mutation.data?.downloadUrl)}
        />
      </div>
    </div>
  )
}
