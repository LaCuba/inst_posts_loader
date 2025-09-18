import { Button } from '@/components/ui-shadcn/button'
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from '@/components/ui-shadcn/card'
import { Input } from '@/components/ui-shadcn/input'
import { Label } from '@/components/ui-shadcn/label'
import { Select } from '@/components/ui/Select'
import React from 'react'

export function Main() {
  const [form, setForm] = React.useState({
    nickname: '',
    year: '',
  })

  return (
    <div className="w-full h-full flex flex-col gap-5">
      <div className="flex w-full max-w-sm m-auto items-center gap-2">
        <Card className="w-full max-w-sm">
          <CardHeader>
            <CardTitle>Download profile posts</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col gap-5">
            <div className="grid gap-2">
              <Label htmlFor="nickname">Nickname</Label>
              <Input
                id="nickname"
                // type="email"
                placeholder="insta_nickname"
                required
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="count_of_posts">Count of posts</Label>
              <Input id="count_of_posts" placeholder="300" required />
            </div>
            <div className="flex gap-2">
              <Button variant="outline">Download</Button>
              <Button variant="secondary">Stop</Button>
            </div>
          </CardContent>
        </Card>
        {/* <Input
          placeholder="nickname"
          value={form.nickname}
          onChange={(event) =>
            setForm((prev) => ({
              ...prev,
              nickname: event.currentTarget.value,
            }))
          }
        />
        <Input
          placeholder="Count of posts"
          value={form.nickname}
          onChange={(event) =>
            setForm((prev) => ({
              ...prev,
              nickname: event.currentTarget.value,
            }))
          }
        />
        <Select
          value={form.year}
          options={[]}
          onChange={(value) => setForm((prev) => ({ ...prev, year: value }))}
        />
        <Button type="submit" variant="outline">
          Subscribe
        </Button> */}
      </div>
    </div>
  )
}
