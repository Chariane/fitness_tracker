import { useEffect, useState } from 'react';
import { Container } from '../../../shared/components/ui/Container';
import { Card } from '../../../shared/components/ui/Card';
import { Button } from '../../../shared/components/ui/Button';
import { Input } from '../../../shared/components/ui/Input';
import { ceremonyTypesApi } from '../../../shared/api/ceremonyTypes';
import type { CeremonyType } from '../../../shared/api/ceremonyTypes';

export default function ManageCeremonyTypes() {
  const [types, setTypes] = useState<CeremonyType[]>([]);
  const [loading, setLoading] = useState(true);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [formData, setFormData] = useState({ name: '', description: '' });

  useEffect(() => {
    fetchTypes();
  }, []);

  const fetchTypes = async () => {
    try {
      const res = await ceremonyTypesApi.getAll();
      setTypes(res.data);
    } catch (error) {
      console.error('Erreur chargement types', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingId) {
        await ceremonyTypesApi.update(editingId, formData);
      } else {
        await ceremonyTypesApi.create(formData);
      }
      setFormData({ name: '', description: '' });
      setEditingId(null);
      fetchTypes();
    } catch (error) {
      console.error('Erreur sauvegarde', error);
    }
  };

  const handleEdit = (type: CeremonyType) => {
    setEditingId(type.id);
    setFormData({ name: type.name, description: type.description || '' });
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Supprimer ce type ?')) {
      try {
        await ceremonyTypesApi.delete(id);
        fetchTypes();
      } catch (error) {
        console.error('Erreur suppression', error);
      }
    }
  };

  if (loading) return <div className="text-center py-8">Chargement...</div>;

  return (
    <Container size="md" className="py-8">
      <h1 className="text-3xl font-bold mb-6">Gérer les types d'événements</h1>
      
      <Card className="p-6 mb-8">
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            placeholder="Nom du type (ex: Mariage)"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            required
          />
          <Input
            placeholder="Description (optionnelle)"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
          />
          <div className="flex gap-3">
            <Button type="submit" variant="primary">
              {editingId ? 'Mettre à jour' : 'Ajouter'}
            </Button>
            {editingId && (
              <Button type="button" variant="outline" onClick={() => {
                setEditingId(null);
                setFormData({ name: '', description: '' });
              }}>
                Annuler
              </Button>
            )}
          </div>
        </form>
      </Card>

      <div className="space-y-3">
        {types.map(type => (
          <Card key={type.id} className="p-4 flex justify-between items-center">
            <div>
              <h3 className="font-semibold">{type.name}</h3>
              {type.description && <p className="text-sm text-text-secondary">{type.description}</p>}
            </div>
            <div className="flex gap-2">
              <Button variant="outline" size="sm" onClick={() => handleEdit(type)}>
                Modifier
              </Button>
              <Button variant="ghost" size="sm" onClick={() => handleDelete(type.id)}>
                Supprimer
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </Container>
  );
}