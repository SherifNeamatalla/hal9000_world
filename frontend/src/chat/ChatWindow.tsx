// ChatWindow.tsx
import React, { useEffect, useRef, useState } from 'react';
import { styled } from '@mui/system';

interface Props {
  agentState: any;
  sendMessage: any;
}

const ChatWindowContainer = styled('div')(({ theme }) => ({
  backgroundColor: theme.palette.matrix.main,
  height: '100%',
  overflowY: 'auto',
  padding: theme.spacing(2),
  display: 'flex',
  flexDirection: 'column',
  borderRadius: '10px',
}));

const MatrixText = styled('div')(({ theme }) => ({
  color: theme.palette.customColors.brightGreen,
  fontFamily: 'Roboto Mono',
  whiteSpace: 'pre-wrap',
  fontSize: '14px',
  lineHeight: '20px',
}));

const ChatWindow: React.FC<Props> = ({ agentState, sendMessage }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const [messages, setMessages] = useState<string[]>([]);

  useEffect(() => {
    if (agentState.response) {
      setMessages((prevMessages) => [
        ...prevMessages,
        `> ${agentState.response}`,
      ]);
    }
  }, [agentState]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages]);

  return (
    <ChatWindowContainer>
      {messages.map((message, index) => (
        <MatrixText key={index}>
          {message}
        </MatrixText>
      ))}
      <MatrixText>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed
      </MatrixText>
      <div ref={messagesEndRef} />
    </ChatWindowContainer>
  );
};

export default ChatWindow;
