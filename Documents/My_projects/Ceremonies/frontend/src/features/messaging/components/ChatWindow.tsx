import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { PaperAirplaneIcon, LockClosedIcon } from '@heroicons/react/24/outline';
import { Avatar } from '../../../shared/components/ui/Avatar';
import { Button } from '../../../shared/components/ui/Button';
import { Input } from '../../../shared/components/ui/Input';
import { cn } from '../../../lib/utils';
import type { Conversation, Message } from '../types';

interface ChatWindowProps {
  conversation: Conversation;
  currentUserId: number;
  messages: Message[];
  onSendMessage: (content: string) => void;
}

export function ChatWindow({ conversation, currentUserId, messages, onSendMessage }: ChatWindowProps) {
  const [newMessage, setNewMessage] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const otherParticipantId = currentUserId === conversation.client_id ? conversation.prestataire_id : conversation.client_id;
  const otherName = conversation.participant_name || 'Utilisateur';

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = () => {
    if (newMessage.trim()) {
      onSendMessage(newMessage);
      setNewMessage('');
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-border overflow-hidden flex flex-col h-[600px]">
      {/* Header */}
      <div className="p-4 border-b border-border flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Avatar initials={otherName.charAt(0)} />
          <div>
            <h3 className="font-semibold text-text-primary">{otherName}</h3>
            <p className="text-xs text-text-secondary">
              {currentUserId === conversation.client_id ? 'Prestataire' : 'Client'}
            </p>
          </div>
        </div>
        {conversation.ceremony_id && (
          <span className="text-xs text-primary-500">Événement associé</span>
        )}
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        <AnimatePresence>
          {messages.map((msg) => {
            const isOwn = msg.sender_id === currentUserId;
            return (
              <motion.div
                key={msg.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className={cn('flex', isOwn ? 'justify-end' : 'justify-start')}
              >
                <div className={cn(
                  'max-w-[70%] rounded-2xl px-4 py-2',
                  isOwn
                    ? 'bg-primary-500 text-white rounded-br-none'
                    : 'bg-surface border border-border rounded-bl-none'
                )}>
                  <p className="text-sm">{msg.content}</p>
                  <p className={cn(
                    'text-xs mt-1',
                    isOwn ? 'text-primary-100' : 'text-text-tertiary'
                  )}>
                    {new Date(msg.created_at).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}
                  </p>
                </div>
              </motion.div>
            );
          })}
        </AnimatePresence>
        <div ref={messagesEndRef} />
      </div>

      {/* Info confidentialité */}
      <div className="px-4 py-2 bg-surface/60 border-t border-border">
        <div className="flex items-center gap-2 text-xs text-text-secondary">
          <LockClosedIcon className="w-3 h-3" />
          <span>Les coordonnées seront dévoilées après confirmation de la réservation</span>
        </div>
      </div>

      {/* Input */}
      <div className="p-4 border-t border-border">
        <div className="flex gap-2">
          <Input
            placeholder="Écrivez votre message..."
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          />
          <Button onClick={handleSend} disabled={!newMessage.trim()}>
            <PaperAirplaneIcon className="w-5 h-5" />
          </Button>
        </div>
      </div>
    </div>
  );
}