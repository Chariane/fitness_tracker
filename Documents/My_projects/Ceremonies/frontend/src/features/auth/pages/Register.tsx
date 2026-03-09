import { Link } from 'react-router-dom';
import { Container } from '../../../shared/components/ui/Container';
import { RegisterForm } from '../components/RegisterForm';
import { useAuth } from '../hooks/useAuth';

export default function RegisterPage() {
  const { register, isLoading, error } = useAuth();

  const handleRegister = (data: any, role: 'client' | 'prestataire') => {
    // data contient full_name, email, password, phone
    register(data, role);
  };

  return (
    <div className="min-h-screen bg-background pt-24 pb-16">
      <Container size="sm">
        <div className="text-center mb-8">
          <Link to="/" className="inline-block mb-6">
            <span className="text-3xl font-bold text-gradient-primary">Cérémonies</span>
          </Link>
          <h1 className="text-3xl font-bold text-text-primary mb-2">
            Créez votre compte
          </h1>
          <p className="text-text-secondary">
            Rejoignez la communauté et trouvez les meilleurs prestataires
          </p>
        </div>

        <div className="bg-white rounded-2xl p-8 shadow-soft">
          <RegisterForm onSubmit={handleRegister} isLoading={isLoading} error={error} />

          <div className="mt-6 text-center">
            <p className="text-text-secondary">
              Déjà inscrit ?{' '}
              <Link to="/login" className="text-primary-500 hover:underline font-medium">
                Connectez-vous
              </Link>
            </p>
          </div>
        </div>
      </Container>
    </div>
  );
}