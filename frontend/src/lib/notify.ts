import { toast } from 'sonner'

import { errorMessage } from '@/lib/errors'

/** One place for toasts, so wording and timing stay consistent across the app. */
export const notify = {
  success(message: string) {
    toast.success(message)
  },

  error(error: unknown, fallback?: string) {
    toast.error(fallback ?? errorMessage(error))
  },

  /** For reversible actions (check-ins, archiving): say what happened and offer Undo. */
  undoable(message: string, onUndo: () => void) {
    toast(message, { action: { label: 'Undo', onClick: onUndo }, duration: 6000 })
  },
}
