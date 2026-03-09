import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Container } from '../../../shared/components/ui/Container';
import { Card } from '../../../shared/components/ui/Card';
import { Button } from '../../../shared/components/ui/Button';
import { offersApi } from '../../../shared/api/offers';
import type { Offer } from '../../../shared/api/offers';
import { PencilIcon, TrashIcon, PlusIcon } from '@heroicons/react/24/outline';

export default function ManageOffers() {
  const [offers, setOffers] = useState<Offer[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchOffers();
  }, []);

  const fetchOffers = async () => {
    try {
      const res = await offersApi.getMyOffers();
      setOffers(res.data);
    } catch (error) {
      console.error('Erreur chargement offres', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm('Supprimer cette offre ?')) return;
    try {
      await offersApi.delete(id);
      fetchOffers();
    } catch (error) {
      console.error('Erreur suppression', error);
    }
  };

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
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-text-primary">Gérer mes offres</h1>
          <Link to="/offers/create">
            <Button variant="primary">
              <PlusIcon className="w-5 h-5 mr-2" />
              Nouvelle offre
            </Button>
          </Link>
        </div>

        {offers.length === 0 ? (
          <p className="text-text-secondary">Vous n'avez pas encore créé d'offre.</p>
        ) : (
          <div className="grid gap-4">
            {offers.map((offer) => (
              <Card key={offer.id} className="p-6 flex justify-between items-center">
                <div>
                  <h2 className="text-xl font-semibold text-text-primary">{offer.title}</h2>
                  <p className="text-text-secondary mt-1">{offer.description}</p>
                  <div className="flex gap-4 mt-2 text-sm">
                    <span className="text-primary-500 font-medium">
                      {offer.base_price ? `${offer.base_price}€` : 'Sur devis'}
                    </span>
                    <span className="text-text-tertiary">
                      {offer.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </div>
                </div>
                <div className="flex gap-2">
                  <Link to={`/offers/edit/${offer.id}`}>
                    <Button variant="outline" size="sm">
                      <PencilIcon className="w-4 h-4" />
                    </Button>
                  </Link>
                  <Button variant="ghost" size="sm" onClick={() => handleDelete(offer.id)}>
                    <TrashIcon className="w-4 h-4 text-red-500" />
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        )}
      </Container>
    </div>
  );
}