import { MutationCache, QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router'
import { Toaster } from 'sonner'

import App from '@/App'
import { ApiError } from '@/lib/api'
import { notify } from '@/lib/notify'
import '@/index.css'

declare module '@tanstack/react-query' {
  interface Register {
    // A mutation can set meta: { silent: true } when it shows its own error UI
    mutationMeta: { silent?: boolean }
  }
}

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30_000,
      refetchOnWindowFocus: true,
      // 4xx answers (e.g. 404 "no plan yet") won't change on retry, so show them right away
      retry: (failureCount, error) =>
        !(error instanceof ApiError && error.status < 500) && failureCount < 2,
    },
  },
  // Every failed save gets a toast, so no error is ever silent
  mutationCache: new MutationCache({
    onError: (error, _vars, _ctx, mutation) => {
      if (!mutation.meta?.silent) notify.error(error)
    },
  }),
})

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
      {/* On phones, sit above the bottom tab bar instead of covering it */}
      <Toaster
        position="bottom-center"
        mobileOffset={{ bottom: 'calc(5rem + env(safe-area-inset-bottom))' }}
      />
    </QueryClientProvider>
  </StrictMode>,
)
