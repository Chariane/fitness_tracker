import { apiClient } from './client';

export interface Conversation {
  id: number;
  client_id: number;
  prestataire_id: number;
  ceremony_id: number | null;
  created_at: string;
  updated_at: string;
}

export interface Message {
  id: number;
  sender_id: number;
  receiver_id: number;
  conversation_id: number;
  content: string;
  created_at: string;
}

export const messagesApi = {
  getConversations: () => apiClient.get<Conversation[]>('/chat/conversations'),
  getMessages: (conversationId: number) => apiClient.get<Message[]>(`/chat/conversations/${conversationId}/messages`),
  sendMessage: (data: { receiver_id: number; content: string; conversation_id?: number }) =>
    apiClient.post('/chat/messages', data),
};