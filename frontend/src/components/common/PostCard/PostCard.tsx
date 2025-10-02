import { Signpost } from 'lucide-react'

export type Props = {
  src?: string
  text: string
  createdDate?: string
  onCardClick?: () => void
}

export function PostCard(props: Props) {
  return (
    <div
      onClick={props.onCardClick}
      className="w-[300px] h-[450px] max-h-[450px] flex flex-col bg-card border rounded-2xl cursor-pointer"
    >
      {props.src ? (
        <img
          src={props.src}
          alt=""
          className="w-full h-[300px] rounded-t-2xl"
        />
      ) : (
        <div className="w-full h-[300px] flex items-center justify-center">
          <Signpost size={80} />
        </div>
      )}
      <div className="max-h-full flex flex-1 min-h-0 flex-col gap-2 py-2 px-4">
        <div className="max-h-full text-sm line-clamp-5">{props.text}</div>
      </div>
      <div className="pb-1 pl-3 flex gap-10 justify-between">
        <div className="text-sm text-gray-500">
          {!!props.createdDate &&
            new Date(props.createdDate).toLocaleDateString('en-GB')}
        </div>
      </div>
    </div>
  )
}
