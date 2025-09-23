import { useState, useEffect } from 'react'

export function useSSE<T>(url: string, isStart: boolean = true) {
  const [data, setData] = useState<T[]>([])

  useEffect(() => {
    if (!isStart) return
    const eventSource = new EventSource(url)

    eventSource.onmessage = (event) => {
      const newData = JSON.parse(event.data) as T
      setData((prev) => [...prev, newData])
    }

    return () => {
      eventSource.close()
    }
  }, [url, isStart])

  return data
}
