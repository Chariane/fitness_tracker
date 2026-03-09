import { Container } from '../../../shared/components/ui/Container';
import { BecomePrestataireForm } from '../components/BecomePrestataireForm';

export default function BecomePrestatairePage() {
  return (
    <div className="min-h-screen bg-background pt-24 pb-16">
      <Container size="md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-text-primary mb-2">
            Complétez votre profil prestataire
          </h1>
          <p className="text-text-secondary">
            Dernière étape pour commencer à recevoir des demandes de clients
          </p>
        </div>

        <div className="bg-white rounded-2xl p-8 shadow-soft">
          <BecomePrestataireForm />
        </div>
      </Container>
    </div>
  );
}