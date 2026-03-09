import { NavLink } from 'react-router-dom';
import {
  HomeIcon,
  UserGroupIcon,
  DocumentCheckIcon,
  TagIcon,
  ChatBubbleLeftRightIcon,
  Cog6ToothIcon,
} from '@heroicons/react/24/outline';

const navigation = [
  { name: 'Dashboard', href: '/admin', icon: HomeIcon },
  { name: 'Vérifications', href: '/admin/verification', icon: DocumentCheckIcon },
  { name: 'Types d\'événements', href: '/admin/ceremony-types', icon: TagIcon },
  { name: 'Catégories de services', href: '/admin/service-categories', icon: TagIcon },
  { name: 'Utilisateurs', href: '/admin/users', icon: UserGroupIcon },
  { name: 'Messages', href: '/admin/messages', icon: ChatBubbleLeftRightIcon },
  { name: 'Paramètres', href: '/admin/settings', icon: Cog6ToothIcon },
];

export function AdminSidebar() {
  return (
    <aside className="w-64 bg-white border-r border-border h-screen fixed left-0 top-0 pt-20">
      <nav className="p-4 space-y-1">
        {navigation.map((item) => (
          <NavLink
            key={item.name}
            to={item.href}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-xl transition-colors ${
                isActive
                  ? 'bg-primary-50 text-primary-600'
                  : 'text-text-secondary hover:bg-surface-alt'
              }`
            }
          >
            <item.icon className="w-5 h-5" />
            <span className="text-sm font-medium">{item.name}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}