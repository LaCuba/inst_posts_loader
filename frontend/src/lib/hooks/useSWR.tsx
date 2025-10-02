import useSWRlib from 'swr'

export type ReturnParams<T> = {
  data: T
  isLoading: boolean
  error: Error
}

export const fetcher = (...args: Parameters<typeof fetch>) =>
  fetch(...args).then((res) => res.json())

export function useSWR<T>(...params: Partial<Parameters<typeof useSWRlib>>) {
  return useSWRlib(
    params?.[0],
    params?.[1] ?? fetcher,
    (params?.[2] as unknown) ?? {
      revalidateOnFocus: false,
      revalidateOnReconnect: false,
      revalidateIfStale: false,
    },
  ) as ReturnParams<T>
}
