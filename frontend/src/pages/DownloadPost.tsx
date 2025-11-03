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

export function DownloadPost() {
  const [link, setLink] = React.useState('')

  async function handleDownloadPosts() {
    try {
      const response = await fetch(`/api/posts/download/post`, {
        method: 'post',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ link }),
      })
      if (!response.ok) {
        alert('Download failed!')
        return
      }

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'instagram_post'
      a.click()
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error(error)
    }
  }

  return (
    <div className="w-full h-full flex flex-col gap-5">
      <div className="flex w-full max-w-sm m-auto items-center gap-2">
        <Card className="w-full max-w-sm">
          <CardHeader>
            <CardTitle>Download profile posts</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col gap-5">
            <div className="grid gap-2">
              <Label htmlFor="link">Link</Label>
              <Input
                id="link"
                placeholder="link to post"
                value={link}
                onChange={(event) => setLink(event.currentTarget.value)}
                required
              />
            </div>
            <div className="flex gap-2">
              <Button variant="outline" onClick={handleDownloadPosts}>
                Download
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
