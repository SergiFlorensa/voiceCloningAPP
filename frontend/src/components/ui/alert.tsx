import { cn } from '../../lib/utils'

export interface AlertProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'info' | 'success' | 'error'
}

const variantStyles: Record<NonNullable<AlertProps['variant']>, string> = {
  info: 'border-sky-700/50 bg-sky-950/40 text-sky-200',
  success: 'border-emerald-700/50 bg-emerald-950/40 text-emerald-200',
  error: 'border-rose-700/50 bg-rose-950/40 text-rose-200',
}

export function Alert({ className, variant = 'info', ...props }: AlertProps) {
  return (
    <div
      role="alert"
      className={cn(
        'w-full rounded-xl border px-4 py-3 text-sm leading-relaxed shadow-inner',
        variantStyles[variant],
        className,
      )}
      {...props}
    />
  )
}
