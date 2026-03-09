import { useState, useEffect } from 'react';
import { XMarkIcon, PhotoIcon } from '@heroicons/react/24/outline';
import { offerMediaApi } from '../../../shared/api/offerMedia';
import type { OfferMedia } from '../../../shared/api/offerMedia';

interface OfferMediaManagerProps {
  offerId: number;
}

export function OfferMediaManager({ offerId }: OfferMediaManagerProps) {
  const [mediaList, setMediaList] = useState<OfferMedia[]>([]);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  useEffect(() => {
    fetchMedia();
  }, [offerId]);

  const fetchMedia = async () => {
    try {
      const res = await offerMediaApi.getByOffer(offerId);
      setMediaList(res.data);
    } catch (error) {
      console.error('Erreur chargement médias', error);
    }
  };

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;
    setUploading(true);
    setError(null);
    try {
      for (const file of Array.from(e.target.files)) {
        await offerMediaApi.upload(offerId, file);
      }
      await fetchMedia();
    } catch (error) {
      setError("Erreur lors de l'upload");
      console.error(error);
    } finally {
      setUploading(false);
      e.target.value = '';
    }
  };

  const handleDelete = async (mediaId: number) => {
    if (!window.confirm('Supprimer ce média ?')) return;
    try {
      await offerMediaApi.delete(mediaId);
      setMediaList(prev => prev.filter(m => m.id !== mediaId));
    } catch (error) {
      console.error('Erreur suppression', error);
    }
  };

  const isVideo = (mimeType: string | null) => {
    return mimeType?.startsWith('video/') || false;
  };

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-text-primary">Médias de l'offre</h3>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {mediaList.map(media => (
          <div key={media.id} className="relative group">
            {isVideo(media.media_type) ? (
              <video
                src={`${API_URL}${media.media_url}`}
                className="w-full h-32 object-cover rounded-lg"
                controls
              />
            ) : (
              <img
                src={`${API_URL}${media.media_url}`}
                alt=""
                className="w-full h-32 object-cover rounded-lg"
              />
            )}
            <button
              onClick={() => handleDelete(media.id)}
              className="absolute top-1 right-1 p-1 bg-red-500 text-white rounded-full opacity-0 group-hover:opacity-100 transition-opacity"
            >
              <XMarkIcon className="w-4 h-4" />
            </button>
          </div>
        ))}

        <label className="border-2 border-dashed border-border rounded-lg h-32 flex flex-col items-center justify-center cursor-pointer hover:border-primary-300 transition-colors">
          {uploading ? (
            <div className="flex flex-col items-center">
              <div className="w-8 h-8 border-4 border-primary-200 border-t-primary-500 rounded-full animate-spin mb-1" />
              <span className="text-xs text-text-secondary">Upload...</span>
            </div>
          ) : (
            <>
              <PhotoIcon className="w-8 h-8 text-text-tertiary mb-1" />
              <span className="text-xs text-text-secondary">
                Images / Vidéos
              </span>
            </>
          )}
          <input
            type="file"
            multiple
            accept="image/*,video/*"
            onChange={handleUpload}
            disabled={uploading}
            className="hidden"
          />
        </label>
      </div>

      {error && <p className="text-sm text-red-500">{error}</p>}
    </div>
  );
}