import { Card } from '@/components/ui/card'
import { Skeleton } from '@/components/ui/skeleton'

export function MatchCardSkeleton() {
  return (
    <Card className="overflow-hidden">
      {/* Header bar */}
      <div className="flex items-center justify-between px-3.5 py-2 border-b border-border/40 bg-muted/30">
        <Skeleton className="h-4 w-24" />
        <Skeleton className="h-4 w-12" />
      </div>
      {/* Teams section */}
      <div className="px-3.5 py-3 space-y-3">
        <div className="flex items-center gap-3">
          <div className="flex-1 space-y-2.5">
            <div className="flex items-center gap-2.5">
              <Skeleton className="h-7 w-7 rounded-full" />
              <Skeleton className="h-5 w-32" />
            </div>
            <div className="flex items-center gap-2.5">
              <Skeleton className="h-7 w-7 rounded-full" />
              <Skeleton className="h-5 w-28" />
            </div>
          </div>
          <Skeleton className="h-12 w-12 rounded-full" />
        </div>
      </div>
      {/* Footer */}
      <div className="flex items-center justify-between px-3.5 py-2 border-t border-border/40 bg-muted/20">
        <div className="flex gap-1">
          <Skeleton className="h-5 w-10 rounded" />
          <Skeleton className="h-5 w-10 rounded" />
          <Skeleton className="h-5 w-10 rounded" />
        </div>
        <Skeleton className="h-4 w-4" />
      </div>
    </Card>
  )
}
