import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { BuildingOfficeIcon, MapPinIcon, PhotoIcon } from '@heroicons/react/24/outline';
import { Button } from '../../../shared/components/ui/Button';
import { Input } from '../../../shared/components/ui/Input';
import { apiClient } from '../../../shared/api/client';
import { serviceCategoriesApi } from '../../../shared/api/serviceCategories';
import type { ServiceCategory } from '../../../shared/api/serviceCategories';

export function BecomePrestataireForm() {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [categories, setCategories] = useState<ServiceCategory[]>([]);
  const [selectedOption, setSelectedOption] = useState<'existing' | 'new'>('existing');
  const [formData, setFormData] = useState({
    business_name: '',
    category_id: '',
    new_category_name: '',
    description: '',
    city: '',
  });
  const [documents, setDocuments] = useState<File[]>([]);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const res = await serviceCategoriesApi.getAll();
        setCategories(res.data);
      } catch (error) {
        console.error('Erreur chargement catégories', error);
      }
    };
    fetchCategories();
  }, []);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setDocuments(Array.from(e.target.files));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      // Construction du payload
      const payload: any = {
        business_name: formData.business_name,
        description: formData.description || null,
        city: formData.city,
      };
      if (selectedOption === 'existing') {
        payload.category_id = parseInt(formData.category_id);
      } else {
        payload.new_category_name = formData.new_category_name;
      }

      // 1. Créer le profil prestataire
      const profileResponse = await apiClient.post('/prestataires/request', payload);
      const prestataireId = profileResponse.data.id;

      // 2. Uploader les documents
      if (documents.length > 0) {
        for (const file of documents) {
          const uploadFormData = new FormData();
          uploadFormData.append('file', file);
          await apiClient.post(`/verification_documents/upload/${prestataireId}`, uploadFormData, {
            headers: { 'Content-Type': 'multipart/form-data' },
          });
        }
      }

      navigate('/pending-approval');
    } catch (err) {
      setError('Erreur lors de la création du profil');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <motion.form
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      onSubmit={handleSubmit}
      className="space-y-6"
    >
      {/* Nom de l'entreprise / marque */}
      <div>
        <label htmlFor="business_name" className="block text-sm font-medium text-text-primary mb-2">
          Nom de votre entreprise / marque *
        </label>
        <Input
          id="business_name"
          name="business_name"
          value={formData.business_name}
          onChange={handleChange}
          placeholder="Ex: Photographie Sophie, Traiteur Lyonnais, etc."
          icon={<BuildingOfficeIcon className="w-5 h-5" />}
          required
        />
      </div>

      {/* Sélection du métier */}
      <div>
        <label className="block text-sm font-medium text-text-primary mb-2">
          Votre métier *
        </label>
        <div className="space-y-4">
          <div className="flex items-center gap-4">
            <label className="flex items-center gap-2">
              <input
                type="radio"
                name="option"
                value="existing"
                checked={selectedOption === 'existing'}
                onChange={() => setSelectedOption('existing')}
              />
              <span>Choisir dans la liste</span>
            </label>
            <label className="flex items-center gap-2">
              <input
                type="radio"
                name="option"
                value="new"
                checked={selectedOption === 'new'}
                onChange={() => setSelectedOption('new')}
              />
              <span>Proposer un nouveau métier</span>
            </label>
          </div>

          {selectedOption === 'existing' && (
            <select
              name="category_id"
              value={formData.category_id}
              onChange={handleChange}
              className="w-full px-4 py-3 rounded-xl border border-border bg-white focus:outline-none focus:ring-2 focus:ring-primary-500/30"
              required={selectedOption === 'existing'}
            >
              <option value="">Sélectionnez un métier</option>
              {categories.map(cat => (
                <option key={cat.id} value={cat.id}>{cat.name}</option>
              ))}
            </select>
          )}

          {selectedOption === 'new' && (
            <Input
              name="new_category_name"
              value={formData.new_category_name}
              onChange={handleChange}
              placeholder="Ex: Organisateur de mariage"
              required={selectedOption === 'new'}
            />
          )}
        </div>
      </div>

      {/* Description */}
      <div>
        <label htmlFor="description" className="block text-sm font-medium text-text-primary mb-2">
          Description de vos services
        </label>
        <textarea
          id="description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          rows={4}
          className="w-full px-4 py-3 rounded-xl border border-border bg-white focus:outline-none focus:ring-2 focus:ring-primary-500/30"
          placeholder="Décrivez votre activité, votre expérience, vos spécialités..."
        />
      </div>

      {/* Ville */}
      <div>
        <label htmlFor="city" className="block text-sm font-medium text-text-primary mb-2">
          Ville *
        </label>
        <Input
          id="city"
          name="city"
          value={formData.city}
          onChange={handleChange}
          placeholder="Lyon"
          icon={<MapPinIcon className="w-5 h-5" />}
          required
        />
      </div>

      {/* Documents */}
      <div>
        <label className="block text-sm font-medium text-text-primary mb-2">
          Documents de vérification (justificatif d'identité, KBIS, etc.)
        </label>
        <div className="flex items-center gap-4">
          <label className="flex-1 cursor-pointer">
            <div className="border-2 border-dashed border-border rounded-xl p-6 text-center hover:border-primary-300 transition-colors">
              <PhotoIcon className="w-8 h-8 mx-auto text-text-tertiary mb-2" />
              <span className="text-sm text-text-secondary">
                Cliquez pour ajouter des fichiers
              </span>
              <input
                type="file"
                multiple
                accept=".pdf,.jpg,.jpeg,.png"
                onChange={handleFileChange}
                className="hidden"
              />
            </div>
          </label>
        </div>
        {documents.length > 0 && (
          <div className="mt-2 text-sm text-text-secondary">
            {documents.length} fichier(s) sélectionné(s)
          </div>
        )}
      </div>

      {error && <p className="text-sm text-red-500">{error}</p>}

      <Button type="submit" variant="primary" fullWidth disabled={isLoading}>
        {isLoading ? 'Enregistrement...' : 'Finaliser mon inscription'}
      </Button>
    </motion.form>
  );
}