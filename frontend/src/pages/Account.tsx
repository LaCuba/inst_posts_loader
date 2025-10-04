import React from 'react'

import { Button } from '@/components/ui-shadcn/button'
import { Input } from '@/components/ui-shadcn/input'
import { Select } from '@/components/ui/Select'
import { useNavigate, useParams } from 'react-router'
import type { Post, SetFormPayload } from '@/typings'
import { PostCard } from '@/components/common/PostCard'
import { useSWR } from '@/lib/hooks/useSWR'

const MOCK_DATES = [
  {
    value: '31-31-2025',
    label: '2025',
  },
  {
    value: '31-31-2024',
    label: '2024',
  },
  {
    value: '31-31-2023',
    label: '2023',
  },
  {
    value: '31-31-2022',
    label: '2022',
  },
  {
    value: '31-31-2021',
    label: '2021',
  },
  {
    value: '31-31-2020',
    label: '2020',
  },
  {
    value: '31-31-2019',
    label: '2019',
  },
  {
    value: '31-31-2018',
    label: '2018',
  },
  {
    value: '31-31-2017',
    label: '2017',
  },
  {
    value: '31-31-2016',
    label: '2016',
  },
  {
    value: '31-31-2015',
    label: '2015',
  },
  {
    value: '31-31-2014',
    label: '2014',
  },
  {
    value: '31-31-2013',
    label: '2013',
  },
  {
    value: '31-31-2012',
    label: '2012',
  },
  {
    value: '31-31-2011',
    label: '2011',
  },
  {
    value: '31-31-2010',
    label: '2010',
  },
]

type Form = {
  text: string
  date: string
}

export function Account() {
  const navigate = useNavigate()

  const { username } = useParams()
  const [form, setForm] = React.useState({
    text: '',
    date: '',
    page: '',
  })

  const params = new URLSearchParams({
    page: '1',
    text: encodeURIComponent(form.text),
    end_date: form.date,
  })

  const { data: posts } = useSWR<Post[]>(
    `/api/posts/list/${username}?${params}`,
  )

  function handleChangeFormValue(payload: SetFormPayload<Form>) {
    setForm((prev) => ({
      ...prev,
      [payload.key]: payload.value,
    }))
  }

  function handleCardClick(postId: number) {
    navigate(`/posts/${postId}`)
  }

  return (
    <div className="w-full h-full flex flex-col gap-20">
      <div className="flex w-full max-w-sm m-auto items-center gap-2">
        <Input
          // className="min-w-[300px]"
          placeholder="text"
          value={form.text}
          onChange={(event) =>
            handleChangeFormValue({
              key: 'text',
              value: event.currentTarget.value,
            })
          }
        />
        <Select
          value={form.date}
          options={MOCK_DATES}
          onChange={(value) =>
            handleChangeFormValue({
              key: 'date',
              value,
            })
          }
        />
        <Button type="submit" variant="outline">
          Search
        </Button>
      </div>
      <div className="h-full max-h-full scroll-auto flex gap-5 flex-wrap">
        {posts?.map((post) => {
          return (
            <PostCard
              key={post.id}
              src={post.url}
              text={post.caption}
              createdDate={post.date_utc}
              onCardClick={() => handleCardClick(post.id)}
            />
          )
        })}
      </div>
    </div>
  )
}
