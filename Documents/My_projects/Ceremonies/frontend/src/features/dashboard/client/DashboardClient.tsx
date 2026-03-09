import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { 
  CalendarIcon, 
  UserGroupIcon, 
  CurrencyEuroIcon,
  ChatBubbleLeftRightIcon,
  HeartIcon,
  PlusIcon,
  ArrowRightIcon
} from '@heroicons/react/24/outline';
import { Container } from '../../../shared/components/ui/Container';
import { Card } from '../../../shared/components/ui/Card';
import { Button } from '../../../shared/components/ui/Button';
import { ceremoniesApi } from '../../../shared/api/ceremonies';
import type { Ceremony } from '../../../shared/api/ceremonies';
import { useAuth } from '../../../features/auth/hooks/useAuth';

// Données mockées temporaires pour les favoris (en attendant l'API)
const mockFavorites = [
  { id: 1, name: "Sophie Martin", category: "Photographe", image: "https://images.unsplash.com/photo-1494790108777-467efad0c2d0?w=100&auto=format" },
  { id: 2, name: "Traiteur Lyonnais", category: "Traiteur", image: "https://images.unsplash.com/photo-1566492031773-4f4e44671857?w=100&auto=format" },
];

export default function DashboardClient() {
  const { user } = useAuth();
  const [events, setEvents] = useState<Ceremony[]>([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalEvents: 0,
    totalBudget: 0,
    totalGuests: 0,
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const eventsRes = await ceremoniesApi.getAll();
        const eventsData = eventsRes.data;
        setEvents(eventsData);

        // Calcul des stats
        const totalEvents = eventsData.length;
        const totalBudget = eventsData.reduce((sum, e) => sum + (e.budget || 0), 0);
        const totalGuests = eventsData.reduce((sum, e) => sum + (e.guest_count || 0), 0);
        setStats({ totalEvents, totalBudget, totalGuests });
      } catch (error) {
        console.error('Erreur chargement événements', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-background pt-24 pb-16 flex justify-center">
        <div className="w-12 h-12 border-4 border-primary-200 border-t-primary-500 rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background pt-24 pb-16">
      <Container>
        {/* En-tête avec nom de l'utilisateur */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-text-primary mb-2">
              Bonjour, {user?.full_name?.split(' ')[0] || 'Utilisateur'} 👋
            </h1>
            <p className="text-text-secondary">
              Gérez vos événements et retrouvez vos prestataires favoris
            </p>
          </div>
          <Link to="/ceremonies/create">
            <Button variant="primary" className="flex items-center gap-2">
              <PlusIcon className="w-5 h-5" />
              Nouvel événement
            </Button>
          </Link>
        </div>

        {/* Stats rapides */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <Card className="p-4 text-center">
            <CalendarIcon className="w-8 h-8 text-primary-500 mx-auto mb-2" />
            <p className="text-2xl font-bold text-text-primary">{stats.totalEvents}</p>
            <p className="text-sm text-text-secondary">Événements</p>
          </Card>
          <Card className="p-4 text-center">
            <HeartIcon className="w-8 h-8 text-primary-500 mx-auto mb-2" />
            <p className="text-2xl font-bold text-text-primary">{mockFavorites.length}</p>
            <p className="text-sm text-text-secondary">Favoris</p>
          </Card>
          <Card className="p-4 text-center">
            <ChatBubbleLeftRightIcon className="w-8 h-8 text-primary-500 mx-auto mb-2" />
            <p className="text-2xl font-bold text-text-primary">3</p>
            <p className="text-sm text-text-secondary">Messages</p>
          </Card>
          <Card className="p-4 text-center">
            <CurrencyEuroIcon className="w-8 h-8 text-primary-500 mx-auto mb-2" />
            <p className="text-2xl font-bold text-text-primary">{stats.totalBudget}€</p>
            <p className="text-sm text-text-secondary">Budget total</p>
          </Card>
        </div>

        {/* Grille principale */}
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Liste des événements */}
          <div className="lg:col-span-2 space-y-4">
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-bold text-text-primary">Mes événements</h2>
              <Link to="/ceremonies" className="text-primary-500 text-sm flex items-center gap-1">
                Voir tout <ArrowRightIcon className="w-4 h-4" />
              </Link>
            </div>
            {events.length === 0 ? (
              <p className="text-text-secondary">Aucun événement pour le moment.</p>
            ) : (
              events.map((event) => (
                <Card key={event.id} className="p-6 hover:shadow-medium transition-all">
                  <div className="flex flex-wrap justify-between items-start gap-4">
                    <div>
                      <h3 className="font-semibold text-text-primary text-lg">{event.title}</h3>
                      <div className="flex flex-wrap gap-4 mt-2 text-sm text-text-secondary">
                        <span>📅 {new Date(event.event_date).toLocaleDateString('fr-FR')}</span>
                        <span>👥 {event.guest_count || 0} invités</span>
                        <span>💰 {event.budget || 0}€</span>
                        {/* Le nombre de prestataires n'est pas disponible ici, on pourrait le calculer via une autre API */}
                      </div>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                      event.status === 'planning' ? 'bg-gold-100 text-gold-600' : 'bg-primary-100 text-primary-600'
                    }`}>
                      {event.status === 'planning' ? 'Planification' : event.status}
                    </span>
                  </div>
                  <div className="mt-4 flex gap-3">
                    <Button variant="outline" size="sm">Gérer</Button>
                    <Button variant="ghost" size="sm">Voir détails</Button>
                  </div>
                </Card>
              ))
            )}
          </div>

          {/* Colonne de droite : favoris et suggestions */}
          <div className="space-y-6">
            {/* Favoris */}
            <Card className="p-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="font-bold text-text-primary">Prestataires favoris</h2>
                <Link to="/favorites" className="text-primary-500 text-sm">Voir tout</Link>
              </div>
              <div className="space-y-3">
                {mockFavorites.map((fav) => (
                  <div key={fav.id} className="flex items-center gap-3">
                    <img src={fav.image} alt={fav.name} className="w-10 h-10 rounded-full object-cover" />
                    <div>
                      <p className="font-medium text-text-primary">{fav.name}</p>
                      <p className="text-xs text-text-secondary">{fav.category}</p>
                    </div>
                  </div>
                ))}
              </div>
            </Card>

            {/* Suggestions intelligentes */}
            <Card className="p-6 bg-gradient-to-br from-primary-50 to-gold-50">
              <h2 className="font-bold text-text-primary mb-3">Suggestions pour vous</h2>
              <p className="text-sm text-text-secondary mb-4">
                D'après votre budget et vos préférences
              </p>
              <Button variant="primary" size="sm" fullWidth>
                Voir les suggestions
              </Button>
            </Card>
          </div>
        </div>
      </Container>
    </div>
  );
}