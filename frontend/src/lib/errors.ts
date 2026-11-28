import { ApiError } from '@/lib/api'

/** True when the API answered 404, i.e. the thing simply doesn't exist yet. */
export function isNotFound(error: unknown): boolean {
  return error instanceof ApiError && error.status === 404
}

/** A short, human sentence for any error. Never blames the user, never shows a stack trace. */
export function errorMessage(error: unknown): string {
  if (error instanceof ApiError) {
    if (error.status >= 500) return 'Something went wrong on our side. Try again in a moment.'
    if (error.status === 409) return typeof error.detail === 'string' ? error.detail : 'That changed somewhere else. Refresh and try again.'
    if (error.status === 422) return validationMessage(error.detail)
    if (typeof error.detail === 'string') return error.detail
    return `Request failed (${error.status}).`
  }
  // fetch() throws a TypeError when the server can't be reached at all
  if (error instanceof TypeError) return "Can't reach Momentum. Check your connection."
  return 'Something unexpected happened.'
}

/** FastAPI 422 bodies are a list of { loc, msg }. Show the first one readably. */
function validationMessage(detail: unknown): string {
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail) && detail.length > 0) {
    const { loc, msg } = detail[0] as { loc?: unknown[]; msg?: string }
    const field = loc?.filter((part) => part !== 'body').join('.')
    const text = (msg ?? 'Invalid value').replace(/^Value error, /, '')
    return field ? `${field}: ${text}` : text
  }
  return 'Some of the details aren’t valid.'
}
