export type SetFormPayload<T extends object> = {
  [K in keyof T]: { key: K; value: T[K] }
}[keyof T]
