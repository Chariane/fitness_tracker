import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  MagnifyingGlassIcon,
  XMarkIcon,
  MapPinIcon,
  CalendarIcon,
  ChevronDownIcon,
  AdjustmentsHorizontalIcon,
  ShieldCheckIcon,
  ArrowRightIcon
} from "@heroicons/react/24/outline";
import { StarIcon as StarIconSolid } from "@heroicons/react/24/solid";
import { Container } from "../../../shared/components/ui/Container";
import { Button } from "../../../shared/components/ui/Button";
import { Input } from "../../../shared/components/ui/Input";
import { prestatairesApi } from "../../../shared/api/prestataires";
import { serviceCategoriesApi } from "../../../shared/api/serviceCategories"; // ← import direct
import type { PrestataireSearchResult } from "../../../shared/api/prestataires";
import { useDebounce } from "../../../shared/hooks/useDebounce";

// Composant PrestataireCard
const PrestataireCard = ({
  prestataire,
  index,
  categoryName
}: {
  prestataire: PrestataireSearchResult;
  index: number;
  categoryName?: string;
}) => {
  const [isHovered, setIsHovered] = useState(false);

  // Log pour vérifier les données de la carte
  console.log(`Carte ${prestataire.business_name}: catId=${prestataire.category_id}, catName=${categoryName}`);

  const priceDisplay = prestataire.min_price ? (
    prestataire.max_price && prestataire.max_price !== prestataire.min_price
      ? `${prestataire.min_price}€ - ${prestataire.max_price}€`
      : `${prestataire.min_price}€`
  ) : "Sur devis";

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.05 }}
      whileHover={{ y: -5 }}
      onHoverStart={() => setIsHovered(true)}
      onHoverEnd={() => setIsHovered(false)}
      className="group bg-white rounded-2xl overflow-hidden shadow-soft hover:shadow-medium transition-all duration-300 cursor-pointer"
      onClick={() => window.location.href = `/prestataire/${prestataire.id}`}
    >
      <div className="relative h-48 overflow-hidden">
        {prestataire.business_image_url ? (
          <motion.img
            src={`${import.meta.env.VITE_API_URL}${prestataire.business_image_url}`}
            alt={prestataire.business_name}
            className="w-full h-full object-cover"
            animate={{ scale: isHovered ? 1.1 : 1 }}
            transition={{ duration: 0.4 }}
          />
        ) : (
          <div className="w-full h-full bg-gray-200 flex items-center justify-center text-text-secondary">
            Pas d'image
          </div>
        )}
        <div className="absolute inset-0 bg-gradient-to-t from-black/40 via-transparent to-transparent" />

        {/* Badge vérifié */}
        {prestataire.verified && (
          <div className="absolute top-3 right-3">
            <span className="px-3 py-1 rounded-full text-xs font-semibold bg-green-500 text-white">
              Vérifié
            </span>
          </div>
        )}

        {/* Prix */}
        <div className="absolute bottom-3 left-3 text-white font-bold">
          {priceDisplay}
        </div>
      </div>

      <div className="p-5">
        <div className="flex justify-between items-start mb-2">
          <div>
            <h3 className="font-bold text-text-primary text-lg">{prestataire.business_name}</h3>
            {categoryName && (
              <p className="text-text-secondary text-sm mt-1">{categoryName}</p>
            )}
          </div>
          {prestataire.avg_rating ? (
            <div className="flex items-center gap-1">
              <StarIconSolid className="w-4 h-4 text-gold-500" />
              <span className="font-semibold">{prestataire.avg_rating.toFixed(1)}</span>
              <span className="text-text-tertiary text-sm">({prestataire.total_reviews})</span>
            </div>
          ) : (
            <span className="text-text-tertiary text-sm">Aucun avis</span>
          )}
        </div>

        <div className="flex flex-wrap gap-3 text-sm text-text-secondary mb-3">
          {prestataire.city && (
            <div className="flex items-center gap-1">
              <MapPinIcon className="w-4 h-4" />
              <span>{prestataire.city}</span>
            </div>
          )}
          <div className="flex items-center gap-1 text-primary-500">
            <CalendarIcon className="w-4 h-4" />
            <span>Disponible</span>
          </div>
        </div>

        <motion.button
          whileHover={{ x: 5 }}
          className="text-primary-500 font-medium text-sm flex items-center gap-1 group"
        >
          Voir le profil
          <ArrowRightIcon className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
        </motion.button>
      </div>
    </motion.div>
  );
};

