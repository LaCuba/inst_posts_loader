import { Header } from '@/components/common/Header'
import { Outlet } from 'react-router'

export function Root() {
  return (
    <div className="w-full h-full flex flex-col gap-25">
      <Header />
      <div className="w-full max-w-[1280px] h-full min-h-0 flex-1 m-auto">
        <Outlet />
      </div>
    </div>
  )
}
