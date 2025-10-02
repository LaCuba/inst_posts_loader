export type SetFormPayload<T extends object> = {
  [K in keyof T]: { key: K; value: T[K] }
}[keyof T]

export type Post = {
  id: number
  account_id: number
  date_utc: string
  caption: string
  likes: number
  url: string
  video_url: string
  typename: string
  username?: string
}
