import { Header } from '@/components/common/Header'
import { Outlet } from 'react-router'

export function Root() {
  return (
    <div className="w-full h-full flex flex-col gap-5">
      <Header />
      <div className="w-full max-w-[1280px] h-full m-auto">
        <Outlet />
      </div>
    </div>
  )
}
