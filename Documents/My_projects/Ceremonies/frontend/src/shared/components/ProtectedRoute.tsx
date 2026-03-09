import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../../features/auth/hooks/useAuth';

interface ProtectedRouteProps {
  allowedRoles?: Array<'client' | 'prestataire' | 'admin'>;
}

export function ProtectedRoute({ allowedRoles }: ProtectedRouteProps) {
  const { user, isInitialized } = useAuth();

  if (!isInitialized) {
    // Peut-être afficher un loader
    return <div className="flex justify-center items-center h-screen">Chargement...</div>;
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (allowedRoles) {
    const hasRole = allowedRoles.some(role => {
      if (role === 'admin' && user.is_admin) return true;
      if (role === 'prestataire' && user.is_prestataire) return true;
      if (role === 'client' && user.is_client) return true;
      return false;
    });
    if (!hasRole) {
      return <Navigate to="/" replace />;
    }
  }

  return <Outlet />;
}