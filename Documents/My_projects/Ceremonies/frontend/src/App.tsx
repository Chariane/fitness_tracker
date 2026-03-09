import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Header } from './shared/components/layout/Header';
import { Footer } from './shared/components/layout/Footer';
import { ProtectedRoute } from './shared/components/ProtectedRoute';
import Home from './features/landing/pages/Home';
import PrestataireSearch from './features/prestataires/pages/PrestataireSearch';
import PrestataireProfile from './features/prestataires/pages/PrestataireProfile';
import LoginPage from './features/auth/pages/Login';
import RegisterPage from './features/auth/pages/Register';
import BecomePrestatairePage from './features/auth/pages/BecomePrestataire';
import DashboardClient from './features/dashboard/client/DashboardClient';
import DashboardPrestataire from './features/dashboard/prestataire/DashboardPrestataire';
import DashboardAdmin from './features/admin/pages/DashboardAdmin';
import ManageCeremonyTypes from './features/admin/pages/ManageCeremonyTypes';
import ManageServiceCategories from './features/admin/pages/ManageServiceCategories';
import PendingPrestataires from './features/admin/pages/PendingPrestataires';
import ModerateReviews from './features/admin/pages/ModerateReviews';
import ManageUsers from './features/admin/pages/ManageUsers';
import MessagesPage from './features/messaging/pages/Messages';
import PendingApprovalPage from './features/auth/pages/PendingApproval';
import ManageOffers from './features/prestataires/pages/ManageOffers';
import CreateOffer from './features/prestataires/pages/CreateOffer';
import EditOffer from './features/prestataires/pages/EditOffer';
import EditProfile from './features/profile/pages/EditProfile';
import EditPrestataireProfile from './features/profile/pages/EditPrestataireProfile';
import OfferDetails from './features/offers/pages/OfferDetails';
import OfferMarketplace from './features/offers/pages/OfferMarketPlace';
import EventBuilder from './features/ceremonies/pages/EventBuilder'; // ou MyCeremonies selon le nom final
import PackRecommendations from './features/recommendations/pages/PackRecommendations';
import EventPackBuilder from './features/offers/pages/EventPackBuilder.tsx'
// Import de la page
import Favorites from './features/prestataires/pages/Favorites';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-background flex flex-col">
        <Header />
        <main className="flex-1 pt-20">
          <Routes>
            {/* Routes publiques */}
            <Route path="/" element={<Home />} />
            <Route path="/search" element={<PrestataireSearch />} />
            <Route path="/prestataire/:id" element={<PrestataireProfile />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/offers/:id" element={<OfferDetails />} />
            <Route path="/marketplace" element={<OfferMarketplace />} />

            {/* Dans les routes protégées pour tous les utilisateurs connectés*/}
            <Route element={<ProtectedRoute />}>
              <Route path="/become-prestataire" element={<BecomePrestatairePage />} />
              <Route path="/pending-approval" element={<PendingApprovalPage />} />
              <Route path="/messages" element={<MessagesPage />} />
              <Route path="/messages/:id" element={<MessagesPage />} />
              <Route path="/profile/edit" element={<EditProfile />} />  
              <Route path="/event-builder" element={<EventBuilder />} />
              <Route path="/pack-recommendations" element={<PackRecommendations />} />
              <Route path="/event-pack-builder" element={<EventPackBuilder />} />
              <Route path="/favorites" element={<Favorites />} />
            </Route>

            {/* Routes pour clients */}
            <Route element={<ProtectedRoute allowedRoles={['client']} />}>
              <Route path="/dashboard" element={<DashboardClient />} />
            </Route>

            {/* Routes pour prestataires */}
            <Route element={<ProtectedRoute allowedRoles={['prestataire']} />}>
              <Route path="/prestataire/dashboard" element={<DashboardPrestataire />} />
              <Route path="/offers" element={<ManageOffers />} />
              <Route path="/offers/create" element={<CreateOffer />} />
              <Route path="/offers/edit/:id" element={<EditOffer />} />
              <Route path="/prestataire/profile/edit" element={<EditPrestataireProfile />} />
            </Route>

            {/* Routes pour admin */}
            <Route element={<ProtectedRoute allowedRoles={['admin']} />}>
              <Route path="/admin" element={<DashboardAdmin />} />
              <Route path="/admin/ceremony-types" element={<ManageCeremonyTypes />} />
              <Route path="/admin/service-categories" element={<ManageServiceCategories />} />
              <Route path="/admin/verification" element={<PendingPrestataires />} />
              <Route path="/admin/reviews" element={<ModerateReviews />} />
              <Route path="/admin/users" element={<ManageUsers />} />
            </Route>
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;