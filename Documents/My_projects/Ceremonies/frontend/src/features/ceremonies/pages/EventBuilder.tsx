import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { CalendarIcon, MapPinIcon, UserGroupIcon, CurrencyEuroIcon } from "@heroicons/react/24/outline";
import { Container } from "../../../shared/components/ui/Container";
import { Card } from "../../../shared/components/ui/Card";
import { Button } from "../../../shared/components/ui/Button";
import { Input } from "../../../shared/components/ui/Input";
import { ceremonyTypesApi } from "../../../shared/api/ceremonyTypes";
import type { CeremonyType } from "../../../shared/api/ceremonyTypes";

export default function EventBuilder() {
  const navigate = useNavigate();
  const [ceremonyTypes, setCeremonyTypes] = useState<CeremonyType[]>([]);
  const [formData, setFormData] = useState({
    ceremony_type_id: "",
    total_budget: "",
    city: "",
    event_date: "",
    guest_count: "",
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchTypes = async () => {
      try {
        const res = await ceremonyTypesApi.getAll();
        setCeremonyTypes(res.data);
      } catch (error) {
        console.error("Erreur chargement types de cérémonie", error);
      }
    };
    fetchTypes();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    // Construire les paramètres pour la page de recommandations
    const params = new URLSearchParams({
      ceremony_type_id: formData.ceremony_type_id,
      total_budget: formData.total_budget,
      city: formData.city,
      event_date: formData.event_date,
      guest_count: formData.guest_count || "",
    });
    navigate(`/pack-recommendations?${params.toString()}`);
  };

  return (
    <div className="min-h-screen bg-background pt-24 pb-16">
      <Container size="md">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <Card className="p-8">
            <h1 className="text-3xl font-bold text-text-primary mb-2">Commencer mon évènement</h1>
            <p className="text-text-secondary mb-6">
              Répondez à quelques questions pour obtenir des recommandations personnalisées.
            </p>

            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Type de cérémonie */}
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

              {/* Budget total */}
              <div>
                <label htmlFor="total_budget" className="block text-sm font-medium text-text-primary mb-2">
                  Budget total estimé (€) *
                </label>
                <Input
                  id="total_budget"
                  name="total_budget"
                  type="number"
                  value={formData.total_budget}
                  onChange={handleChange}
                  placeholder="Ex: 5000"
                  icon={<CurrencyEuroIcon className="w-5 h-5" />}
                  required
                />
              </div>

              {/* Ville */}
              <div>
                <label htmlFor="city" className="block text-sm font-medium text-text-primary mb-2">
                  Ville ou emplacement *
                </label>
                <Input
                  id="city"
                  name="city"
                  value={formData.city}
                  onChange={handleChange}
                  placeholder="Ex: Lyon"
                  icon={<MapPinIcon className="w-5 h-5" />}
                  required
                />
              </div>

              {/* Date */}
              <div>
                <label htmlFor="event_date" className="block text-sm font-medium text-text-primary mb-2">
                  Date de l'événement *
                </label>
                <Input
                  id="event_date"
                  name="event_date"
                  type="date"
                  value={formData.event_date}
                  onChange={handleChange}
                  icon={<CalendarIcon className="w-5 h-5" />}
                  required
                />
              </div>

              {/* Nombre d'invités (optionnel) */}
              <div>
                <label htmlFor="guest_count" className="block text-sm font-medium text-text-primary mb-2">
                  Nombre d'invités (optionnel)
                </label>
                <Input
                  id="guest_count"
                  name="guest_count"
                  type="number"
                  value={formData.guest_count}
                  onChange={handleChange}
                  placeholder="Ex: 100"
                  icon={<UserGroupIcon className="w-5 h-5" />}
                />
              </div>

              <div className="pt-4">
                <Button type="submit" variant="primary" fullWidth disabled={loading}>
                  {loading ? "Chargement..." : "Voir les recommandations"}
                </Button>
              </div>
            </form>
          </Card>
        </motion.div>
      </Container>
    </div>
  );
}