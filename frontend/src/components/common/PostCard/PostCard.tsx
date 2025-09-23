import { Signpost } from 'lucide-react'

export type Props = {
  src?: string
  text: string
  onCardClick?: () => void
}

export function PostCard(props: Props) {
  return (
    <div
      onClick={props.onCardClick}
      className="w-[300px] h-[450px] flex flex-col bg-card border rounded-2xl cursor-pointer"
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
      <div className="flex flex-col gap-2 py-2 px-4">
        <div className="text-lg">{props.text}</div>
      </div>
    </div>
  )
}
