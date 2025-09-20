import { useState } from 'react'

import { Alert } from '../../../components/ui/alert'
import { Button } from '../../../components/ui/button'
import { Card } from '../../../components/ui/card'

interface GeneratedPreviewProps {
  downloadUrl: string | null
  isVisible: boolean
}

export function GeneratedPreview({ downloadUrl, isVisible }: GeneratedPreviewProps) {
  const [copied, setCopied] = useState(false)

  if (!isVisible || !downloadUrl) {
    return null
  }

  const handleCopy = async () => {
    if (!navigator?.clipboard) {
      window.prompt('Copy the link manually:', downloadUrl)
      return
    }

    try {
      await navigator.clipboard.writeText(downloadUrl)
      setCopied(true)
      setTimeout(() => setCopied(false), 2500)
    } catch {
      setCopied(false)
    }
  }

  return (
    <Card className="space-y-4">
      <div className="space-y-1">
        <h2 className="text-lg font-semibold text-slate-100">Output</h2>
        <p className="text-sm text-slate-400">Play or download the generated clip.</p>
      </div>

      <audio className="w-full" controls src={downloadUrl} />

      <div className="flex flex-wrap items-center gap-3">
        <Button type="button" variant="secondary" onClick={() => window.open(downloadUrl, '_blank')}>
          Open in a new tab
        </Button>
        <Button type="button" variant="ghost" onClick={handleCopy}>
          {copied ? 'Copied' : 'Copy link'}
        </Button>
      </div>

      <Alert variant="info" className="text-xs">
        If you share the result, make it clear that the voice was generated with AI.
      </Alert>
    </Card>
  )
}
