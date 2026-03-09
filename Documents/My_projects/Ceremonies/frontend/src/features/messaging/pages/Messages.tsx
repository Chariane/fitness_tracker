import { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Container } from '../../../shared/components/ui/Container';
import { ConversationList } from '../components/ConversationList';
import { ChatWindow } from '../components/ChatWindow';
import { useMessages } from '../hooks/useMessages';
import { useAuth } from '../../../features/auth/hooks/useAuth';

export default function MessagesPage() {
  const { id } = useParams<{ id?: string }>();
  const { user } = useAuth();
  const currentUserId = user?.id || 0;
  const {
    conversations,
    selectedConversation,
    selectConversation,
    messages,
    sendMessage,
    loading,
  } = useMessages(currentUserId);

  // Sélectionner la conversation depuis l'URL
  useEffect(() => {
    if (id && conversations.length > 0) {
      const conv = conversations.find(c => c.id === parseInt(id));
      if (conv) selectConversation(conv);
    }
  }, [id, conversations, selectConversation]);

  if (loading) {
    return (
      <div className="min-h-screen bg-background pt-24 flex items-center justify-center">
        <div className="w-12 h-12 border-4 border-primary-200 border-t-primary-500 rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background pt-24 pb-16">
      <Container>
        <h1 className="text-3xl font-bold text-text-primary mb-8">Messages</h1>
        <div className="grid grid-cols-12 gap-6">
          <div className="col-span-4">
            <ConversationList
              conversations={conversations}
              selectedId={selectedConversation?.id}
              onSelect={selectConversation}
              currentUserId={currentUserId}
            />
          </div>
          <div className="col-span-8">
            {selectedConversation ? (
              <ChatWindow
                conversation={selectedConversation}
                currentUserId={currentUserId}
                messages={messages}
                onSendMessage={sendMessage}
              />
            ) : (
              <div className="bg-white rounded-2xl border border-border h-[600px] flex items-center justify-center">
                <p className="text-text-secondary">Sélectionnez une conversation</p>
              </div>
            )}
          </div>
        </div>
      </Container>
    </div>
  );
}