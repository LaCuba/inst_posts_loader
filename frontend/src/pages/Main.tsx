import React from 'react'

import { Button } from '@/components/ui-shadcn/button'
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from '@/components/ui-shadcn/card'
import { Input } from '@/components/ui-shadcn/input'
import { Label } from '@/components/ui-shadcn/label'
import { useSSE } from '@/lib/hooks'
import { Progress } from '@/components/ui-shadcn/progress'

type ProgressData = {
  status: string
  total_posts: number
  percent: number
}

export function Main() {
  const [username, setNickname] = React.useState('')
  const [jobId, setJobId] = React.useState<string>()

  const { data, error } = useSSE<ProgressData>(
    `/api/posts/download_status/${jobId}`,
    Boolean(jobId),
  )

  React.useEffect(() => {
    const jobId = window.localStorage.getItem('active_job_id')
    if (jobId) setJobId(jobId)
  }, [])

  async function handleDownloadPosts() {
    try {
      const response = await fetch(`/api/posts/download/${username}`, {
        method: 'get',
      })
      const data = (await response.json()) as {
        job_id: string
      }
      if (data.job_id) {
        window.localStorage.setItem('active_job_id', data.job_id)
        setJobId(data.job_id)
      }
    } catch (error) {
      console.error(error)
    }
  }

  const lastProgress = data[data.length - 1]

  React.useEffect(() => {
    if (lastProgress?.percent === 100) {
      setJobId(undefined)
      window.localStorage.removeItem('active_job_id')
    }
  }, [lastProgress?.percent])

  return (
    <div className="w-full h-full flex flex-col gap-5">
      <div className="flex w-full max-w-sm m-auto items-center gap-2">
        <Card className="w-full max-w-sm">
          <CardHeader>
            <CardTitle>Download profile posts</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col gap-5">
            <div className="grid gap-2">
              <Label htmlFor="username">Username</Label>
              <Input
                id="username"
                placeholder="inst_username"
                value={username}
                onChange={(event) => setNickname(event.currentTarget.value)}
                required
              />
            </div>
            <div className="flex gap-2">
              <Button
                variant="outline"
                onClick={handleDownloadPosts}
                disabled={Boolean(jobId)}
              >
                Download
              </Button>
              <Button variant="secondary">Stop</Button>
            </div>
            {Boolean(lastProgress?.percent !== undefined) && (
              <Progress value={lastProgress.percent} />
            )}
            <div className="text-red">{error}</div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
