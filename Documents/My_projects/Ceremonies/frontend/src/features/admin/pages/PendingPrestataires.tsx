import { useEffect, useState } from 'react';
import { Container } from '../../../shared/components/ui/Container';
import { Card } from '../../../shared/components/ui/Card';
import { Button } from '../../../shared/components/ui/Button';
import { adminApi } from '../../../shared/api/admin';
import type { Prestataire, VerificationDocument, ServiceCategory } from '../../../shared/api/admin';
import { AdminSidebar } from '../components/AdminSidebar';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function PendingPrestataires() {
  const [prestataires, setPrestataires] = useState<Prestataire[]>([]);
  const [categories, setCategories] = useState<ServiceCategory[]>([]);
  const [selectedDocs, setSelectedDocs] = useState<VerificationDocument[]>([]);
  const [showDocsModal, setShowDocsModal] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [prestatairesRes, categoriesRes] = await Promise.all([
          adminApi.getPendingPrestataires(),
          adminApi.getServiceCategories(),
        ]);
        setPrestataires(prestatairesRes.data);
        setCategories(categoriesRes.data);
      } catch (error) {
        console.error('Erreur chargement données', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleViewDocs = async (prestataireId: number) => {
    try {
      const res = await adminApi.getPrestataireDocuments(prestataireId);
      setSelectedDocs(res.data);
      setShowDocsModal(true);
    } catch (error) {
      console.error('Erreur chargement documents', error);
    }
  };

  const handleVerify = async (prestataireId: number, approved: boolean) => {
    try {
      await adminApi.verifyPrestataire(prestataireId, approved);
      // Rafraîchir la liste
      const res = await adminApi.getPendingPrestataires();
      setPrestataires(res.data);
    } catch (error) {
      console.error('Erreur vérification', error);
    }
  };

  // Fonction pour obtenir le nom de la catégorie
  const getCategoryName = (prestataire: Prestataire): string => {
    if (prestataire.proposed_category) {
      return `Proposition: ${prestataire.proposed_category}`;
    }
    if (prestataire.category_id) {
      const cat = categories.find(c => c.id === prestataire.category_id);
      return cat ? cat.name : `Catégorie #${prestataire.category_id}`;
    }
    return 'Catégorie non définie';
  };

  if (loading) return <div className="text-center py-8">Chargement...</div>;

  return (
    <div className="flex">
      <AdminSidebar />
      <main className="flex-1 ml-64 p-8">
        <Container size="lg">
          <h1 className="text-3xl font-bold mb-6">Prestataires en attente de vérification</h1>
          {prestataires.length === 0 ? (
            <p className="text-text-secondary">Aucun prestataire en attente.</p>
          ) : (
            <div className="space-y-4">
              {prestataires.map((p) => (
                <Card key={p.id} className="p-6">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <h2 className="text-xl font-semibold">{p.business_name}</h2>
                      <p className="text-text-secondary">
                        {p.city} • {getCategoryName(p)}
                      </p>
                      <p className="mt-2">{p.description}</p>
                      {p.proposed_category && (
                        <span className="inline-block mt-2 px-3 py-1 bg-yellow-100 text-yellow-800 text-xs rounded-full">
                          Nouvelle catégorie proposée : {p.proposed_category}
                        </span>
                      )}
                    </div>
                    <div className="flex gap-3">
                      <Button variant="outline" size="sm" onClick={() => handleViewDocs(p.id)}>
                        Voir documents
                      </Button>
                      <Button variant="primary" size="sm" onClick={() => handleVerify(p.id, true)}>
                        Valider
                      </Button>
                      <Button variant="ghost" size="sm" onClick={() => handleVerify(p.id, false)}>
                        Rejeter
                      </Button>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          )}

          {/* Modal pour afficher les documents */}
          {showDocsModal && (
            <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
              <div className="bg-white rounded-2xl p-6 max-w-2xl w-full max-h-[80vh] overflow-y-auto">
                <h2 className="text-xl font-bold mb-4">Documents de vérification</h2>
                <div className="space-y-4">
                  {selectedDocs.map(doc => (
                    <div key={doc.id} className="border border-border rounded-lg p-4">
                      <p className="text-sm text-text-secondary">Type: {doc.document_type || 'Document'}</p>
                      <a
                        href={`${API_URL}${doc.document_url}`}
                        target="_blank"
                        rel="noreferrer"
                        className="text-primary-500 hover:underline"
                      >
                        Voir le document
                      </a>
                      <p className="text-xs text-text-tertiary mt-1">Statut: {doc.status}</p>
                    </div>
                  ))}
                </div>
                <div className="mt-6 flex justify-end">
                  <Button variant="outline" onClick={() => setShowDocsModal(false)}>
                    Fermer
                  </Button>
                </div>
              </div>
            </div>
          )}
        </Container>
      </main>
    </div>
  );
}