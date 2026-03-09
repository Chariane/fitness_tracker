// frontend/src/features/profile/pages/EditProfile.tsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container } from '../../../shared/components/ui/Container';
import { Card } from '../../../shared/components/ui/Card';
import { Button } from '../../../shared/components/ui/Button';
import { Input } from '../../../shared/components/ui/Input';
import { Avatar } from '../../../shared/components/ui/Avatar';
import { apiClient } from '../../../shared/api/client';
import { useAuth } from '../../auth/hooks/useAuth';
import { CameraIcon } from '@heroicons/react/24/outline';

export default function EditProfile() {
  const navigate = useNavigate();
  const { user, setUser } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [uploadingAvatar, setUploadingAvatar] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [fullName, setFullName] = useState(user?.full_name || '');

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
      setUser(res.data);
    } catch (err) {
      setError("Erreur lors de l'upload de l'avatar");
      console.error(err);
    } finally {
      setUploadingAvatar(false);
      e.target.value = '';
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      const res = await apiClient.put('/users/me', { full_name: fullName });
      setUser(res.data);
      navigate(-1);
    } catch (err) {
      setError('Erreur lors de la mise à jour du profil');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  return (
    <div className="min-h-screen bg-background pt-24 pb-16">
      <Container size="md">
        <Card className="p-8">
          <h1 className="text-2xl font-bold text-text-primary mb-6">Modifier mon profil</h1>

          <div className="flex flex-col items-center mb-6">
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
            {uploadingAvatar && (
              <p className="text-sm text-text-secondary mt-2">Upload en cours...</p>
            )}
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="full_name" className="block text-sm font-medium text-text-primary mb-2">
                Nom complet
              </label>
              <Input
                id="full_name"
                name="full_name"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
              />
            </div>

            {error && <p className="text-sm text-red-500">{error}</p>}

            <div className="flex gap-4">
              <Button type="submit" variant="primary" disabled={isLoading}>
                {isLoading ? 'Mise à jour...' : 'Enregistrer'}
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