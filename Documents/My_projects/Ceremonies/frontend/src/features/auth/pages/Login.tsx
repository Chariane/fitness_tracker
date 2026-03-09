import { Link } from 'react-router-dom';
import { Container } from '../../../shared/components/ui/Container';
import { LoginForm } from '../components/LoginForm';
import { useAuth } from '../hooks/useAuth';

export default function LoginPage() {
  const { login, isLoading, error } = useAuth();

  const handleLogin = (email: string, password: string) => {
    login({ email, password });
  };

  return (
    <div className="min-h-screen bg-background pt-24 pb-16">
      <Container size="sm">
        <div className="text-center mb-8">
          <Link to="/" className="inline-block mb-6">
            <span className="text-3xl font-bold text-gradient-primary">Cérémonies</span>
          </Link>
          <h1 className="text-3xl font-bold text-text-primary mb-2">
            Content de vous revoir
          </h1>
          <p className="text-text-secondary">
            Connectez-vous pour accéder à votre espace
          </p>
        </div>

        <div className="bg-white rounded-2xl p-8 shadow-soft">
          <LoginForm onSubmit={handleLogin} isLoading={isLoading} error={error} />

          <div className="mt-6 text-center">
            <p className="text-text-secondary">
              Pas encore de compte ?{' '}
              <Link to="/register" className="text-primary-500 hover:underline font-medium">
                Inscrivez-vous
              </Link>
            </p>
          </div>
        </div>
      </Container>
    </div>
  );
}