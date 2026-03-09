// On reprend la structure de l'API et on ajoute les champs supplémentaires
export interface Conversation {
  id: number;
  client_id: number;
  prestataire_id: number;
  ceremony_id: number | null;  // aligné avec l'API
  created_at: string;
  updated_at: string;
  // Champs enrichis (optionnels, ajoutés côté frontend)
  last_message?: Message;
  unread_count?: number;
  participant_name?: string;
  participant_avatar?: string;
  event_name?: string;
}

export interface Message {
  id: number;
  sender_id: number;
  receiver_id: number;
  conversation_id: number;
  content: string;
  created_at: string;
  read?: boolean; // optionnel, peut être ajouté côté frontend
}