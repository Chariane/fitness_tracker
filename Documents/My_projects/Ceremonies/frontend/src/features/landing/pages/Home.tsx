import { motion, useScroll, useTransform, useSpring } from "framer-motion";
import { useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../auth/hooks/useAuth";
import { 
  SparklesIcon, 
  ArrowRightIcon, 
  CameraIcon, 
  CakeIcon,
  MusicalNoteIcon,
  BuildingOfficeIcon,
  HeartIcon,
  StarIcon,
  MapPinIcon,
  CalendarIcon,
  UsersIcon,
  ChatBubbleLeftRightIcon,
  ShieldCheckIcon,
  ChevronDownIcon,
  FireIcon
} from "@heroicons/react/24/outline";
import { StarIcon as StarIconSolid } from "@heroicons/react/24/solid";

// =============================================
// COMPOSANT 1 : PARTICULES DE LUMIÈRE
// =============================================
const LightParticles = () => {
  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {[...Array(30)].map((_, i) => (
        <motion.div
          key={i}
          className="absolute w-2 h-2 bg-gradient-to-r from-primary-300/30 to-gold-300/30 rounded-full blur-sm"
          initial={{
            x: Math.random() * (typeof window !== 'undefined' ? window.innerWidth : 1000),
            y: Math.random() * (typeof window !== 'undefined' ? window.innerHeight : 1000),
            scale: 0
          }}
          animate={{
            y: [null, -100, 100, -100],
            x: [null, 100, -100, 100],
            scale: [0, 1, 0.5, 0],
          }}
          transition={{
            duration: 15 + Math.random() * 10,
            repeat: Infinity,
            ease: "linear",
            delay: Math.random() * 5
          }}
          style={{
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 100}%`,
          }}
        />
      ))}
    </div>
  );
};

// =============================================
// COMPOSANT 2 : CARTE ÉVÉNEMENT FLOTTANTE
// =============================================
const FloatingEventCard = ({ delay, position, color, icon: Icon, name, role }: any) => {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.5, y: 50 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      transition={{ delay, duration: 0.8, type: "spring" }}
      whileHover={{ scale: 1.05, rotate: 2 }}
      className={`absolute ${position} glass-card rounded-2xl p-5 shadow-2xl backdrop-blur-md bg-white/90 border border-white/20 hidden lg:block`}
      style={{ zIndex: 20 }}
    >
      <div className="flex items-center gap-4">
        <div className={`w-14 h-14 rounded-xl bg-gradient-to-br ${color} flex items-center justify-center shadow-lg`}>
          <Icon className="w-7 h-7 text-white" />
        </div>
        <div>
          <div className="font-bold text-text-primary text-lg">{name}</div>
          <div className="text-sm text-text-secondary">{role}</div>
          <div className="flex items-center gap-1 mt-2">
            {[...Array(5)].map((_, i) => (
              <StarIconSolid key={i} className="w-3 h-3 text-gold-500" />
            ))}
          </div>
        </div>
      </div>
    </motion.div>
  );
};

// =============================================
// COMPOSANT 3 : STATS ANIMÉES
// =============================================
const AnimatedStat = ({ value, label, icon: Icon }: { value: string; label: string; icon: any }) => {
  const [count, setCount] = useState(0);
  const numericValue = parseInt(value.replace('+', '').replace('k', '000').replace('.', ''));
  const ref = useRef(null);
  const isInView = useInView(ref);

  useEffect(() => {
    if (isInView) {
      let start = 0;
      const end = numericValue;
      const duration = 2000;
      const increment = end / (duration / 16);
      
      const timer = setInterval(() => {
        start += increment;
        if (start >= end) {
          setCount(end);
          clearInterval(timer);
        } else {
          setCount(Math.floor(start));
        }
      }, 16);
      
      return () => clearInterval(timer);
    }
  }, [isInView, numericValue]);

  const displayValue = value.includes('k') 
    ? `${(count / 1000).toFixed(1)}k+`
    : value.includes('.') 
      ? (count / 10).toFixed(1)
      : `${count}+`;

  return (
    <motion.div
      ref={ref}
      whileHover={{ y: -5 }}
      className="text-center"
    >
      <div className="flex justify-center mb-2">
        <div className="w-12 h-12 bg-primary-100 rounded-xl flex items-center justify-center">
          <Icon className="w-6 h-6 text-primary-500" />
        </div>
      </div>
      <div className="text-3xl font-bold text-primary-500">{displayValue}</div>
      <div className="text-sm text-text-secondary">{label}</div>
    </motion.div>
  );
};

// =============================================
// COMPOSANT 4 : SECTION PRESTATAIRE
// =============================================
const PrestataireCard = ({ prestataire, index }: { prestataire: any; index: number }) => {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <motion.div
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ delay: index * 0.1, duration: 0.6 }}
      whileHover={{ y: -10 }}
      onHoverStart={() => setIsHovered(true)}
      onHoverEnd={() => setIsHovered(false)}
      className="group relative bg-white rounded-3xl overflow-hidden shadow-soft hover:shadow-strong transition-all duration-500"
    >
      <Link to={`/prestataire/${prestataire.id}`}>
        {/* Image avec overlay animé */}
        <div className="relative h-72 overflow-hidden">
          <motion.img
            src={prestataire.image}
            alt={prestataire.name}
            className="w-full h-full object-cover"
            animate={{ scale: isHovered ? 1.1 : 1 }}
            transition={{ duration: 0.6 }}
          />
          <motion.div 
            className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"
            animate={{ opacity: isHovered ? 0.8 : 0.5 }}
          />
          
          {/* Badge flottant */}
          <motion.div
            initial={{ x: 100, opacity: 0 }}
            animate={{ x: isHovered ? 0 : 100, opacity: isHovered ? 1 : 0 }}
            className="absolute top-4 right-4"
          >
            <span className={`px-4 py-2 rounded-full text-sm font-semibold ${
              prestataire.badge === "Premium" 
                ? "bg-gradient-to-r from-gold-400 to-gold-500 text-white"
                : prestataire.badge === "Vérifié"
                ? "bg-green-500 text-white"
                : "bg-primary-500 text-white"
            }`}>
              {prestataire.badge}
            </span>
          </motion.div>

          {/* Prix */}
          <div className="absolute bottom-4 left-4 text-white font-bold text-lg">
            {prestataire.price}
          </div>
        </div>

        {/* Contenu */}
        <div className="p-6">
          <div className="flex justify-between items-start mb-3">
            <div>
              <h3 className="text-xl font-bold text-text-primary">{prestataire.name}</h3>
              <p className="text-text-secondary">{prestataire.category}</p>
            </div>
            <div className="flex items-center gap-1">
              <StarIconSolid className="w-5 h-5 text-gold-500" />
              <span className="font-bold">{prestataire.rating}</span>
            </div>
          </div>

          <div className="flex items-center gap-3 text-text-secondary text-sm mb-4">
            <div className="flex items-center gap-1">
              <MapPinIcon className="w-4 h-4" />
              <span>{prestataire.location}</span>
            </div>
            <span>•</span>
            <span>{prestataire.reviews} avis</span>
          </div>

          <div className="flex items-center gap-2 mb-4">
            <span className="px-3 py-1 bg-primary-50 text-primary-600 rounded-full text-xs font-medium">
              {prestataire.specialty}
            </span>
            <span className="px-3 py-1 bg-gold-50 text-gold-600 rounded-full text-xs font-medium">
              {prestataire.events} événements
            </span>
          </div>

          <motion.button
            whileHover={{ x: 5 }}
            className="text-primary-500 font-semibold flex items-center gap-2 group"
            onClick={(e) => e.preventDefault()} // le lien englobe déjà
          >
            Voir le profil
            <ArrowRightIcon className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </motion.button>
        </div>
      </Link>

      {/* Éléments décoratifs au hover */}
      {isHovered && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="absolute -top-20 -right-20 w-40 h-40 bg-primary-200/20 rounded-full blur-3xl"
          />
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="absolute -bottom-20 -left-20 w-40 h-40 bg-gold-200/20 rounded-full blur-3xl"
          />
        </>
      )}
    </motion.div>
  );
};

// =============================================
// COMPOSANT 5 : TÉMOIGNAGE
// =============================================
const TestimonialCard = ({ testimonial, index }: { testimonial: any; index: number }) => {
  return (
    <motion.div
      initial={{ opacity: 0, x: index % 2 === 0 ? -50 : 50 }}
      whileInView={{ opacity: 1, x: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.8 }}
      className="bg-white rounded-3xl p-8 shadow-soft hover:shadow-medium transition-all duration-300"
    >
      <div className="flex items-center gap-4 mb-6">
        <img 
          src={testimonial.image} 
          alt={testimonial.name}
          className="w-16 h-16 rounded-full object-cover"
        />
        <div>
          <h4 className="font-bold text-text-primary">{testimonial.name}</h4>
          <p className="text-sm text-text-secondary">{testimonial.role}</p>
          <div className="flex gap-1 mt-2">
            {[...Array(testimonial.rating)].map((_, i) => (
              <StarIconSolid key={i} className="w-4 h-4 text-gold-500" />
            ))}
          </div>
        </div>
      </div>
      <p className="text-text-secondary italic">"{testimonial.content}"</p>
    </motion.div>
  );
};

// =============================================
// HOOK PERSONNALISÉ
// =============================================
function useInView(ref: any) {
  const [isInView, setIsInView] = useState(false);

  useEffect(() => {
    if (!ref.current) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        setIsInView(entry.isIntersecting);
      },
      { threshold: 0.1 }
    );

    observer.observe(ref.current);
    return () => observer.disconnect();
  }, [ref]);

  return isInView;
}

// =============================================
// PAGE PRINCIPALE
// =============================================
export default function Home() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const heroRef = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll();
  const smoothProgress = useSpring(scrollYProgress, { damping: 20, stiffness: 100 });
  
  const heroOpacity = useTransform(smoothProgress, [0, 0.3], [1, 0]);
  const heroY = useTransform(smoothProgress, [0, 0.3], [0, -100]);
  const scale = useTransform(smoothProgress, [0, 0.3], [1, 0.95]);

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (heroRef.current) {
        const rect = heroRef.current.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width - 0.5;
        const y = (e.clientY - rect.top) / rect.height - 0.5;
        setMousePosition({ x, y });
      }
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  const handleBecomePrestataire = () => {
    if (user) {
      navigate("/become-prestataire");
    } else {
      navigate("/register?role=prestataire");
    }
  };

  const categories = [
    { 
      name: "Photographes", 
      icon: CameraIcon, 
      count: 234, 
      color: "from-primary-400 to-primary-500",
      description: "Immortalisez vos plus beaux moments"
    },
    { 
      name: "Traiteurs", 
      icon: CakeIcon, 
      count: 156, 
      color: "from-gold-400 to-gold-500",
      description: "Une cuisine d'exception"
    },
    { 
      name: "DJs & Musiciens", 
      icon: MusicalNoteIcon, 
      count: 89, 
      color: "from-purple-400 to-purple-500",
      description: "L'ambiance parfaite"
    },
    { 
      name: "Salles", 
      icon: BuildingOfficeIcon, 
      count: 112, 
      color: "from-emerald-400 to-emerald-500",
      description: "Des lieux de rêve"
    },
  ];

  const featuredprestataires = [
    {
      id: 1,
      name: "Sophie Martin",
      category: "Photographe",
      location: "Lyon",
      rating: 4.9,
      reviews: 128,
      image: "https://images.unsplash.com/photo-1494790108777-467efad0c2d0?w=800&auto=format",
      badge: "Premium",
      price: "À partir de 1200€",
      verified: true,
      specialty: "Mariage & Portrait",
      events: 45
    },
    {
      id: 2,
      name: "Traiteur Lyonnais",
      category: "Traiteur",
      location: "Lyon",
      rating: 4.8,
      reviews: 256,
      image: "https://images.unsplash.com/photo-1566492031773-4f4e44671857?w=800&auto=format",
      badge: "Vérifié",
      price: "À partir de 45€/pers",
      verified: true,
      specialty: "Cuisine traditionnelle",
      events: 120
    },
    {
      id: 3,
      name: "DJ Pulse",
      category: "DJ",
      location: "Paris",
      rating: 4.9,
      reviews: 89,
      image: "https://images.unsplash.com/photo-1516280440614-37939bbacd81?w=800&auto=format",
      badge: "Premium",
      price: "À partir de 800€",
      verified: true,
      specialty: "Électro & Lounge",
      events: 67
    },
    {
      id: 4,
      name: "Déco & Co",
      category: "Décoration",
      location: "Bordeaux",
      rating: 4.7,
      reviews: 64,
      image: "https://images.unsplash.com/photo-1532375810709-75b1da00537c?w=800&auto=format",
      badge: "Nouveau",
      price: "Sur devis",
      verified: false,
      specialty: "Décoration florale",
      events: 23
    }
  ];

  const testimonials = [
    {
      name: "Marie & Thomas",
      role: "Mariage - Juin 2024",
      content: "Grâce à Cérémonies, nous avons trouvé la photographe et le traiteur parfaits pour notre mariage. Une expérience fluide et des professionnels exceptionnels.",
      rating: 5,
      image: "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?w=200&auto=format"
    },
    {
      name: "Sophie Dubois",
      role: "Anniversaire - 50 ans",
      content: "Je recommande à 100% ! Le DJ était incroyable et la mise en relation s'est faite en quelques clics. La plateforme est magnifique et intuitive.",
      rating: 5,
      image: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=200&auto=format"
    },
    {
      name: "Pierre Martin",
      role: "Séminaire d'entreprise",
      content: "Une sélection de prestataires de très haute qualité. Notre salle était parfaite et le traiteur a régalé tous nos invités.",
      rating: 5,
      image: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=200&auto=format"
    }
  ];

  const stats = [
    { value: "500+", label: "Prestataires vérifiés", icon: ShieldCheckIcon },
    { value: "10k+", label: "Événements organisés", icon: CalendarIcon },
    { value: "4.9", label: "Note moyenne", icon: StarIcon },
    { value: "15k+", label: "Utilisateurs actifs", icon: UsersIcon },
  ];

  return (
    <div className="min-h-screen bg-background overflow-x-hidden">
      <LightParticles />

      {/* SECTION 1 : HERO */}
      <section 
        ref={heroRef}
        className="relative min-h-screen flex items-center justify-center overflow-hidden"
      >
        {/* Background cinématique */}
        <motion.div
          style={{
            x: mousePosition.x * 30,
            y: mousePosition.y * 30,
          }}
          className="absolute inset-0"
        >
          <div className="absolute inset-0 bg-gradient-to-br from-primary-100/30 via-background to-gold-100/30" />
          
          {/* Cercles lumineux animés */}
          <motion.div
            animate={{
              scale: [1, 1.3, 1],
              rotate: [0, 180, 360],
            }}
            transition={{
              duration: 25,
              repeat: Infinity,
              ease: "linear",
            }}
            className="absolute top-1/4 left-1/4 w-[600px] h-[600px] bg-primary-300/20 rounded-full blur-3xl"
          />
          <motion.div
            animate={{
              scale: [1, 1.2, 1],
              rotate: [0, -180, -360],
            }}
            transition={{
              duration: 20,
              repeat: Infinity,
              ease: "linear",
            }}
            className="absolute bottom-1/4 right-1/4 w-[500px] h-[500px] bg-gold-300/20 rounded-full blur-3xl"
          />
          
          {/* Grille décorative */}
          <div className="absolute inset-0 opacity-10">
            <div className="absolute inset-0" style={{
              backgroundImage: `
                linear-gradient(rgba(224, 107, 94, 0.1) 1px, transparent 1px),
                linear-gradient(90deg, rgba(224, 107, 94, 0.1) 1px, transparent 1px)
              `,
              backgroundSize: '50px 50px'
            }} />
          </div>
        </motion.div>

        {/* Cartes flottantes événementielles */}
        <FloatingEventCard 
          delay={0.2} 
          position="top-32 left-16" 
          color="from-primary-400 to-primary-500"
          icon={CameraIcon}
          name="Sophie Martin"
          role="Photographe"
        />
        <FloatingEventCard 
          delay={0.4} 
          position="bottom-32 right-16" 
          color="from-gold-400 to-gold-500"
          icon={CakeIcon}
          name="Traiteur Lyonnais"
          role="Traiteur"
        />
        <FloatingEventCard 
          delay={0.6} 
          position="top-48 right-32" 
          color="from-purple-400 to-purple-500"
          icon={MusicalNoteIcon}
          name="DJ Pulse"
          role="DJ"
        />

        {/* Contenu principal */}
        <motion.div
          style={{ opacity: heroOpacity, y: heroY, scale }}
          className="relative z-30 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-32 text-center"
        >
          {/* Badge premium */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            whileHover={{ scale: 1.05 }}
            className="inline-flex items-center gap-2 px-6 py-3 glass-card rounded-full mb-8 backdrop-blur-md border border-white/20 shadow-xl"
          >
            <FireIcon className="w-5 h-5 text-primary-500" />
            <span className="text-sm font-medium text-text-secondary">
              Plus de 500 prestataires d'exception
            </span>
            <SparklesIcon className="w-4 h-4 text-gold-500" />
          </motion.div>

          {/* Titre principal avec animation de lettres */}
          <motion.h1
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 1 }}
            className="text-7xl md:text-9xl font-bold mb-8 leading-[0.9]"
          >
            {"Créez l'exception".split('').map((char, index) => (
              <motion.span
                key={index}
                initial={{ opacity: 0, y: 50 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.03 }}
                className="inline-block hover:text-primary-500 transition-colors duration-300"
                whileHover={{ scale: 1.1, rotate: 5 }}
              >
                {char === ' ' ? '\u00A0' : char}
              </motion.span>
            ))}
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.5 }}
            className="text-2xl text-text-secondary max-w-3xl mx-auto mb-12"
          >
            Photographes, traiteurs, DJs, décorateurs... Une sélection 
            <span className="text-primary-500 font-semibold"> exclusive </span> 
            de professionnels pour des moments inoubliables.
          </motion.p>

          {/* CTA */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.7 }}
            className="flex flex-col sm:flex-row gap-6 justify-center items-center"
          >
            <Link to="/search">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="group relative px-10 py-5 bg-gradient-to-r from-primary-500 to-gold-500 text-white rounded-full text-lg font-semibold shadow-2xl shadow-primary-500/30 overflow-hidden"
              >
                <span className="relative z-10 flex items-center gap-3">
                  Commencer l'aventure
                  <ArrowRightIcon className="w-5 h-5 group-hover:translate-x-2 transition-transform" />
                </span>
                <motion.div
                  className="absolute inset-0 bg-gradient-to-r from-primary-600 to-gold-600"
                  initial={{ x: '100%' }}
                  whileHover={{ x: 0 }}
                  transition={{ duration: 0.3 }}
                />
              </motion.button>
            </Link>

            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleBecomePrestataire}
              className="px-10 py-5 bg-white text-text-primary rounded-full text-lg font-semibold shadow-xl hover:shadow-2xl transition-all border-2 border-primary-200"
            >
              Devenir prestataire
            </motion.button>
          </motion.div>

          {/* Indicateur de scroll */}
          <motion.div
            animate={{ y: [0, 10, 0] }}
            transition={{ duration: 2, repeat: Infinity }}
            className="absolute bottom-10 left-1/2 -translate-x-1/2 cursor-pointer"
            onClick={() => window.scrollTo({ top: window.innerHeight, behavior: 'smooth' })}
          >
            <div className="w-6 h-10 border-2 border-primary-300 rounded-full flex justify-center">
              <motion.div
                animate={{ y: [0, 12, 0] }}
                transition={{ duration: 1.5, repeat: Infinity }}
                className="w-1.5 h-3 bg-primary-400 rounded-full mt-2"
              />
            </div>
          </motion.div>
        </motion.div>
      </section>

      {/* SECTION 2 : STATISTIQUES */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <AnimatedStat key={index} {...stat} />
            ))}
          </div>
        </div>
      </section>

      {/* SECTION 3 : CATÉGORIES */}
      <section className="py-20 bg-gradient-to-b from-background to-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-5xl font-bold mb-4">
              Parcourez par <span className="text-gradient-primary">catégorie</span>
            </h2>
            <p className="text-xl text-text-secondary max-w-3xl mx-auto">
              Des professionnels spécialisés dans chaque domaine de l'événementiel
            </p>
          </motion.div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {categories.map((cat, index) => (
              <motion.div
                key={cat.name}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ y: -10, scale: 1.02 }}
                className="group cursor-pointer"
              >
                <Link to={`/search?category=${cat.name}`}>
                  <div className="bg-white rounded-3xl p-8 shadow-soft hover:shadow-strong transition-all duration-300 text-center border border-border/50">
                    <motion.div 
                      className={`w-20 h-20 rounded-2xl bg-gradient-to-br ${cat.color} p-5 mx-auto mb-5`}
                      whileHover={{ rotate: 360 }}
                      transition={{ duration: 0.6 }}
                    >
                      <cat.icon className="w-full h-full text-white" />
                    </motion.div>
                    <h3 className="text-xl font-bold text-text-primary mb-2">{cat.name}</h3>
                    <p className="text-text-secondary text-sm mb-3">{cat.description}</p>
                    <p className="text-primary-500 font-semibold">{cat.count} prestataires</p>
                  </div>
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* SECTION 4 : PRESTATAIRES À LA UNE */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-5xl font-bold mb-4">
              Prestataires <span className="text-gradient-primary">d'exception</span>
            </h2>
            <p className="text-xl text-text-secondary max-w-3xl mx-auto">
              Une sélection rigoureuse des meilleurs professionnels
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {featuredprestataires.map((prestataire, index) => (
              <PrestataireCard key={prestataire.id} prestataire={prestataire} index={index} />
            ))}
          </div>

          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-center mt-12"
          >
            <Link to="/search">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="px-8 py-4 bg-transparent border-2 border-primary-500 text-primary-500 rounded-full font-semibold hover:bg-primary-50 transition-all inline-flex items-center gap-2"
              >
                Voir tous les prestataires
                <ArrowRightIcon className="w-5 h-5" />
              </motion.button>
            </Link>
          </motion.div>
        </div>
      </section>

      {/* SECTION 5 : TÉMOIGNAGES */}
      <section className="py-20 bg-gradient-to-b from-white to-background">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-5xl font-bold mb-4">
              Ils nous <span className="text-gradient-primary">font confiance</span>
            </h2>
            <p className="text-xl text-text-secondary max-w-3xl mx-auto">
              Des milliers d'organisateurs ont déjà trouvé leurs prestataires
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-6">
            {testimonials.map((testimonial, index) => (
              <TestimonialCard key={index} testimonial={testimonial} index={index} />
            ))}
          </div>
        </div>
      </section>

      {/* SECTION 6 : CTA FINAL */}
      <section className="py-32 relative overflow-hidden">
        <div className="absolute inset-0">
          <motion.div
            animate={{
              scale: [1, 1.2, 1],
              rotate: [0, 45, 0],
            }}
            transition={{
              duration: 15,
              repeat: Infinity,
              ease: "linear",
            }}
            className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-gradient-to-r from-primary-300/20 to-gold-300/20 rounded-full blur-3xl"
          />
        </div>

        <div className="relative max-w-4xl mx-auto text-center px-4">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-6xl md:text-7xl font-bold mb-6"
          >
            Prêt à créer
            <br />
            <span className="text-gradient-primary">l'inoubliable ?</span>
          </motion.h2>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="text-2xl text-text-secondary mb-12"
          >
            Rejoignez la communauté et donnez vie à vos plus beaux projets
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="flex flex-col sm:flex-row gap-6 justify-center"
          >
            <Link to="/marketplace">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="px-12 py-5 bg-gradient-to-r from-primary-500 to-gold-500 text-white rounded-full text-xl font-semibold shadow-2xl shadow-primary-500/30"
              >
                Commencer maintenant
              </motion.button>
            </Link>
            <Link to="/contact">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="px-12 py-5 bg-white text-text-primary rounded-full text-xl font-semibold shadow-xl border-2 border-primary-200"
              >
                Nous contacter
              </motion.button>
            </Link>
          </motion.div>

          {/* Petites bulles décoratives */}
          {[...Array(5)].map((_, i) => (
            <motion.div
              key={i}
              className="absolute w-2 h-2 bg-primary-300/50 rounded-full"
              animate={{
                y: [0, -30, 0],
                x: [0, 20, 0],
              }}
              transition={{
                duration: 3 + i,
                repeat: Infinity,
                delay: i * 0.5,
              }}
              style={{
                left: `${10 + i * 20}%`,
                bottom: '20%',
              }}
            />
          ))}
        </div>
      </section>

      {/* Bouton flottant pour remonter */}
      <motion.button
        className="fixed bottom-8 right-8 w-12 h-12 bg-primary-500 rounded-full shadow-lg flex items-center justify-center text-white z-50"
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 2 }}
      >
        <ChevronDownIcon className="w-6 h-6 rotate-180" />
      </motion.button>
    </div>
  );
}