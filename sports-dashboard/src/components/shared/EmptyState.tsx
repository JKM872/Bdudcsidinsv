import { SearchX } from 'lucide-react'

interface Props {
  title: string
  description?: string
}

export function EmptyState({ title, description }: Props) {
  return (
    <div className="flex flex-col items-center justify-center py-16 text-center">
      <SearchX className="h-12 w-12 text-muted-foreground/50 mb-4" />
      <h3 className="font-semibold text-lg">{title}</h3>
      {description && (
        <p className="text-sm text-muted-foreground mt-1 max-w-sm">{description}</p>
      )}
    </div>
  )
}
