import { useEffect, useState } from 'react';
import { Container } from '../../../shared/components/ui/Container';
import { Card } from '../../../shared/components/ui/Card';
import { Button } from '../../../shared/components/ui/Button';
import { Input } from '../../../shared/components/ui/Input';
import { serviceCategoriesApi } from '../../../shared/api/serviceCategories';
import type { ServiceCategory } from '../../../shared/api/serviceCategories';
import { AdminSidebar } from '../components/AdminSidebar';

export default function ManageServiceCategories() {
  const [categories, setCategories] = useState<ServiceCategory[]>([]);
  const [loading, setLoading] = useState(true);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [formData, setFormData] = useState({ name: '' });

  useEffect(() => {
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    try {
      const res = await serviceCategoriesApi.getAll();
      setCategories(res.data);
    } catch (error) {
      console.error('Erreur chargement catégories', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingId) {
        await serviceCategoriesApi.update(editingId, formData);
      } else {
        await serviceCategoriesApi.create(formData);
      }
      setFormData({ name: '' });
      setEditingId(null);
      fetchCategories();
    } catch (error) {
      console.error('Erreur sauvegarde', error);
    }
  };

  const handleEdit = (cat: ServiceCategory) => {
    setEditingId(cat.id);
    setFormData({ name: cat.name });
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Supprimer cette catégorie ?')) {
      try {
        await serviceCategoriesApi.delete(id);
        fetchCategories();
      } catch (error) {
        console.error('Erreur suppression', error);
      }
    }
  };

  if (loading) return <div className="text-center py-8">Chargement...</div>;

  return (
    <div className="flex">
      <AdminSidebar />
      <main className="flex-1 ml-64 p-8">
        <Container size="md">
          <h1 className="text-3xl font-bold mb-6">Gérer les catégories de services</h1>
          
          <Card className="p-6 mb-8">
            <form onSubmit={handleSubmit} className="space-y-4">
              <Input
                placeholder="Nom de la catégorie (ex: Photographe)"
                value={formData.name}
                onChange={(e) => setFormData({ name: e.target.value })}
                required
              />
              <div className="flex gap-3">
                <Button type="submit" variant="primary">
                  {editingId ? 'Mettre à jour' : 'Ajouter'}
                </Button>
                {editingId && (
                  <Button type="button" variant="outline" onClick={() => {
                    setEditingId(null);
                    setFormData({ name: '' });
                  }}>
                    Annuler
                  </Button>
                )}
              </div>
            </form>
          </Card>

          <div className="space-y-3">
            {categories.map(cat => (
              <Card key={cat.id} className="p-4 flex justify-between items-center">
                <div>
                  <h3 className="font-semibold">{cat.name}</h3>
                </div>
                <div className="flex gap-2">
                  <Button variant="outline" size="sm" onClick={() => handleEdit(cat)}>
                    Modifier
                  </Button>
                  <Button variant="ghost" size="sm" onClick={() => handleDelete(cat.id)}>
                    Supprimer
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        </Container>
      </main>
    </div>
  );
}