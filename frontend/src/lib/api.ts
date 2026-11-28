/** Small fetch wrapper for the Momentum API. Paths are relative (e.g. "/api/goals");
 *  in development Vite proxies them to FastAPI. */

export class ApiError extends Error {
  readonly status: number
  readonly detail: unknown

  constructor(status: number, detail: unknown) {
    super(typeof detail === 'string' ? detail : `Request failed (${status})`)
    this.status = status
    this.detail = detail
  }
}

export async function api<T>(path: string, init: RequestInit = {}): Promise<T> {
  const response = await fetch(path, {
    ...init,
    headers: { 'Content-Type': 'application/json', ...init.headers },
  })

  const body = response.headers.get('content-type')?.includes('application/json')
    ? await response.json()
    : null

  if (!response.ok) throw new ApiError(response.status, body?.detail ?? body)
  return body as T
}

export type Health = { status: 'ok' | 'degraded'; database: 'ok' | 'unavailable' }
