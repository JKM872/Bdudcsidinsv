import { Card, CardContent, CardHeader } from '@/components/ui/card'
import { Skeleton } from '@/components/ui/skeleton'

export function MatchCardSkeleton() {
  return (
    <Card className="overflow-hidden">
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <Skeleton className="h-5 w-24" />
          <Skeleton className="h-4 w-12" />
        </div>
      </CardHeader>
      <CardContent className="space-y-3">
        <div className="space-y-1">
          <Skeleton className="h-5 w-40" />
          <Skeleton className="h-5 w-36" />
        </div>
        <div className="grid grid-cols-2 gap-3 border-t pt-2">
          <Skeleton className="h-10 w-full" />
          <Skeleton className="h-10 w-full" />
        </div>
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-1.5 w-full rounded-full" />
      </CardContent>
    </Card>
  )
}
