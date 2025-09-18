import React from 'react'

import { Button } from '@/components/ui-shadcn/button'
import { Input } from '@/components/ui-shadcn/input'
import { Select } from '@/components/ui/Select'

export function Accounts() {
  const [form, setForm] = React.useState({
    nickname: '',
    year: '',
  })

  return (
    <div className="w-full h-full flex flex-col gap-5">
      <div className="flex w-full max-w-sm m-auto items-center gap-2">
        <Input
          placeholder="nickname"
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
        </Button>
      </div>
    </div>
  )
}
