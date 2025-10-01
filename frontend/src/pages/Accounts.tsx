import { AccountCard } from '@/components/common/AccountCard'
import { Input } from '@/components/ui-shadcn/input'
import { fetcher } from '@/lib/utils'
import React from 'react'
import { useNavigate } from 'react-router'
import useSWR from 'swr'

// const DATA = [
//   { totalposts: 124, username: 'nfuasdi', id: 234 },
//   { totalposts: 12341234, username: 'nfuasdisadfsadf', id: 2341 },
//   { totalposts: 12341234, username: 'asdf', id: 23411 },
//   { totalposts: 12341234, username: 'nfuasdisadfsadf', id: 23412 },
//   { totalposts: 12341234, username: 'nfuasdisadfsadf', id: 23413 },
//   { totalposts: 12341234, username: 'erqw', id: 23414 },
//   { totalposts: 12341234, username: 'sm', id: 23415 },
// ]

type Account = {
  totalposts: number
  username: string
  id: number
}

export function Accounts() {
  const navigate = useNavigate()
  const [searchText, setSearchText] = React.useState('')

  const { data: accounts } = useSWR<Account[]>('/api/accounts', fetcher)

  const displayAccounts = React.useMemo(() => {
    const lowerSearchText = searchText.toLocaleLowerCase()
    return (accounts ?? []).filter((account) =>
      account.username.toLocaleLowerCase().includes(lowerSearchText),
    )
  }, [searchText, accounts])

  return (
    <div className="w-full h-full flex flex-col gap-20">
      <Input
        className="w-[40%] m-auto"
        placeholder="search by username"
        value={searchText}
        onChange={(event) => setSearchText(event.currentTarget.value)}
      />
      <div className="h-full min-h-0 max-h-full flex-1 overflow-auto pb-10 flex gap-10 flex-wrap">
        {displayAccounts.map((account) => {
          return (
            <AccountCard
              key={account.id}
              id={account.id}
              totalCount={account.totalposts}
              name={account.username}
              onCardClick={() => navigate(`/accounts/${account.username}`)}
            />
          )
        })}
      </div>
    </div>
  )
}
