import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../../../features/auth/hooks/useAuth';
import {
  MagnifyingGlassIcon,
  UserIcon,
  BellIcon,
  ChevronDownIcon,
  HeartIcon,
  ChatBubbleLeftRightIcon,
} from '@heroicons/react/24/outline';
import { Container } from '../ui/Container';
import { Button } from '../ui/Button';
import { prestataireFavoritesApi } from '../../api/prestataireFavorites'; // à créer

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const navigation = [
  { name: 'Accueil', href: '/' },
  { name: 'Prestataires', href: '/search' },
  { name: 'Offres', href: '/marketplace' },
  { name: 'Comment ça marche', href: '/how-it-works' },
  { name: 'Inspirations', href: '/inspirations' },
];

export function Header() {
  const { user, logout } = useAuth();
  const [scrolled, setScrolled] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const [favoriteCount, setFavoriteCount] = useState(0);
  const location = useLocation();

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (isProfileOpen && !(e.target as Element).closest('.profile-menu')) {
        setIsProfileOpen(false);
      }
    };
    document.addEventListener('click', handleClickOutside);
    return () => document.removeEventListener('click', handleClickOutside);
  }, [isProfileOpen]);

  // Charger le nombre de favoris quand l'utilisateur est connecté
  useEffect(() => {
    if (user) {
      prestataireFavoritesApi.getCount()
        .then(res => setFavoriteCount(res.data.count))
        .catch(err => console.error("Erreur chargement favoris", err));
    } else {
      setFavoriteCount(0);
    }
  }, [user]);

  const getInitials = () => {
    if (!user?.full_name) return 'U';
    return user.full_name.split(' ').map(n => n[0]).join('').toUpperCase();
  };

  return (
    <motion.header
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.6 }}
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled ? 'bg-white/90 backdrop-blur-xl border-b border-border shadow-soft' : 'bg-transparent'
      }`}
    >
      <Container>
        <div className="flex items-center justify-between h-20">
          <Link to="/" className="relative z-10">
            <span className="text-2xl font-bold">
              <span className="text-gradient-primary">Céré</span>
              <span className="text-text-primary">monies</span>
            </span>
          </Link>

          <nav className="hidden md:flex items-center gap-8">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href;
              return (
                <Link key={item.name} to={item.href} className="relative group">
                  <span className={`text-sm font-medium transition-colors ${
                    isActive ? 'text-primary-500' : 'text-text-secondary hover:text-text-primary'
                  }`}>
                    {item.name}
                  </span>
                  {isActive && (
                    <motion.div
                      layoutId="activeNav"
                      className="absolute -bottom-1 left-0 right-0 h-0.5 bg-gradient-to-r from-primary-500 to-gold-500"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ duration: 0.3 }}
                    />
                  )}
                </Link>
              );
            })}
          </nav>

          <div className="flex items-center gap-4">
            {user ? (
              <div className="flex items-center gap-3">
                <Link to="/favorites" className="relative p-2 hover:bg-primary-50 rounded-full transition-colors">
                  <HeartIcon className="w-5 h-5 text-text-secondary" />
                  {favoriteCount > 0 && (
                    <span className="absolute -top-1 -right-1 w-4 h-4 bg-primary-500 text-white text-xs rounded-full flex items-center justify-center">
                      {favoriteCount > 9 ? '9+' : favoriteCount}
                    </span>
                  )}
                </Link>

                <Link to="/messages" className="relative p-2 hover:bg-primary-50 rounded-full transition-colors">
                  <ChatBubbleLeftRightIcon className="w-5 h-5 text-text-secondary" />
                  <span className="absolute -top-1 -right-1 w-4 h-4 bg-primary-500 text-white text-xs rounded-full flex items-center justify-center">
                    5
                  </span>
                </Link>

                <button className="relative p-2 hover:bg-primary-50 rounded-full transition-colors">
                  <BellIcon className="w-5 h-5 text-text-secondary" />
                  <span className="absolute top-1 right-1 w-2 h-2 bg-primary-500 rounded-full animate-pulse" />
                </button>

                <div className="relative profile-menu">
                  <button
                    onClick={() => setIsProfileOpen(!isProfileOpen)}
                    className="flex items-center gap-2 p-1 hover:bg-primary-50 rounded-full transition-colors"
                  >
                    {user.avatar_url ? (
                      <img
                        src={`${API_URL}${user.avatar_url}`}
                        alt={user.full_name || "Avatar"}
                        className="w-9 h-9 rounded-full object-cover"
                      />
                    ) : (
                      <div className="w-9 h-9 rounded-full bg-gradient-to-br from-primary-400 to-gold-400 flex items-center justify-center text-white font-medium">
                        {getInitials()}
                      </div>
                    )}
                    <ChevronDownIcon className={`w-4 h-4 text-text-secondary transition-transform duration-200 ${
                      isProfileOpen ? 'rotate-180' : ''
                    }`} />
                  </button>

                  {isProfileOpen && (
                    <motion.div
                      initial={{ opacity: 0, y: -10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -10 }}
                      className="absolute right-0 mt-2 w-64 bg-white rounded-2xl shadow-strong border border-border overflow-hidden"
                    >
                      <div className="p-4 bg-gradient-to-r from-primary-50 to-gold-50 border-b border-border">
                        <p className="font-semibold text-text-primary">{user.full_name || 'Utilisateur'}</p>
                        <p className="text-sm text-text-secondary">{user.email}</p>
                        {user.is_prestataire && (
                          <span className="inline-block mt-2 text-xs text-primary-600 bg-primary-100 px-2 py-1 rounded-full">Prestataire</span>
                        )}
                        {user.is_admin && (
                          <span className="inline-block mt-2 text-xs text-purple-600 bg-purple-100 px-2 py-1 rounded-full">Admin</span>
                        )}
                      </div>
                      <div className="p-2">
                        {user.is_prestataire ? (
                          <Link to="/prestataire/dashboard" className="flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-surface-alt transition-colors" onClick={() => setIsProfileOpen(false)}>
                            <UserIcon className="w-5 h-5 text-text-secondary" />
                            <span className="text-sm font-medium">Dashboard</span>
                          </Link>
                        ) : user.is_client ? (
                          <Link to="/dashboard" className="flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-surface-alt transition-colors" onClick={() => setIsProfileOpen(false)}>
                            <UserIcon className="w-5 h-5 text-text-secondary" />
                            <span className="text-sm font-medium">Dashboard</span>
                          </Link>
                        ) : null}
                        {user.is_admin && (
                          <Link to="/admin" className="flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-surface-alt transition-colors" onClick={() => setIsProfileOpen(false)}>
                            <UserIcon className="w-5 h-5 text-text-secondary" />
                            <span className="text-sm font-medium">Admin</span>
                          </Link>
                        )}
                        <Link to="/profile/edit" className="flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-surface-alt transition-colors" onClick={() => setIsProfileOpen(false)}>
                          <UserIcon className="w-5 h-5 text-text-secondary" />
                          <span className="text-sm font-medium">Mon profil</span>
                        </Link>
                        <Link to="/settings" className="flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-surface-alt transition-colors" onClick={() => setIsProfileOpen(false)}>
                          <UserIcon className="w-5 h-5 text-text-secondary" />
                          <span className="text-sm font-medium">Paramètres</span>
                        </Link>
                        <div className="border-t border-border my-2" />
                        <button
                          onClick={() => {
                            setIsProfileOpen(false);
                            logout();
                          }}
                          className="w-full flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-surface-alt text-red-500 transition-colors text-left"
                        >
                          <span className="text-sm font-medium">Déconnexion</span>
                        </button>
                      </div>
                    </motion.div>
                  )}
                </div>
              </div>
            ) : (
              <div className="flex items-center gap-3">
                <Link to="/login">
                  <Button variant="ghost" size="sm">Connexion</Button>
                </Link>
                <Link to="/register">
                  <Button variant="primary" size="sm">Inscription</Button>
                </Link>
              </div>
            )}

            <button onClick={() => setIsOpen(!isOpen)} className="md:hidden p-2 hover:bg-surface-alt rounded-lg transition-colors">
              <div className="w-5 h-4 relative flex flex-col justify-between">
                <span className={`w-full h-0.5 bg-text-primary transition-transform ${isOpen ? 'rotate-45 translate-y-1.5' : ''}`} />
                <span className={`w-full h-0.5 bg-text-primary transition-opacity ${isOpen ? 'opacity-0' : ''}`} />
                <span className={`w-full h-0.5 bg-text-primary transition-transform ${isOpen ? '-rotate-45 -translate-y-1.5' : ''}`} />
              </div>
            </button>
          </div>
        </div>

        {isOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden py-4 border-t border-border"
          >
            <nav className="flex flex-col gap-2">
              {navigation.map((item) => (
                <Link key={item.name} to={item.href} className="px-4 py-2 hover:bg-surface-alt rounded-lg transition-colors" onClick={() => setIsOpen(false)}>
                  {item.name}
                </Link>
              ))}
            </nav>
          </motion.div>
        )}
      </Container>
    </motion.header>
  );
}