// Filtre Slide-over (inchangé)
const FilterSidebar = ({
  isOpen,
  onClose,
  onApply,
  categories,
  initialSelectedIds = []
}: {
  isOpen: boolean;
  onClose: () => void;
  onApply: (filters: any) => void;
  categories: { id: number; name: string }[];
  initialSelectedIds?: number[];
}) => {
  const [selectedIds, setSelectedIds] = useState<number[]>(initialSelectedIds);
  const [city, setCity] = useState('');
  const [minPrice, setMinPrice] = useState('');
  const [maxPrice, setMaxPrice] = useState('');
  const [verifiedOnly, setVerifiedOnly] = useState(false);

  useEffect(() => {
    setSelectedIds(initialSelectedIds);
  }, [initialSelectedIds]);

  const toggleCategory = (id: number) => {
    setSelectedIds(prev =>
      prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]
    );
  };

  const handleApply = () => {
    onApply({
      category_ids: selectedIds.length > 0 ? selectedIds : undefined,
      city: city || undefined,
      min_price: minPrice ? parseFloat(minPrice) : undefined,
      max_price: maxPrice ? parseFloat(maxPrice) : undefined,
      verified_only: verifiedOnly,
    });
    onClose();
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/20 backdrop-blur-sm z-50"
            onClick={onClose}
          />
          <motion.div
            initial={{ x: "100%" }}
            animate={{ x: 0 }}
            exit={{ x: "100%" }}
            transition={{ type: "spring", damping: 25 }}
            className="fixed right-0 top-0 bottom-0 w-full max-w-md bg-white shadow-2xl z-50 overflow-y-auto"
          >
            <div className="p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-bold">Filtres avancés</h2>
                <button onClick={onClose} className="p-2 hover:bg-surface-alt rounded-full">
                  <XMarkIcon className="w-5 h-5" />
                </button>
              </div>

              <div className="mb-6">
                <h3 className="font-semibold mb-3">Catégories</h3>
                <div className="space-y-2 max-h-60 overflow-y-auto border border-border rounded-xl p-3">
                  {categories.map(cat => (
                    <label key={cat.id} className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={selectedIds.includes(cat.id)}
                        onChange={() => toggleCategory(cat.id)}
                        className="rounded border-border text-primary-500 focus:ring-primary-500"
                      />
                      <span className="text-sm text-text-primary">{cat.name}</span>
                    </label>
                  ))}
                </div>
              </div>

              <div className="mb-6">
                <h3 className="font-semibold mb-3">Budget</h3>
                <div className="flex gap-3">
                  <Input
                    placeholder="Min"
                    type="number"
                    value={minPrice}
                    onChange={(e) => setMinPrice(e.target.value)}
                  />
                  <Input
                    placeholder="Max"
                    type="number"
                    value={maxPrice}
                    onChange={(e) => setMaxPrice(e.target.value)}
                  />
                </div>
              </div>

              <div className="mb-6">
                <h3 className="font-semibold mb-3">Ville</h3>
                <div className="relative">
                  <MapPinIcon className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-text-tertiary" />
                  <Input
                    className="pl-10"
                    placeholder="Ville"
                    value={city}
                    onChange={(e) => setCity(e.target.value)}
                  />
                </div>
              </div>

              <div className="mb-6">
                <h3 className="font-semibold mb-3">Profil</h3>
                <label className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    className="rounded border-border text-primary-500"
                    checked={verifiedOnly}
                    onChange={(e) => setVerifiedOnly(e.target.checked)}
                  />
                  <span className="text-sm">Profils vérifiés uniquement</span>
                </label>
              </div>

              <Button variant="primary" fullWidth className="mb-3" onClick={handleApply}>
                Appliquer les filtres
              </Button>
              <Button variant="ghost" fullWidth onClick={() => {
                setSelectedIds([]);
                setCity('');
                setMinPrice('');
                setMaxPrice('');
                setVerifiedOnly(false);
                onApply({});
                onClose();
              }}>
                Réinitialiser
              </Button>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};

