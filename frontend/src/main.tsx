import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router'
import { Toaster } from 'sonner'

import App from '@/App'
import '@/index.css'
import { followSystemTheme } from '@/lib/theme'

followSystemTheme()

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { staleTime: 30_000, refetchOnWindowFocus: true },
  },
})

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
      <Toaster position="bottom-center" richColors theme="system" />
    </QueryClientProvider>
  </StrictMode>,
)
