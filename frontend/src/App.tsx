import { Route, Routes } from 'react-router'

import { AppLayout } from '@/components/AppLayout'
import { NowPage } from '@/pages/NowPage'
import { PlaceholderPage } from '@/pages/PlaceholderPage'

export default function App() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route index element={<NowPage />} />
        <Route path="today" element={<PlaceholderPage title="Today" comingOn="Dec 6" />} />
        <Route path="goals" element={<PlaceholderPage title="Goals" comingOn="Dec 5" />} />
        <Route path="progress" element={<PlaceholderPage title="Progress" comingOn="Dec 24" />} />
        <Route path="*" element={<PlaceholderPage title="Not found" comingOn="never" />} />
      </Route>
    </Routes>
  )
}