// Page principale
export default function PrestataireSearch() {
  const [searchTerm, setSearchTerm] = useState("");
  const [sortBy, setSortBy] = useState("relevance");
  const [isFilterOpen, setIsFilterOpen] = useState(false);
  const [results, setResults] = useState<PrestataireSearchResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [categories, setCategories] = useState<{ id: number; name: string }[]>([]);
  const [filters, setFilters] = useState({
    category_ids: undefined as number[] | undefined,
    city: undefined as string | undefined,
    min_price: undefined as number | undefined,
    max_price: undefined as number | undefined,
    verified_only: false,
  });

  const [quickCategoryId, setQuickCategoryId] = useState<number | null>(null);
  const debouncedSearch = useDebounce(searchTerm, 500);

  // Charger les catégories au montage
  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const res = await serviceCategoriesApi.getAll();
        setCategories(res.data);
        console.log('Catégories chargées:', res.data);
      } catch (error) {
        console.error('Erreur chargement catégories', error);
      }
    };
    fetchCategories();
  }, []);

  // Synchroniser la barre rapide avec les filtres avancés
  useEffect(() => {
    if (quickCategoryId !== null) {
      setFilters(prev => ({ ...prev, category_ids: [quickCategoryId] }));
    } else {
      setFilters(prev => ({ ...prev, category_ids: undefined }));
    }
  }, [quickCategoryId]);

  // Charger les résultats
  useEffect(() => {
    const fetchResults = async () => {
      setIsLoading(true);
      try {
        const params: any = {
          q: debouncedSearch || undefined,
          sort_by: sortBy,
          ...filters,
        };
        Object.keys(params).forEach(key => {
          if (params[key] === undefined) delete params[key];
          if (Array.isArray(params[key]) && params[key].length === 0) delete params[key];
        });
        const res = await prestatairesApi.search(params);
        console.log('Résultats API:', res.data);
        setResults(res.data);
        console.log('Premier résultat détaillé:', res.data[0]);
        console.log('Clés disponibles:', Object.keys(res.data[0]));
      } catch (error) {
        console.error('Erreur recherche', error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchResults();
  }, [debouncedSearch, sortBy, filters]);

  const getCategoryName = (categoryId?: number | null): string | undefined => {
    if (!categoryId) return undefined;
    const cat = categories.find(c => c.id === categoryId);
    return cat?.name;
  };

  return (
    <div className="min-h-screen bg-background pt-24 pb-16">
      <Container>
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-3">
            Trouvez le <span className="text-gradient-primary">prestataire</span> idéal
          </h1>
          <p className="text-text-secondary text-lg">
            Parcourez notre sélection de professionnels qualifiés
          </p>
        </div>

        <div className="mb-6">
          <div className="relative">
            <MagnifyingGlassIcon className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-text-tertiary" />
            <input
              type="text"
              placeholder="Rechercher par nom, catégorie, ville..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-12 pr-4 py-4 bg-white border border-border rounded-2xl focus:outline-none focus:ring-2 focus:ring-primary-500/30 text-lg"
            />
          </div>
        </div>

        <div className="mb-6 overflow-x-auto pb-2">
          <div className="flex gap-2">
            <button
              onClick={() => setQuickCategoryId(null)}
              className={`px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-all ${
                quickCategoryId === null
                  ? 'bg-primary-500 text-white'
                  : 'bg-white border border-border hover:border-primary-300 text-text-secondary'
              }`}
            >
              Toutes
            </button>
            {categories.map(cat => (
              <button
                key={cat.id}
                onClick={() => setQuickCategoryId(cat.id)}
                className={`px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-all ${
                  quickCategoryId === cat.id
                    ? 'bg-primary-500 text-white'
                    : 'bg-white border border-border hover:border-primary-300 text-text-secondary'
                }`}
              >
                {cat.name}
              </button>
            ))}
          </div>
        </div>

        <div className="flex flex-wrap gap-4 justify-between items-center mb-8">
          <div className="flex gap-3">
            <button
              onClick={() => setIsFilterOpen(true)}
              className="flex items-center gap-2 px-4 py-2 bg-white border border-border rounded-full hover:border-primary-300 transition-all"
            >
              <AdjustmentsHorizontalIcon className="w-5 h-5" />
              <span className="text-sm font-medium">Filtres avancés</span>
            </button>

            <div className="relative">
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="appearance-none px-4 py-2 bg-white border border-border rounded-full pr-10 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-primary-500/30"
              >
                <option value="relevance">Pertinence</option>
                <option value="rating">Meilleures notes</option>
                <option value="price_asc">Prix croissant</option>
                <option value="price_desc">Prix décroissant</option>
              </select>
              <ChevronDownIcon className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-tertiary pointer-events-none" />
            </div>
          </div>
        </div>

        {isLoading ? (
          <div className="flex justify-center items-center py-20">
            <div className="w-12 h-12 border-4 border-primary-200 border-t-primary-500 rounded-full animate-spin" />
          </div>
        ) : (
          <>
            <p className="text-text-secondary mb-4">
              {results.length} prestataires trouvés
            </p>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {results.map((prestataire, index) => (
                <PrestataireCard
                  key={prestataire.id}
                  prestataire={prestataire}
                  index={index}
                  categoryName={getCategoryName(prestataire.category_id)}
                />
              ))}
            </div>
          </>
        )}
      </Container>

      <FilterSidebar
        isOpen={isFilterOpen}
        onClose={() => setIsFilterOpen(false)}
        onApply={(newFilters) => {
          setQuickCategoryId(null);
          setFilters(prev => ({ ...prev, ...newFilters }));
        }}
        categories={categories}
        initialSelectedIds={filters.category_ids || []}
      />
    </div>
  );
}