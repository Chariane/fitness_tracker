import { useState, useEffect } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { motion } from "framer-motion";
import {
  ArrowLeftIcon,
  CurrencyEuroIcon,
  PhotoIcon,
  HeartIcon as HeartOutline,
  ChatBubbleLeftIcon,
} from "@heroicons/react/24/outline";
import { HeartIcon as HeartSolid } from "@heroicons/react/24/solid";
import { Container } from "../../../shared/components/ui/Container";
import { Card } from "../../../shared/components/ui/Card";
import { Button } from "../../../shared/components/ui/Button";
import { Avatar } from "../../../shared/components/ui/Avatar";
import { Input } from "../../../shared/components/ui/Input";
import { Gallery } from "../../../shared/components/ui/Gallery";
import { offersApi } from "../../../shared/api/offers";
import { prestatairesApi } from "../../../shared/api/prestataires";
import { ceremonyTypesApi } from "../../../shared/api/ceremonyTypes";
import { offerMediaApi } from "../../../shared/api/offerMedia";
import { commentsApi } from "../../../shared/api/comments";
import { favoritesApi } from "../../../shared/api/favorites";
import { useAuth } from "../../auth/hooks/useAuth";
import type { Offer } from "../../../shared/api/offers";
import type { Prestataire } from "../../../shared/api/prestataires";
import type { OfferMedia } from "../../../shared/api/offerMedia";
import type { Comment } from "../../../shared/api/comments";

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function OfferDetails() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [offer, setOffer] = useState<Offer | null>(null);
  const [prestataire, setPrestataire] = useState<Prestataire | null>(null);
  const [ceremonyName, setCeremonyName] = useState<string>("");
  const [media, setMedia] = useState<OfferMedia[]>([]);
  const [comments, setComments] = useState<Comment[]>([]);
  const [newComment, setNewComment] = useState("");
  const [isLiked, setIsLiked] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) {
      setError("ID de l'offre manquant");
      setLoading(false);
      return;
    }
    const offerId = parseInt(id);
    if (isNaN(offerId)) {
      setError("ID de l'offre invalide");
      setLoading(false);
      return;
    }

    const fetchData = async () => {
      try {
        const [offerRes, mediaRes, commentsRes] = await Promise.all([
          offersApi.getOne(offerId),
          offerMediaApi.getByOffer(offerId),
          commentsApi.getByOffer(offerId),
        ]);
        setOffer(offerRes.data);
        setMedia(mediaRes.data);
        setComments(commentsRes.data);

        const ceremonyRes = await ceremonyTypesApi.getOne(offerRes.data.ceremony_type_id);
        setCeremonyName(ceremonyRes.data.name);

        if (offerRes.data.prestataire_id) {
          const prestRes = await prestatairesApi.getPrestataire(offerRes.data.prestataire_id);
          setPrestataire(prestRes.data);
        }

        if (user) {
          const likeRes = await favoritesApi.check(offerId);
          setIsLiked(likeRes.data.liked);
        }
      } catch (err) {
        console.error("Erreur chargement offre", err);
        setError("Impossible de charger les détails de l'offre.");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [id, user]);

  const handleLikeToggle = async () => {
    if (!user) {
      navigate('/login');
      return;
    }
    try {
      if (isLiked) {
        await favoritesApi.remove(offer!.id);
      } else {
        await favoritesApi.add(offer!.id);
      }
      setIsLiked(!isLiked);
      // Mettre à jour le compteur de likes
      setOffer(prev => prev ? { ...prev, likes_count: (prev.likes_count || 0) + (isLiked ? -1 : 1) } : prev);
    } catch (error) {
      console.error("Erreur like", error);
    }
  };

  const handleAddComment = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user || !newComment.trim() || !offer) return;
    try {
      const res = await commentsApi.create({
        offer_id: offer.id,
        content: newComment.trim(),
      });
      setComments(prev => [res.data, ...prev]);
      setNewComment("");
    } catch (error) {
      console.error("Erreur ajout commentaire", error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-background pt-24 flex justify-center">
        <div className="w-12 h-12 border-4 border-primary-200 border-t-primary-500 rounded-full animate-spin" />
      </div>
    );
  }

  if (error || !offer) {
    return (
      <div className="min-h-screen bg-background pt-24 text-center">
        <p className="text-text-secondary">{error || "Offre introuvable."}</p>
        <Button variant="primary" onClick={() => navigate(-1)} className="mt-4">
          Retour
        </Button>
      </div>
    );
  }

  const imageUrls = media.map(m => `${API_URL}${m.media_url}`);

  return (
    <div className="min-h-screen bg-background pt-24 pb-16">
      <Container size="lg">
        <button
          onClick={() => navigate(-1)}
          className="flex items-center gap-2 text-text-secondary hover:text-text-primary mb-6 transition-colors"
        >
          <ArrowLeftIcon className="w-5 h-5" />
          Retour
        </button>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Colonne principale */}
          <div className="lg:col-span-2 space-y-6">
            <Card className="p-8">
              <div className="flex justify-between items-start mb-4">
                <h1 className="text-3xl font-bold text-text-primary">{offer.title}</h1>
                <div className="flex items-center gap-2">
                  <span className="text-text-secondary">{offer.likes_count || 0}</span>
                  <button
                    onClick={handleLikeToggle}
                    className="p-2 hover:bg-surface-alt rounded-full transition-colors"
                  >
                    {isLiked ? (
                      <HeartSolid className="w-7 h-7 text-red-500" />
                    ) : (
                      <HeartOutline className="w-7 h-7 text-text-secondary" />
                    )}
                  </button>
                </div>
              </div>
              {ceremonyName && (
                <span className="inline-block bg-primary-50 text-primary-700 text-sm font-medium px-3 py-1 rounded-full mb-4">
                  {ceremonyName}
                </span>
              )}
              <p className="text-text-secondary whitespace-pre-line mb-6">
                {offer.description || "Aucune description fournie."}
              </p>
              <div className="flex items-center gap-2 text-2xl font-bold text-primary-500">
                <CurrencyEuroIcon className="w-6 h-6" />
                {offer.base_price ? `${offer.base_price}€` : "Sur devis"}
              </div>
            </Card>

            {/* Galerie */}
            <Card className="p-8">
              <h2 className="text-xl font-bold text-text-primary mb-4 flex items-center gap-2">
                <PhotoIcon className="w-6 h-6" />
                Galerie ({media.length})
              </h2>
              <Gallery images={imageUrls} />
            </Card>

            {/* Commentaires */}
            <Card className="p-8">
              <h2 className="text-xl font-bold text-text-primary mb-4 flex items-center gap-2">
                <ChatBubbleLeftIcon className="w-6 h-6" />
                Commentaires ({comments.length})
              </h2>

              {user ? (
                <form onSubmit={handleAddComment} className="mb-6">
                  <div className="flex gap-3">
                    <Avatar
                      src={user.avatar_url ? `${API_URL}${user.avatar_url}` : undefined}
                      initials={user.full_name?.charAt(0) || "U"}
                      size="sm"
                    />
                    <Input
                      placeholder="Ajouter un commentaire..."
                      value={newComment}
                      onChange={(e) => setNewComment(e.target.value)}
                      className="flex-1"
                    />
                    <Button type="submit" variant="primary" size="sm">
                      Publier
                    </Button>
                  </div>
                </form>
              ) : (
                <p className="text-text-secondary mb-4">
                  <Link to="/login" className="text-primary-500 hover:underline">
                    Connectez-vous
                  </Link>{" "}
                  pour commenter.
                </p>
              )}

              <div className="space-y-4">
                {comments.length === 0 ? (
                  <p className="text-text-secondary">Aucun commentaire pour le moment.</p>
                ) : (
                  comments.map((comment) => (
                    <div key={comment.id} className="flex gap-3">
                      <Avatar
                        src={comment.author_avatar ? `${API_URL}${comment.author_avatar}` : undefined}
                        initials={comment.author_name?.charAt(0) || "U"}
                        size="sm"
                      />
                      <div className="flex-1">
                        <div className="flex justify-between items-start">
                          <span className="font-semibold text-text-primary">
                            {comment.author_name || "Utilisateur"}
                          </span>
                          <span className="text-xs text-text-tertiary">
                            {new Date(comment.created_at).toLocaleDateString()}
                          </span>
                        </div>
                        <p className="text-text-secondary text-sm mt-1">{comment.content}</p>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </Card>
          </div>

          {/* Colonne latérale */}
          <div className="space-y-6">
            {prestataire && (
              <Card className="p-6">
                <h2 className="text-xl font-bold text-text-primary mb-4">Prestataire</h2>
                <Link
                  to={`/prestataire/${prestataire.id}`}
                  className="flex items-center gap-3 hover:bg-surface-alt p-2 rounded-xl transition-colors"
                >
                  <Avatar
                    src={prestataire.avatar_url ? `${API_URL}${prestataire.avatar_url}` : undefined}
                    initials={prestataire.business_name.charAt(0)}
                    size="md"
                  />
                  <div>
                    <p className="font-semibold text-text-primary">{prestataire.business_name}</p>
                    {prestataire.verified && (
                      <span className="text-xs text-green-600">Vérifié</span>
                    )}
                  </div>
                </Link>
              </Card>
            )}

            <Card className="p-6">
              <h2 className="text-xl font-bold text-text-primary mb-4">Intéressé ?</h2>
              <Button
                variant="primary"
                fullWidth
                onClick={() => navigate(`/messages?prestataire=${prestataire?.id}&offer=${offer.id}`)}
              >
                Contacter le prestataire
              </Button>
            </Card>
          </div>
        </div>
      </Container>
    </div>
  );
}