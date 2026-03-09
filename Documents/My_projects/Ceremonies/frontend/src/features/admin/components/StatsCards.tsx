import { Card } from '../../../shared/components/ui/Card';
import type { AdminStats } from '../../../shared/api/admin';

interface StatsCardsProps {
  stats: AdminStats;
}

export function StatsCards({ stats }: StatsCardsProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
      <Card className="p-4 text-center">
        <p className="text-2xl font-bold text-primary-500">{stats.totalUsers}</p>
        <p className="text-sm text-text-secondary">Utilisateurs</p>
      </Card>
      <Card className="p-4 text-center">
        <p className="text-2xl font-bold text-primary-500">{stats.totalClients}</p>
        <p className="text-sm text-text-secondary">Clients</p>
      </Card>
      <Card className="p-4 text-center">
        <p className="text-2xl font-bold text-primary-500">{stats.totalPrestataires}</p>
        <p className="text-sm text-text-secondary">Prestataires</p>
      </Card>
      <Card className="p-4 text-center">
        <p className="text-2xl font-bold text-amber-500">{stats.pendingVerifications}</p>
        <p className="text-sm text-text-secondary">En attente</p>
      </Card>
      <Card className="p-4 text-center">
        <p className="text-2xl font-bold text-primary-500">{stats.totalCeremonies}</p>
        <p className="text-sm text-text-secondary">Événements</p>
      </Card>
    </div>
  );
}