import { BrowserRouter } from 'react-router'
import { Routes } from './routes'
import { ThemeProvider } from './components/providers'

export function App() {
  return (
    <BrowserRouter>
      <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
        <Routes />
      </ThemeProvider>
    </BrowserRouter>
  )
}
