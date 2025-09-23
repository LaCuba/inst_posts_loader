import { UserSearch } from 'lucide-react'

export type Props = {
  id: number
  src?: string
  name: string
  totalCount: number
  onCardClick?: () => void
}

export function AccountCard(props: Props) {
  return (
    <div
      onClick={props.onCardClick}
      className="w-[200px] h-[300px] flex flex-col bg-card border rounded-2xl cursor-pointer"
    >
      {props.src ? (
        <img
          src={props.src}
          alt=""
          className="w-full h-[200px] rounded-t-2xl"
        />
      ) : (
        <div className="w-full h-[200px] flex items-center justify-center">
          <UserSearch size={80} />
        </div>
      )}
      <div className="flex flex-col gap-2 py-2 px-4">
        <div className="text-2xl">{props.name}</div>
        <div className="text-sm">posts: {props.totalCount}</div>
      </div>
    </div>
  )
}
