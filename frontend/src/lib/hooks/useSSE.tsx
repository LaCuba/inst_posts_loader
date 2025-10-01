import React from 'react'

export function useSSE<T>(url: string, isStart: boolean = true) {
  const [data, setData] = React.useState<T[]>([])
  const [error, setError] = React.useState<string>()

  React.useEffect(() => {
    if (!isStart) return
    const eventSource = new EventSource(url)

    eventSource.onmessage = (event) => {
      const newData = JSON.parse(event.data) as T
      setData((prev) => [...prev, newData])
    }

    eventSource.onerror = (event) => {
      debugger
      try {
        const data = JSON.parse((event as MessageEvent).data)
        console.error('App error from server:', data.message)
        setError(data.message)
      } catch {
        console.error('SSE error (connection closed or invalid JSON)')
        setError('Error executed')
      }
      eventSource.close()
    }

    return () => {
      eventSource.close()
    }
  }, [url, isStart])

  return { data, error }
}
