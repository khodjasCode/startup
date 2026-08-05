import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'

import { CategoriesPage } from '@pages/categories/CategoriesPage'
import { ContactPage } from '@pages/contact/ContactPage'
import { DatabasesPage } from '@pages/databases/DatabasesPage'
import { FaqPage } from '@pages/faq/FaqPage'
import { HomePage } from '@pages/home/HomePage'
import { LoginPage } from '@pages/login/LoginPage'
import { ServicePage } from '@pages/services/ServicePage'
import { ServicesPage } from '@pages/services/ServicesPage'
import { SourcesPage } from '@pages/sources/SourcesPage'

import { AppLayout } from './layout/AppLayout'
import { AppProviders } from './providers/AppProviders'
import { ROUTES } from './routes'

export function App() {
  return (
    <BrowserRouter>
      <AppProviders>
        <Routes>
          <Route element={<AppLayout />}>
            <Route path={ROUTES.home} element={<HomePage />} />
            <Route path={ROUTES.categories} element={<CategoriesPage />} />
            <Route path={ROUTES.services} element={<ServicesPage />} />
            <Route path={ROUTES.service} element={<ServicePage />} />
            <Route path={ROUTES.databases} element={<DatabasesPage />} />
            <Route path={ROUTES.sources} element={<SourcesPage />} />
            <Route path={ROUTES.faq} element={<FaqPage />} />
            <Route path={ROUTES.contact} element={<ContactPage />} />
            <Route path={ROUTES.login} element={<LoginPage />} />
            {/* Noma'lum yo'l — bosh sahifaga. */}
            <Route path="*" element={<Navigate to={ROUTES.home} replace />} />
          </Route>
        </Routes>
      </AppProviders>
    </BrowserRouter>
  )
}
