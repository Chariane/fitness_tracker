import { useState, useEffect, useCallback } from 'react';
import { messagesApi } from '../../../shared/api/messages';
import { usersApi } from '../../../shared/api/users';
import { useWebSocket } from '../../../shared/hooks/useWebSocket';
import type { Conversation as ApiConversation } from '../../../shared/api/messages';
import type { Conversation, Message } from '../types';

async function enrichConversation(conv: ApiConversation, currentUserId: number): Promise<Conversation> {
  const otherId = currentUserId === conv.client_id ? conv.prestataire_id : conv.client_id;
  try {
    const userRes = await usersApi.getUserById(otherId);
    return {
      ...conv,
      participant_name: userRes.data.full_name || 'Utilisateur',
      participant_avatar: userRes.data.avatar_url ?? undefined,
    };
  } catch {
    return {
      ...conv,
      participant_name: 'Utilisateur',
    };
  }
}

export function useMessages(currentUserId: number) {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [selectedConversation, setSelectedConversation] = useState<Conversation | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(true);
  const { sendMessage: sendWsMessage, onMessage } = useWebSocket();

  // Charger les conversations
  useEffect(() => {
    const fetchConversations = async () => {
      try {
        const res = await messagesApi.getConversations();
        const apiConvs = res.data;
        const enriched = await Promise.all(
          apiConvs.map(conv => enrichConversation(conv, currentUserId))
        );
        setConversations(enriched);
      } catch (error) {
        console.error('Erreur chargement conversations', error);
      } finally {
        setLoading(false);
      }
    };
    fetchConversations();
  }, [currentUserId]);

  // Charger les messages d'une conversation sélectionnée
  useEffect(() => {
    if (selectedConversation) {
      const fetchMessages = async () => {
        try {
          const res = await messagesApi.getMessages(selectedConversation.id);
          setMessages(res.data);
        } catch (error) {
          console.error('Erreur chargement messages', error);
        }
      };
      fetchMessages();
    }
  }, [selectedConversation]);

  // Écouter les nouveaux messages via WebSocket
  useEffect(() => {
    const handleNewMessage = (data: any) => {
      const msg = data as Message;
      // Mise à jour des messages de la conversation courante
      if (msg.conversation_id === selectedConversation?.id) {
        setMessages(prev => {
          // Éviter les doublons (si on a déjà reçu ce message)
          const exists = prev.some(m => m.id === msg.id);
          if (exists) return prev;
          return [...prev, msg];
        });
      }
      // Mettre à jour la dernière conversation dans la liste
      setConversations(prev => prev.map(conv =>
        conv.id === msg.conversation_id
          ? { ...conv, last_message: msg, unread_count: (conv.unread_count || 0) + 1 }
          : conv
      ));
    };
    onMessage(handleNewMessage);
  }, [selectedConversation, onMessage]);

  const sendMessage = useCallback((content: string) => {
    if (!selectedConversation) return;
    const receiverId = currentUserId === selectedConversation.client_id
      ? selectedConversation.prestataire_id
      : selectedConversation.client_id;
    // Envoi via WebSocket (pas d'optimistic update)
    sendWsMessage(receiverId, content, selectedConversation.id);
  }, [selectedConversation, currentUserId, sendWsMessage]);

  const selectConversation = useCallback((conversation: Conversation) => {
    setSelectedConversation(conversation);
    // Optionnel : marquer comme lu
  }, []);

  return {
    conversations,
    selectedConversation,
    selectConversation,
    messages,
    sendMessage,
    loading,
  };
}