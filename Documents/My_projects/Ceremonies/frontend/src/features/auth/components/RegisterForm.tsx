import { useState } from 'react';
import { motion } from 'framer-motion';
import { UserIcon, EnvelopeIcon, LockClosedIcon, EyeIcon, EyeSlashIcon } from '@heroicons/react/24/outline';
import { Button } from '../../../shared/components/ui/Button';
import { Input } from '../../../shared/components/ui/Input';

interface RegisterFormProps {
  onSubmit: (data: any, role: 'client' | 'prestataire') => void;
  isLoading?: boolean;
  error?: string | null;
}

export function RegisterForm({ onSubmit, isLoading, error }: RegisterFormProps) {
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    password: '',
  });
  const [role, setRole] = useState<'client' | 'prestataire'>('client');
  const [showPassword, setShowPassword] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData, role);
  };

  return (
    <motion.form
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      onSubmit={handleSubmit}
      className="space-y-6"
    >
      {/* Sélecteur de rôle */}
      <div className="grid grid-cols-2 gap-4 mb-4">
        <button
          type="button"
          onClick={() => setRole('client')}
          className={`p-4 rounded-xl border-2 transition-all ${
            role === 'client'
              ? 'border-primary-500 bg-primary-50'
              : 'border-border hover:border-primary-200'
          }`}
        >
          <span className={`font-medium ${role === 'client' ? 'text-primary-500' : 'text-text-secondary'}`}>
            Je suis organisateur
          </span>
          <p className="text-xs text-text-tertiary mt-1">Je cherche des prestataires</p>
        </button>
        <button
          type="button"
          onClick={() => setRole('prestataire')}
          className={`p-4 rounded-xl border-2 transition-all ${
            role === 'prestataire'
              ? 'border-primary-500 bg-primary-50'
              : 'border-border hover:border-primary-200'
          }`}
        >
          <span className={`font-medium ${role === 'prestataire' ? 'text-primary-500' : 'text-text-secondary'}`}>
            Je suis prestataire
          </span>
          <p className="text-xs text-text-tertiary mt-1">Je propose mes services</p>
        </button>
      </div>

      <div>
        <label htmlFor="full_name" className="block text-sm font-medium text-text-primary mb-2">
          Nom complet
        </label>
        <Input
          id="full_name"
          name="full_name"
          value={formData.full_name}
          onChange={handleChange}
          placeholder="Jean Dupont"
          icon={<UserIcon className="w-5 h-5" />}
          required
        />
      </div>

      <div>
        <label htmlFor="email" className="block text-sm font-medium text-text-primary mb-2">
          Email
        </label>
        <Input
          id="email"
          name="email"
          type="email"
          value={formData.email}
          onChange={handleChange}
          placeholder="vous@exemple.com"
          icon={<EnvelopeIcon className="w-5 h-5" />}
          required
        />
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium text-text-primary mb-2">
          Mot de passe
        </label>
        <div className="relative">
          <Input
            id="password"
            name="password"
            type={showPassword ? 'text' : 'password'}
            value={formData.password}
            onChange={handleChange}
            placeholder="••••••••"
            icon={<LockClosedIcon className="w-5 h-5" />}
            required
          />
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-text-tertiary hover:text-text-primary"
          >
            {showPassword ? <EyeSlashIcon className="w-5 h-5" /> : <EyeIcon className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {error && (
        <p className="text-sm text-red-500">{error}</p>
      )}

      <Button type="submit" variant="primary" fullWidth disabled={isLoading}>
        {isLoading ? 'Inscription...' : 'Créer mon compte'}
      </Button>

      <p className="text-center text-sm text-text-secondary">
        En vous inscrivant, vous acceptez nos{' '}
        <a href="/cgu" className="text-primary-500 hover:underline">
          conditions d'utilisation
        </a>
      </p>
    </motion.form>
  );
}