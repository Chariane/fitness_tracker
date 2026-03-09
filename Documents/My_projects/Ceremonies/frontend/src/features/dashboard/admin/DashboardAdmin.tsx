import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Container } from '../../../shared/components/ui/Container';
import { Card } from '../../../shared/components/ui/Card';
import { adminApi } from '../../../shared/api/admin';
import type { AdminStats } from '../../../shared/api/admin';

export default function DashboardAdmin() {
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await adminApi.getDashboardStats();
        setStats(response.data);
      } catch (error) {
        console.error('Erreur chargement statistiques', error);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-background pt-24 flex justify-center">
        <div className="w-12 h-12 border-4 border-primary-200 border-t-primary-500 rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <Container className="py-8">
      <h1 className="text-3xl font-bold mb-8">Dashboard Administrateur</h1>

      {/* Statistiques */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
        <Card className="p-4 text-center">
          <p className="text-2xl font-bold text-primary-500">{stats?.totalUsers}</p>
          <p className="text-sm text-text-secondary">Utilisateurs</p>
        </Card>
        <Card className="p-4 text-center">
          <p className="text-2xl font-bold text-primary-500">{stats?.totalClients}</p>
          <p className="text-sm text-text-secondary">Clients</p>
        </Card>
        <Card className="p-4 text-center">
          <p className="text-2xl font-bold text-primary-500">{stats?.totalPrestataires}</p>
          <p className="text-sm text-text-secondary">Prestataires</p>
        </Card>
        <Card className="p-4 text-center">
          <p className="text-2xl font-bold text-amber-500">{stats?.pendingVerifications}</p>
          <p className="text-sm text-text-secondary">En attente</p>
        </Card>
        <Card className="p-4 text-center">
          <p className="text-2xl font-bold text-primary-500">{stats?.totalCeremonies}</p>
          <p className="text-sm text-text-secondary">Événements</p>
        </Card>
      </div>

      {/* Actions rapides */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <Link to="/admin/verification">
          <Card className="p-6 hover:shadow-medium transition-all cursor-pointer">
            <h3 className="font-semibold text-lg mb-2">Vérifications</h3>
            <p className="text-sm text-text-secondary mb-4">Prestataires en attente</p>
            <span className="text-primary-500 text-sm">Voir →</span>
          </Card>
        </Link>
        <Link to="/admin/ceremony-types">
          <Card className="p-6 hover:shadow-medium transition-all cursor-pointer">
            <h3 className="font-semibold text-lg mb-2">Types d'événements</h3>
            <p className="text-sm text-text-secondary mb-4">Gérer les types</p>
            <span className="text-primary-500 text-sm">Voir →</span>
          </Card>
        </Link>
        <Link to="/admin/service-categories">
          <Card className="p-6 hover:shadow-medium transition-all cursor-pointer">
            <h3 className="font-semibold text-lg mb-2">Catégories de services</h3>
            <p className="text-sm text-text-secondary mb-4">Gérer les catégories</p>
            <span className="text-primary-500 text-sm">Voir →</span>
          </Card>
        </Link>
        <Link to="/admin/users">
          <Card className="p-6 hover:shadow-medium transition-all cursor-pointer">
            <h3 className="font-semibold text-lg mb-2">Utilisateurs</h3>
            <p className="text-sm text-text-secondary mb-4">Gérer les comptes</p>
            <span className="text-primary-500 text-sm">Voir →</span>
          </Card>
        </Link>
      </div>
    </Container>
  );
}