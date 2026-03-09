import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Container } from '../../../shared/components/ui/Container';
import { Card } from '../../../shared/components/ui/Card';
import { Button } from '../../../shared/components/ui/Button';
import { Input } from '../../../shared/components/ui/Input';
import { ceremoniesApi } from '../../../shared/api/ceremonies';
import type { CreateCeremonyData } from '../../../shared/api/ceremonies';
import { ceremonyTypesApi } from '../../../shared/api/ceremonyTypes';
import type { CeremonyType } from '../../../shared/api/ceremonyTypes';

export default function CreateCeremony() {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [types, setTypes] = useState<CeremonyType[]>([]);
  const [formData, setFormData] = useState({
    ceremony_type_id: '',
    title: '',
    event_date: '',
    location: '',
    budget: '',
    guest_count: '',
  });

  useEffect(() => {
    const fetchTypes = async () => {
      try {
        const res = await ceremonyTypesApi.getAll();
        setTypes(res.data);
        if (res.data.length > 0) {
          setFormData(prev => ({ ...prev, ceremony_type_id: String(res.data[0].id) }));
        }
      } catch (error) {
        console.error('Erreur chargement types', error);
      }
    };
    fetchTypes();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      const data: CreateCeremonyData = {
        ceremony_type_id: Number(formData.ceremony_type_id),
        title: formData.title,
        event_date: formData.event_date,
        location: formData.location || undefined,
        budget: formData.budget ? Number(formData.budget) : undefined,
        guest_count: formData.guest_count ? Number(formData.guest_count) : undefined,
      };
      await ceremoniesApi.create(data);
      navigate('/dashboard');
    } catch (err) {
      setError("Erreur lors de la création de l'événement");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background pt-24 pb-16">
      <Container size="md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-text-primary mb-2">
            Créer un nouvel événement
          </h1>
          <p className="text-text-secondary">
            Remplissez les informations ci-dessous pour commencer
          </p>
        </div>

        <Card className="p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Type d'événement */}
            <div>
              <label htmlFor="ceremony_type_id" className="block text-sm font-medium text-text-primary mb-2">
                Type d'événement *
              </label>
              <select
                id="ceremony_type_id"
                name="ceremony_type_id"
                value={formData.ceremony_type_id}
                onChange={handleChange}
                className="w-full px-4 py-3 rounded-xl border border-border bg-white focus:outline-none focus:ring-2 focus:ring-primary-500/30"
                required
              >
                <option value="">Sélectionnez un type</option>
                {types.map(type => (
                  <option key={type.id} value={type.id}>{type.name}</option>
                ))}
              </select>
            </div>

            {/* Titre */}
            <div>
              <label htmlFor="title" className="block text-sm font-medium text-text-primary mb-2">
                Titre de l'événement *
              </label>
              <Input
                id="title"
                name="title"
                value={formData.title}
                onChange={handleChange}
                placeholder="Ex: Mariage de Sophie & Thomas"
                required
              />
            </div>

            {/* Date */}
            <div>
              <label htmlFor="event_date" className="block text-sm font-medium text-text-primary mb-2">
                Date de l'événement *
              </label>
              <Input
                id="event_date"
                name="event_date"
                type="date"
                value={formData.event_date}
                onChange={handleChange}
                required
              />
            </div>

            {/* Lieu */}
            <div>
              <label htmlFor="location" className="block text-sm font-medium text-text-primary mb-2">
                Lieu
              </label>
              <Input
                id="location"
                name="location"
                value={formData.location}
                onChange={handleChange}
                placeholder="Ville, adresse..."
              />
            </div>

            {/* Budget */}
            <div>
              <label htmlFor="budget" className="block text-sm font-medium text-text-primary mb-2">
                Budget total (€)
              </label>
              <Input
                id="budget"
                name="budget"
                type="number"
                value={formData.budget}
                onChange={handleChange}
                placeholder="Ex: 15000"
              />
            </div>

            {/* Nombre d'invités */}
            <div>
              <label htmlFor="guest_count" className="block text-sm font-medium text-text-primary mb-2">
                Nombre d'invités
              </label>
              <Input
                id="guest_count"
                name="guest_count"
                type="number"
                value={formData.guest_count}
                onChange={handleChange}
                placeholder="Ex: 120"
              />
            </div>

            {error && (
              <p className="text-sm text-red-500">{error}</p>
            )}

            <div className="flex gap-4 pt-4">
              <Button type="submit" variant="primary" disabled={isLoading}>
                {isLoading ? 'Création...' : 'Créer l\'événement'}
              </Button>
              <Button type="button" variant="outline" onClick={() => navigate(-1)}>
                Annuler
              </Button>
            </div>
          </form>
        </Card>
      </Container>
    </div>
  );
}