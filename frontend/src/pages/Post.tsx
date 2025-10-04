import { useParams } from 'react-router'

import type { Post as PostType } from '../typings'
import { useSWR } from '@/lib/hooks/useSWR'
import { Card, CardContent, CardHeader } from '@/components/ui-shadcn/card'
import { PostCardSkeleton } from '@/components/common/PostSkeleton'

export function Post() {
  const { postId } = useParams()

  const { data: post } = useSWR<PostType>(`/api/posts/${postId}`)

  if (!post)
    return (
      <div className="p-6">
        <PostCardSkeleton />
      </div>
    )

  function handleOpenImage() {
    window.open(post.url, '_blank', 'noopener,noreferrer')
  }

  return (
    <div className="max-h-full p-6 overflow-auto">
      <Card className="w-full max-w-2xl mx-auto rounded-2xl shadow-md overflow-hidden">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <div className="flex items-center gap-2">
            <span className="font-semibold">{post.username}</span>
          </div>
          <span className="text-sm text-gray-500">
            {new Date(post.date_utc).toLocaleDateString('en-GB')}
          </span>
        </CardHeader>

        {post.url && (
          <div className="w-full h-222 overflow-hidden cursor-pointer">
            <img
              onClick={handleOpenImage}
              src={post.url}
              alt="Post"
              className="w-full h-full object-cover"
            />
          </div>
        )}

        <CardContent>
          {post.caption && (
            <p className="text-lg text-gray-300">{post.caption}</p>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
