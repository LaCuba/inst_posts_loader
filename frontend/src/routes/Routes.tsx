import { layouts } from '@/layouts'
import { Account } from '@/pages/Account'
import { Accounts } from '@/pages/Accounts'
import { DownloadPost } from '@/pages/DownloadPost'
import { Main } from '@/pages/Main'
import { Post } from '@/pages/Post'
import { Route, Routes as RouterRoutes } from 'react-router'

export function Routes() {
  return (
    <RouterRoutes>
      <Route path="/" element={<layouts.Root />}>
        <Route index element={<Main />} />
        <Route path="accounts" element={<Accounts />} />
        <Route path="accounts/:username" element={<Account />} />
        <Route path="posts/:postId" element={<Post />} />
        <Route path="download_post" element={<DownloadPost />} />
      </Route>
    </RouterRoutes>
  )
}
