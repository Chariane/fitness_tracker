import { Link } from 'react-router-dom';
import { 
  EyeIcon,
  ChatBubbleLeftRightIcon,
  CurrencyEuroIcon,
  CheckCircleIcon,
  PlusIcon,
  ArrowRightIcon,
  PencilIcon
} from '@heroicons/react/24/outline';
import { Container } from '../../../shared/components/ui/Container';
import { Card } from '../../../shared/components/ui/Card';
import { Button } from '../../../shared/components/ui/Button';
import { usePrestataireDashboard } from '../../../features/prestataires/hooks/usePrestataireDashboard';

export default function DashboardPrestataire() {
  const { offers, requests, stats, loading } = usePrestataireDashboard();

  if (loading) {
    return (
      <div className="min-h-screen bg-background pt-24 flex justify-center">
        <div className="w-12 h-12 border-4 border-primary-200 border-t-primary-500 rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background pt-24 pb-16">
      <Container>
        {/* En-tête */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-text-primary mb-2">
              Bonjour 👋
            </h1>
            <p className="text-text-secondary">
              Gérez vos prestations et vos demandes de clients
            </p>
          </div>
          <Link to="/offers/create">
            <Button variant="primary" className="flex items-center gap-2">
              <PlusIcon className="w-5 h-5" />
              Nouvelle offre
            </Button>
          </Link>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <Card className="p-4 text-center">
            <EyeIcon className="w-8 h-8 text-primary-500 mx-auto mb-2" />
            <p className="text-2xl font-bold text-text-primary">{stats.totalViews}</p>
            <p className="text-sm text-text-secondary">Vues totales</p>
          </Card>
          <Card className="p-4 text-center">
            <ChatBubbleLeftRightIcon className="w-8 h-8 text-primary-500 mx-auto mb-2" />
            <p className="text-2xl font-bold text-text-primary">{stats.totalContacts}</p>
            <p className="text-sm text-text-secondary">Contacts</p>
          </Card>
          <Card className="p-4 text-center">
            <CurrencyEuroIcon className="w-8 h-8 text-primary-500 mx-auto mb-2" />
            <p className="text-2xl font-bold text-text-primary">{stats.totalReservations}</p>
            <p className="text-sm text-text-secondary">Réservations</p>
          </Card>
          <Card className="p-4 text-center">
            <CheckCircleIcon className="w-8 h-8 text-primary-500 mx-auto mb-2" />
            <p className="text-2xl font-bold text-text-primary">{stats.averageRating}</p>
            <p className="text-sm text-text-secondary">Note moyenne</p>
          </Card>
        </div>

        {/* Grille principale */}
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Demandes récentes */}
          <div className="lg:col-span-2 space-y-4">
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-bold text-text-primary">Demandes récentes</h2>
              <Link to="/requests" className="text-primary-500 text-sm flex items-center gap-1">
                Voir tout <ArrowRightIcon className="w-4 h-4" />
              </Link>
            </div>
            {requests.length === 0 ? (
              <p className="text-text-secondary">Aucune demande pour le moment.</p>
            ) : (
              requests.map((req) => (
                <Card key={req.id} className="p-6 hover:shadow-medium transition-all">
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-semibold text-text-primary">{req.client}</h3>
                      <p className="text-sm text-text-secondary mt-1">{req.event}</p>
                      <p className="text-text-secondary mt-2">"{req.message}"</p>
                    </div>
                    <span className="text-xs text-text-tertiary">{req.date}</span>
                  </div>
                  <div className="mt-4 flex gap-3">
                    <Link to={`/messages?conversation=${req.id}`}>
                      <Button variant="primary" size="sm">Répondre</Button>
                    </Link>
                    <Button variant="outline" size="sm">Voir détails</Button>
                  </div>
                </Card>
              ))
            )}
          </div>

          {/* Colonne de droite : offres et profil */}
          <div className="space-y-6">
            {/* Aperçu des offres */}
            <Card className="p-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="font-bold text-text-primary">Mes offres</h2>
                <Link to="/offers" className="text-primary-500 text-sm">Gérer</Link>
              </div>
              <div className="space-y-3">
                {offers.length === 0 ? (
                  <p className="text-text-secondary text-sm">Aucune offre pour le moment.</p>
                ) : (
                  offers.slice(0, 3).map((offer) => (
                    <div key={offer.id} className="flex justify-between items-center">
                      <div>
                        <p className="font-medium text-text-primary">{offer.title}</p>
                        <p className="text-xs text-text-secondary">
                          {offer.views || 0} vues • {offer.contacts || 0} contacts
                        </p>
                      </div>
                      <Link to={`/offers/edit/${offer.id}`}>
                        <PencilIcon className="w-4 h-4 text-text-tertiary hover:text-primary-500" />
                      </Link>
                    </div>
                  ))
                )}
              </div>
            </Card>

            {/* Compléter le profil */}
            <Card className="p-6 bg-gradient-to-br from-primary-50 to-gold-50">
              <h2 className="font-bold text-text-primary mb-2">Profil à 70%</h2>
              <p className="text-sm text-text-secondary mb-4">
                Ajoutez des photos pour augmenter votre visibilité
              </p>
              <Link to="/prestataire/profile/edit">
                <Button variant="primary" size="sm" fullWidth>
                  Compléter mon profil
                </Button>
              </Link>
            </Card>
          </div>
        </div>
      </Container>
    </div>
  );
}