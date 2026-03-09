import { Container } from '../../../shared/components/ui/Container';
import { Card } from '../../../shared/components/ui/Card';
import { ClockIcon } from '@heroicons/react/24/outline';

export default function PendingApprovalPage() {
  return (
    <div className="min-h-screen bg-background pt-24 pb-16">
      <Container size="sm">
        <Card className="p-8 text-center">
          <ClockIcon className="w-16 h-16 text-primary-500 mx-auto mb-4" />
          <h1 className="text-2xl font-bold text-text-primary mb-2">
            Demande en cours de vérification
          </h1>
          <p className="text-text-secondary mb-6">
            Votre demande pour devenir prestataire a bien été reçue. 
            Notre équipe examine vos documents et vous recevrez une confirmation par email sous 48h.
          </p>
          <p className="text-sm text-text-tertiary">
            En attendant, vous pouvez continuer à utiliser la plateforme en tant qu'organisateur.
          </p>
        </Card>
      </Container>
    </div>
  );
}