import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Container } from '../../../shared/components/ui/Container';
import { Card } from '../../../shared/components/ui/Card';
import { Button } from '../../../shared/components/ui/Button';
import { Input } from '../../../shared/components/ui/Input';
import { offersApi } from '../../../shared/api/offers';
import type { CreateOfferData } from '../../../shared/api/offers';
import { CeremonyTypeSelector } from '../components/CeremonyTypeSelector';
import { OfferMediaManager } from '../components/OfferMediaManager';

export default function EditOffer() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [ceremonyTypeId, setCeremonyTypeId] = useState<number | null>(null);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    base_price: '',
  });

  useEffect(() => {
    const fetchOffer = async () => {
      if (!id) return;
      try {
        const res = await offersApi.getOne(parseInt(id));
        const offer = res.data;
        setCeremonyTypeId(offer.ceremony_type_id);
        setFormData({
          title: offer.title,
          description: offer.description || '',
          base_price: offer.base_price?.toString() || '',
        });
      } catch (error) {
        console.error('Erreur chargement offre', error);
        setError("Impossible de charger l'offre");
      }
    };
    fetchOffer();
  }, [id]);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!ceremonyTypeId) {
      setError("Veuillez sélectionner un type de cérémonie");
      return;
    }
    setIsLoading(true);
    setError(null);

    try {
      const data: CreateOfferData = {
        ceremony_type_id: ceremonyTypeId,
        title: formData.title,
        description: formData.description || null,
        base_price: formData.base_price ? parseFloat(formData.base_price) : null,
      };
      await offersApi.update(parseInt(id!), data);
      // Reste sur la page après mise à jour
    } catch (err) {
      setError("Erreur lors de la mise à jour de l'offre");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading && !formData.title) {
    return (
      <div className="min-h-screen bg-background pt-24 flex justify-center">
        <div className="w-12 h-12 border-4 border-primary-200 border-t-primary-500 rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background pt-24 pb-16">
      <Container size="md">
        <Card className="p-8">
          <h1 className="text-2xl font-bold text-text-primary mb-6">Modifier l'offre</h1>

          <form id="edit-form" onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-text-primary mb-2">
                Type de cérémonie *
              </label>
              <CeremonyTypeSelector
                value={ceremonyTypeId || undefined}
                onChange={setCeremonyTypeId}
              />
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
              />
            </div>

            {error && <p className="text-sm text-red-500">{error}</p>}

            <div className="flex gap-4">
              <Button type="submit" variant="primary" disabled={isLoading}>
                {isLoading ? 'Mise à jour...' : 'Mettre à jour'}
              </Button>
              <Button type="button" variant="outline" onClick={() => navigate(-1)}>
                Annuler
              </Button>
            </div>
          </form>

          <hr className="my-8 border-border" />

          <OfferMediaManager offerId={parseInt(id!)} />
        </Card>
      </Container>
    </div>
  );
}