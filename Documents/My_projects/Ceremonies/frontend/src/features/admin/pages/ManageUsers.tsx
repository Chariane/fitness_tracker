import { useEffect, useState } from 'react';
import { Container } from '../../../shared/components/ui/Container';
import { Card } from '../../../shared/components/ui/Card';
import { Button } from '../../../shared/components/ui/Button';
import { adminApi } from '../../../shared/api/admin';
import type { User } from '../../../shared/api/users';
import { AdminSidebar } from '../components/AdminSidebar';

export default function ManageUsers() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      // Endpoint à créer dans le backend : /admin/users
      const res = await adminApi.getUsers(); // à définir dans adminApi
      setUsers(res.data);
    } catch (error) {
      console.error('Erreur chargement utilisateurs', error);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleActive = async (userId: number, currentActive: boolean) => {
    // Endpoint à créer : PATCH /admin/users/{id}/toggle-active
    try {
      await adminApi.toggleUserActive(userId, !currentActive);
      fetchUsers(); // rafraîchir
    } catch (error) {
      console.error('Erreur modification statut', error);
    }
  };

  if (loading) return <div className="text-center py-8">Chargement...</div>;

  return (
    <div className="flex">
      <AdminSidebar />
      <main className="flex-1 ml-64 p-8">
        <Container size="lg">
          <h1 className="text-3xl font-bold mb-6">Gestion des utilisateurs</h1>
          <div className="space-y-4">
            {users.map(user => (
              <Card key={user.id} className="p-6">
                <div className="flex justify-between items-center">
                  <div>
                    <p className="font-semibold">{user.full_name || 'Sans nom'}</p>
                    <p className="text-sm text-text-secondary">{user.email}</p>
                    <div className="flex gap-2 mt-2">
                      {user.is_client && <span className="px-2 py-1 bg-blue-100 text-blue-600 text-xs rounded">Client</span>}
                      {user.is_prestataire && <span className="px-2 py-1 bg-green-100 text-green-600 text-xs rounded">Prestataire</span>}
                      {user.is_admin && <span className="px-2 py-1 bg-purple-100 text-purple-600 text-xs rounded">Admin</span>}
                    </div>
                  </div>
                  <div className="flex items-center gap-4">
                    <span className={`text-sm ${user.is_active ? 'text-green-500' : 'text-red-500'}`}>
                      {user.is_active ? 'Actif' : 'Inactif'}
                    </span>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleToggleActive(user.id, user.is_active)}
                    >
                      {user.is_active ? 'Désactiver' : 'Activer'}
                    </Button>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </Container>
      </main>
    </div>
  );
}