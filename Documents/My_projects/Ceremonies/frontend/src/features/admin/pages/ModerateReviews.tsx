import { useEffect, useState } from 'react';
import { Container } from '../../../shared/components/ui/Container';
import { Card } from '../../../shared/components/ui/Card';
import { Button } from '../../../shared/components/ui/Button';
import { apiClient } from '../../../shared/api/client';
import { AdminSidebar } from '../components/AdminSidebar';

interface ReviewToModerate {
  id: number;
  author: string;
  rating: number;
  content: string;
  status: 'pending' | 'approved' | 'rejected';
  created_at: string;
}

export default function ModerateReviews() {
  const [reviews, setReviews] = useState<ReviewToModerate[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchReviews();
  }, []);

  const fetchReviews = async () => {
    try {
      // Endpoint à créer : /admin/reviews/pending
      const res = await apiClient.get('/admin/reviews/pending');
      setReviews(res.data);
    } catch (error) {
      console.error('Erreur chargement avis', error);
    } finally {
      setLoading(false);
    }
  };

  const handleModerate = async (reviewId: number, approved: boolean) => {
    try {
      await apiClient.post(`/admin/reviews/${reviewId}/moderate`, { approved });
      fetchReviews(); // rafraîchir la liste
    } catch (error) {
      console.error('Erreur modération', error);
    }
  };

  if (loading) return <div className="text-center py-8">Chargement...</div>;

  return (
    <div className="flex">
      <AdminSidebar />
      <main className="flex-1 ml-64 p-8">
        <Container size="lg">
          <h1 className="text-3xl font-bold mb-6">Modération des avis</h1>
          {reviews.length === 0 ? (
            <p className="text-text-secondary">Aucun avis en attente.</p>
          ) : (
            <div className="space-y-4">
              {reviews.map((review) => (
                <Card key={review.id} className="p-6">
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="font-semibold">{review.author}</p>
                      <p className="text-sm text-text-secondary">Note : {review.rating}/5</p>
                      <p className="text-xs text-text-tertiary">{new Date(review.created_at).toLocaleDateString()}</p>
                      <p className="mt-2">{review.content}</p>
                    </div>
                    <div className="flex gap-2">
                      <Button variant="primary" size="sm" onClick={() => handleModerate(review.id, true)}>
                        Approuver
                      </Button>
                      <Button variant="ghost" size="sm" onClick={() => handleModerate(review.id, false)}>
                        Rejeter
                      </Button>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          )}
        </Container>
      </main>
    </div>
  );
}