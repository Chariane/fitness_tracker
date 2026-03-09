import { motion } from 'framer-motion';
import { formatDistanceToNow } from 'date-fns';
import { fr } from 'date-fns/locale';
import { Avatar } from '../../../shared/components/ui/Avatar';
import { cn } from '../../../lib/utils';
import type { Conversation } from '../types';

interface ConversationListProps {
  conversations: Conversation[];
  selectedId?: number;
  onSelect: (conversation: Conversation) => void; // maintenant on passe la conversation
  currentUserId: number;
}

export function ConversationList({ conversations, selectedId, onSelect, currentUserId }: ConversationListProps) {
  return (
    <div className="bg-white rounded-2xl border border-border overflow-hidden">
      <div className="p-4 border-b border-border">
        <h3 className="font-semibold text-text-primary">Messages</h3>
      </div>
      <div className="divide-y divide-border">
        {conversations.map((conv) => {
          const otherId = currentUserId === conv.client_id ? conv.prestataire_id : conv.client_id;
          const otherName = conv.participant_name || `Utilisateur ${otherId}`;
          const lastMsg = conv.last_message;

          return (
            <motion.div
              key={conv.id}
              whileHover={{ backgroundColor: 'rgba(0,0,0,0.02)' }}
              onClick={() => onSelect(conv)} // on passe la conversation entière
              className={cn(
                'p-4 cursor-pointer transition-colors',
                selectedId === conv.id ? 'bg-primary-50' : ''
              )}
            >
              <div className="flex gap-3">
                <Avatar initials={otherName.charAt(0)} size="md" />
                <div className="flex-1 min-w-0">
                  <div className="flex justify-between items-start">
                    <h4 className="font-medium text-text-primary truncate">{otherName}</h4>
                    {lastMsg && (
                      <span className="text-xs text-text-tertiary">
                        {formatDistanceToNow(new Date(lastMsg.created_at), { addSuffix: true, locale: fr })}
                      </span>
                    )}
                  </div>
                  {conv.event_name && (
                    <p className="text-xs text-primary-500 mb-1">{conv.event_name}</p>
                  )}
                  {lastMsg && (
                    <p className={cn(
                      'text-sm truncate',
                      conv.unread_count ? 'font-semibold text-text-primary' : 'text-text-secondary'
                    )}>
                      {lastMsg.sender_id === currentUserId ? 'Vous : ' : ''}{lastMsg.content}
                    </p>
                  )}
                </div>
                {conv.unread_count ? (
                  <div className="w-5 h-5 rounded-full bg-primary-500 text-white text-xs flex items-center justify-center">
                    {conv.unread_count}
                  </div>
                ) : null}
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}