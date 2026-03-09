import { useEffect, useRef } from 'react';
import { useAuth } from '../../features/auth/hooks/useAuth';

export function useWebSocket() {
  const { user } = useAuth();
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!user) return;

    const token = localStorage.getItem('token');
    const socket = new WebSocket(`ws://localhost:8000/ws/${user.id}?token=${token}`);
    ws.current = socket;

    socket.onopen = () => console.log('WebSocket connected');
    socket.onclose = () => console.log('WebSocket disconnected');
    socket.onerror = (error) => console.error('WebSocket error', error);

    return () => {
      socket.close();
    };
  }, [user]);

  const sendMessage = (receiverId: number, content: string, conversationId?: number) => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify({
        receiver_id: receiverId,
        content,
        conversation_id: conversationId,
      }));
    }
  };

  const onMessage = (callback: (data: any) => void) => {
    if (ws.current) {
      ws.current.onmessage = (event) => {
        const data = JSON.parse(event.data);
        callback(data);
      };
    }
  };

  return { isConnected: ws.current?.readyState === WebSocket.OPEN, sendMessage, onMessage };
}