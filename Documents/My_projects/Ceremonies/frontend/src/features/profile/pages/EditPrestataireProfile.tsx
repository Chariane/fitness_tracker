import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container } from '../../../shared/components/ui/Container';
import { Card } from '../../../shared/components/ui/Card';
import { Button } from '../../../shared/components/ui/Button';
import { Input } from '../../../shared/components/ui/Input';
import { Avatar } from '../../../shared/components/ui/Avatar';
import { useAuth } from '../../auth/hooks/useAuth';
import { prestatairesApi } from '../../../shared/api/prestataires';
import { apiClient } from '../../../shared/api/client';   // ← AJOUTÉ
import { CameraIcon } from '@heroicons/react/24/outline';
import type { Prestataire } from '../../../shared/api/prestataires';

export default function EditPrestataireProfile() {
  const navigate = useNavigate();
  const { user, setUser } = useAuth();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [uploadingAvatar, setUploadingAvatar] = useState(false);
  const [uploadingBusinessImage, setUploadingBusinessImage] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [prestataire, setPrestataire] = useState<Prestataire | null>(null);
  const [formData, setFormData] = useState({
    business_name: '',
    description: '',
    city: '',
    whatsapp: '',
    map_url: '',
  });

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await prestatairesApi.getMyProfile();
        setPrestataire(res.data);
        setFormData({
          business_name: res.data.business_name,
          description: res.data.description || '',
          city: res.data.city || '',
          whatsapp: res.data.whatsapp || '',
          map_url: res.data.map_url || '',
        });
      } catch (err) {
        setError('Impossible de charger le profil prestataire');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleAvatarUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;
    setUploadingAvatar(true);
    setError(null);
    try {
      const file = e.target.files[0];
      const formData = new FormData();
      formData.append('file', file);
      const res = await apiClient.post('/users/avatar', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setUser(res.data); // met à jour l'utilisateur global
    } catch (err) {
      setError("Erreur lors de l'upload de l'avatar");
      console.error(err);
    } finally {
      setUploadingAvatar(false);
      e.target.value = '';
    }
  };

  const handleBusinessImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;
    setUploadingBusinessImage(true);
    setError(null);
    try {
      const file = e.target.files[0];
      const formData = new FormData();
      formData.append('file', file);
      const res = await apiClient.post('/prestataires/me/business-image', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      // Mettre à jour le prestataire local
      setPrestataire(prev => prev ? { ...prev, business_image_url: res.data.business_image_url } : null);
    } catch (err) {
      setError("Erreur lors de l'upload de l'image professionnelle");
      console.error(err);
    } finally {
      setUploadingBusinessImage(false);
      e.target.value = '';
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setError(null);
    try {
      await prestatairesApi.updateProfile(formData);
      // Recharger le profil pour être sûr
      const res = await prestatairesApi.getMyProfile();
      setPrestataire(res.data);
      navigate('/prestataire/dashboard');
    } catch (err) {
      setError('Erreur lors de la mise à jour du profil');
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  if (loading) {
    return (
      <div className="min-h-screen bg-background pt-24 flex justify-center">
        <div className="w-12 h-12 border-4 border-primary-200 border-t-primary-500 rounded-full animate-spin" />
      </div>
    );
  }

  if (!prestataire) {
    return (
      <div className="min-h-screen bg-background pt-24 text-center">
        <p className="text-text-secondary">Profil prestataire introuvable.</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background pt-24 pb-16">
      <Container size="md">
        <Card className="p-8">
          <h1 className="text-2xl font-bold text-text-primary mb-6">Modifier mon profil prestataire</h1>

          {/* Avatar utilisateur */}
          <div className="flex flex-col items-center mb-8">
            <label className="block text-sm font-medium text-text-primary mb-2">Photo de profil</label>
            <div className="relative">
              <Avatar
                src={user?.avatar_url ? `${API_URL}${user.avatar_url}` : undefined}
                initials={user?.full_name?.charAt(0) || 'U'}
                size="lg"
                className="w-24 h-24 text-2xl"
              />
              <label
                htmlFor="avatar-upload"
                className="absolute bottom-0 right-0 p-1 bg-primary-500 rounded-full cursor-pointer hover:bg-primary-600 transition-colors"
              >
                <CameraIcon className="w-4 h-4 text-white" />
                <input
                  id="avatar-upload"
                  type="file"
                  accept="image/*"
                  onChange={handleAvatarUpload}
                  disabled={uploadingAvatar}
                  className="hidden"
                />
              </label>
            </div>
            {uploadingAvatar && <p className="text-sm text-text-secondary mt-2">Upload en cours...</p>}
          </div>

          {/* Image professionnelle */}
          <div className="flex flex-col items-center mb-8">
            <label className="block text-sm font-medium text-text-primary mb-2">Image de couverture / business</label>
            <div className="relative">
              {prestataire.business_image_url ? (
                <img
                  src={`${API_URL}${prestataire.business_image_url}`}
                  alt="Business"
                  className="w-32 h-32 object-cover rounded-lg"
                />
              ) : (
                <div className="w-32 h-32 bg-gray-200 rounded-lg flex items-center justify-center text-text-secondary">
                  Aucune image
                </div>
              )}
              <label
                htmlFor="business-image-upload"
                className="absolute bottom-0 right-0 p-1 bg-primary-500 rounded-full cursor-pointer hover:bg-primary-600 transition-colors"
              >
                <CameraIcon className="w-4 h-4 text-white" />
                <input
                  id="business-image-upload"
                  type="file"
                  accept="image/*"
                  onChange={handleBusinessImageUpload}
                  disabled={uploadingBusinessImage}
                  className="hidden"
                />
              </label>
            </div>
            {uploadingBusinessImage && <p className="text-sm text-text-secondary mt-2">Upload en cours...</p>}
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="business_name" className="block text-sm font-medium text-text-primary mb-2">
                Nom de l'entreprise / marque *
              </label>
              <Input
                id="business_name"
                name="business_name"
                value={formData.business_name}
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
              <label htmlFor="city" className="block text-sm font-medium text-text-primary mb-2">
                Ville
              </label>
              <Input
                id="city"
                name="city"
                value={formData.city}
                onChange={handleChange}
              />
            </div>

            <div>
              <label htmlFor="whatsapp" className="block text-sm font-medium text-text-primary mb-2">
                Numéro WhatsApp
              </label>
              <Input
                id="whatsapp"
                name="whatsapp"
                value={formData.whatsapp}
                onChange={handleChange}
                placeholder="+33612345678"
              />
            </div>

            <div>
              <label htmlFor="map_url" className="block text-sm font-medium text-text-primary mb-2">
                Lien Google Maps (partage)
              </label>
              <Input
                id="map_url"
                name="map_url"
                value={formData.map_url}
                onChange={handleChange}
                placeholder="https://maps.app.goo.gl/..."
              />
            </div>

            {error && <p className="text-sm text-red-500">{error}</p>}

            <div className="flex gap-4">
              <Button type="submit" variant="primary" disabled={saving}>
                {saving ? 'Enregistrement...' : 'Enregistrer'}
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