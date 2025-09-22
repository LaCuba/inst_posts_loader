import { Button } from '@/components/ui-shadcn/button'
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from '@/components/ui-shadcn/card'
import { Input } from '@/components/ui-shadcn/input'
import { Label } from '@/components/ui-shadcn/label'
import React from 'react'

export function Main() {
  const [username, setNickname] = React.useState('')

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
              <Button variant="outline">Download</Button>
              <Button variant="secondary">Stop</Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
