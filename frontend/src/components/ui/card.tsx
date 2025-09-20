import { cn } from '../../lib/utils'

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {}

export function Card({ className, ...props }: CardProps) {
  return (
    <div
      className={cn('rounded-2xl border border-slate-800 bg-slate-900/60 p-6 shadow-lg shadow-slate-950/60 backdrop-blur', className)}
      {...props}
    />
  )
}
