import { Card, CardContent, CardHeader } from '@/components/ui-shadcn/card'
import { Skeleton } from '@/components/ui-shadcn/skeleton'

export function PostCardSkeleton() {
  return (
    <Card className="w-full max-w-md mx-auto rounded-2xl shadow-md overflow-hidden">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <div className="flex items-center gap-2">
          <Skeleton className="h-10 w-10 rounded-full" />
          <Skeleton className="h-4 w-24" />
        </div>
        <Skeleton className="h-4 w-16" />
      </CardHeader>

      <div className="w-full h-64">
        <Skeleton className="w-full h-full" />
      </div>

      <CardContent>
        <div className="space-y-2 mt-2">
          <Skeleton className="h-3 w-full" />
          <Skeleton className="h-3 w-5/6" />
          <Skeleton className="h-3 w-2/3" />
        </div>
      </CardContent>
    </Card>
  )
}
