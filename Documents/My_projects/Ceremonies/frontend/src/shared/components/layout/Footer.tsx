import { Link } from "react-router-dom";
import { Container } from "../ui/Container";
import { 
  HeartIcon,
  SparklesIcon,
  ShieldCheckIcon,
  ChatBubbleLeftRightIcon
} from "@heroicons/react/24/outline";

const footerLinks = {
  plateforme: [
    { name: "Prestataires", href: "/search" },
    { name: "Comment ça marche", href: "/how-it-works" },
    { name: "Tarifs", href: "/pricing" },
    { name: "FAQ", href: "/faq" },
  ],
  legal: [
    { name: "CGU", href: "/terms" },
    { name: "Confidentialité", href: "/privacy" },
    { name: "Mentions légales", href: "/legal" },
    { name: "Cookies", href: "/cookies" },
  ],
  entreprise: [
    { name: "À propos", href: "/about" },
    { name: "Blog", href: "/blog" },
    { name: "Carrières", href: "/careers" },
    { name: "Contact", href: "/contact" },
  ]
};

const socialLinks = [
  { name: "Instagram", icon: "📸", href: "#" },
  { name: "Facebook", icon: "👥", href: "#" },
  { name: "Pinterest", icon: "📌", href: "#" },
  { name: "LinkedIn", icon: "💼", href: "#" },
];

export function Footer() {
  return (
    <footer className="bg-white border-t border-border mt-auto">
      <Container className="py-16">
        {/* Main footer */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-12 mb-16">
          {/* Brand */}
          <div className="lg:col-span-2">
            <Link to="/" className="inline-block mb-4">
              <span className="text-2xl font-bold">
                <span className="text-gradient-primary">Céré</span>
                <span className="text-text-primary">monies</span>
              </span>
            </Link>
            <p className="text-text-secondary text-sm mb-6 max-w-sm">
              La plateforme qui connecte organisateurs et prestataires d'exception 
              pour des événements inoubliables.
            </p>
            
            {/* Stats mini */}
            <div className="flex gap-6">
              <div>
                <div className="flex items-center gap-1 text-primary-500">
                  <SparklesIcon className="w-4 h-4" />
                  <span className="font-bold">500+</span>
                </div>
                <span className="text-xs text-text-tertiary">Prestataires</span>
              </div>
              <div>
                <div className="flex items-center gap-1 text-primary-500">
                  <HeartIcon className="w-4 h-4" />
                  <span className="font-bold">10k+</span>
                </div>
                <span className="text-xs text-text-tertiary">Événements</span>
              </div>
              <div>
                <div className="flex items-center gap-1 text-primary-500">
                  <ShieldCheckIcon className="w-4 h-4" />
                  <span className="font-bold">4.9</span>
                </div>
                <span className="text-xs text-text-tertiary">Note</span>
              </div>
            </div>
          </div>

          {/* Links */}
          <div>
            <h3 className="font-semibold text-text-primary mb-4">Plateforme</h3>
            <ul className="space-y-3">
              {footerLinks.plateforme.map((link) => (
                <li key={link.name}>
                  <Link 
                    to={link.href} 
                    className="text-text-secondary hover:text-primary-500 transition-colors text-sm"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="font-semibold text-text-primary mb-4">Entreprise</h3>
            <ul className="space-y-3">
              {footerLinks.entreprise.map((link) => (
                <li key={link.name}>
                  <Link 
                    to={link.href} 
                    className="text-text-secondary hover:text-primary-500 transition-colors text-sm"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="font-semibold text-text-primary mb-4">Légal</h3>
            <ul className="space-y-3">
              {footerLinks.legal.map((link) => (
                <li key={link.name}>
                  <Link 
                    to={link.href} 
                    className="text-text-secondary hover:text-primary-500 transition-colors text-sm"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="pt-8 border-t border-border flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="text-sm text-text-tertiary">
            © 2024 Cérémonies. Tous droits réservés.
          </div>

          {/* Social links */}
          <div className="flex items-center gap-4">
            {socialLinks.map((social) => (
              <a
                key={social.name}
                href={social.href}
                className="w-10 h-10 bg-surface-alt rounded-full flex items-center justify-center hover:bg-primary-100 transition-colors group"
                aria-label={social.name}
              >
                <span className="text-lg group-hover:scale-110 transition-transform">
                  {social.icon}
                </span>
              </a>
            ))}
          </div>

          {/* Payment methods (pour plus tard) */}
          <div className="flex items-center gap-2">
            <span className="text-xs text-text-tertiary">Paiement sécurisé</span>
            <div className="flex gap-1">
              <span className="w-8 h-5 bg-surface-alt rounded text-[10px] flex items-center justify-center text-text-secondary">Visa</span>
              <span className="w-8 h-5 bg-surface-alt rounded text-[10px] flex items-center justify-center text-text-secondary">MC</span>
              <span className="w-8 h-5 bg-surface-alt rounded text-[10px] flex items-center justify-center text-text-secondary">CB</span>
            </div>
          </div>
        </div>
      </Container>
    </footer>
  );
}
