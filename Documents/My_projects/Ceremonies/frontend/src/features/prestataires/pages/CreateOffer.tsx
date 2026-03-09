import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container } from '../../../shared/components/ui/Container';
import { Card } from '../../../shared/components/ui/Card';
import { Button } from '../../../shared/components/ui/Button';
import { Input } from '../../../shared/components/ui/Input';
import { offersApi } from '../../../shared/api/offers';
import type { CreateOfferData } from '../../../shared/api/offers';
import { ceremonyTypesApi } from '../../../shared/api/ceremonyTypes';
import type { CeremonyType } from '../../../shared/api/ceremonyTypes';
import { OfferMediaManager } from '../components/OfferMediaManager';

export default function CreateOffer() {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [ceremonyTypes, setCeremonyTypes] = useState<CeremonyType[]>([]);
  const [createdOfferId, setCreatedOfferId] = useState<number | null>(null);
  const [formData, setFormData] = useState({
    ceremony_type_id: '',
    title: '',
    description: '',
    base_price: '',
  });

  useEffect(() => {
    const fetchCeremonyTypes = async () => {
      try {
        const res = await ceremonyTypesApi.getAll();
        setCeremonyTypes(res.data);
      } catch (error) {
        console.error('Erreur chargement types de cérémonie', error);
      }
    };
    fetchCeremonyTypes();
  }, []);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      const data: CreateOfferData = {
        ceremony_type_id: parseInt(formData.ceremony_type_id),
        title: formData.title,
        description: formData.description || null,
        base_price: formData.base_price ? parseFloat(formData.base_price) : null,
      };
      const response = await offersApi.create(data);
      setCreatedOfferId(response.data.id);
    } catch (err) {
      setError("Erreur lors de la création de l'offre");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  if (createdOfferId) {
    return (
      <div className="min-h-screen bg-background pt-24 pb-16">
        <Container size="md">
          <Card className="p-8">
            <h1 className="text-2xl font-bold text-text-primary mb-6">
              Offre créée avec succès
            </h1>
            <p className="text-text-secondary mb-6">
              Vous pouvez maintenant ajouter des photos à votre offre.
            </p>
            <OfferMediaManager offerId={createdOfferId} />
            <div className="mt-8 flex gap-4">
              <Button variant="primary" onClick={() => navigate('/offers')}>
                Voir mes offres
              </Button>
              <Button variant="outline" onClick={() => navigate('/prestataire/dashboard')}>
                Retour au dashboard
              </Button>
            </div>
          </Card>
        </Container>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background pt-24 pb-16">
      <Container size="md">
        <Card className="p-8">
          <h1 className="text-2xl font-bold text-text-primary mb-6">Créer une nouvelle offre</h1>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="ceremony_type_id" className="block text-sm font-medium text-text-primary mb-2">
                Type de cérémonie *
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
                {ceremonyTypes.map(type => (
                  <option key={type.id} value={type.id}>{type.name}</option>
                ))}
              </select>
            </div>

            <div>
              <label htmlFor="title" className="block text-sm font-medium text-text-primary mb-2">
                Titre de l'offre *
              </label>
              <Input
                id="title"
                name="title"
                value={formData.title}
                onChange={handleChange}
                placeholder="Ex: Pack Mariage complet"
                required
              />
            </div>

            <div>
              <label htmlFor="description" className="block text-sm font-medium text-text-primary mb-2">
                Description
              </label>
              <textarea
                id="description"
                name="description"
                value={formData.description}
                onChange={handleChange}
                rows={4}
                className="w-full px-4 py-3 rounded-xl border border-border bg-white focus:outline-none focus:ring-2 focus:ring-primary-500/30"
                placeholder="Décrivez votre prestation..."
              />
            </div>

            <div>
              <label htmlFor="base_price" className="block text-sm font-medium text-text-primary mb-2">
                Prix de base (€)
              </label>
              <Input
                id="base_price"
                name="base_price"
                type="number"
                value={formData.base_price}
                onChange={handleChange}
                placeholder="Ex: 1200"
              />
            </div>

            {error && <p className="text-sm text-red-500">{error}</p>}

            <div className="flex gap-4">
              <Button type="submit" variant="primary" disabled={isLoading}>
                {isLoading ? 'Création...' : 'Créer l\'offre'}
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