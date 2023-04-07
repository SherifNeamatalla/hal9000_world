// ChatWindow.tsx
import React, { useEffect, useRef, useState } from 'react';
import { styled } from '@mui/system';
import { List, ListItem, ListSubheader, Stack } from '@mui/material';
import { ListItemText } from '@material-ui/core';
import './ChatWindow.css';

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
  position: 'relative',
}));


const MatrixText = styled('div')(({ theme }) => ({
  color: theme.palette.customColors.brightGreen,
  fontFamily: 'Roboto Mono',
  whiteSpace: 'pre-wrap',
  fontSize: '14px',
  lineHeight: '20px',
}));

const ThoughtText = styled('div')(({ theme }) => ({
  color: theme.palette.customColors.darkViolet,
  fontFamily: 'Roboto Mono',
  whiteSpace: 'pre-wrap',
  fontSize: '14px',
  lineHeight: '20px',
}));

const CriticismText = styled('div')(({ theme }) => ({
  color: theme.palette.customColors.brightOrange2,
  fontFamily: 'Roboto Mono',
  whiteSpace: 'pre-wrap',
  fontSize: '14px',
  lineHeight: '20px',
}));

const ReasoningText = styled('div')(({ theme }) => ({
  color: theme.palette.customColors.brightOrange,
  fontFamily: 'Roboto Mono',
  whiteSpace: 'pre-wrap',
  fontSize: '14px',
  lineHeight: '20px',
}));

const PlanText = styled('div')(({ theme }) => ({
  color: theme.palette.customColors.brightBlueGreen,
  fontFamily: 'Roboto Mono',
  whiteSpace: 'pre-wrap',
  fontSize: '14px',
  lineHeight: '20px',
}));

const HeaderText = styled('div')(({ theme }) => ({
  fontFamily: 'Roboto Mono',
  whiteSpace: 'pre-wrap',
  fontSize: '14px',
  lineHeight: '20px',
}));

const ChatWindow: React.FC<Props> = ({ agentState, sendMessage }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const [messages, setMessages] = useState<string[]>([]);

  const [thought, setThought] = useState<string>('');
  const [criticism, setCriticism] = useState<string>('');
  const [speak, setSpeak] = useState<string>('');
  const [reasoning, setReasoning] = useState<string>('');
  const [plan, setPlan] = useState<string>('');

  const [showHal, setShowHal] = useState<boolean>(false);
  useEffect(() => {
    if (agentState.response) {
      setMessages((prevMessages) => [
        ...prevMessages,
        `> ${agentState.response}`,
      ]);
    }

    setThought('This is a thought');
    setCriticism('This is a criticism');
    setSpeak('This is a text user should see/hear');
    setReasoning('This is a reasoning');
    setPlan('Plan1\nPlan2\nPlan3\nPlan4');
  }, [agentState]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages]);


  function plansComponent() {
    if (!plan) {
      return null;
    }

    const plans = (plan || '').split('\n');

    const plansComponents = plans.map((plan, index) => (
      <ListItem key={index} disablePadding>
        <ListItemText>
          <PlanText>{index + 1}. plan</PlanText>
        </ListItemText>
      </ListItem>
    ));
    return (<Stack>
      <List>
        <ListSubheader>
          <HeaderText>My plans</HeaderText>
        </ListSubheader>
        {plansComponents}
      </List>
    </Stack>);
  }

  function thoughtsComponent() {
    if (!thought) {
      return null;
    }


    return (<Stack>
      <List>
        <ListSubheader>
          <HeaderText>My thoughts</HeaderText>
        </ListSubheader>
        <ThoughtText>{thought}</ThoughtText>
      </List>
    </Stack>);
  }

  function criticismComponent() {
    if (!criticism) {
      return null;
    }

    return (<Stack>
      <List>
        <ListSubheader>
          <HeaderText>My criticism</HeaderText>
        </ListSubheader>
        <CriticismText>{criticism}</CriticismText>
      </List>
    </Stack>);
  }

  function reasoningComponent() {
    if (!reasoning) {
      return null;
    }

    return (<Stack>
      <List>
        <ListSubheader>
          <HeaderText>My reasoning</HeaderText>
        </ListSubheader>
        <ReasoningText>{reasoning}</ReasoningText>
      </List>
    </Stack>);
  }


  function speakComponent() {
    if (!speak) {
      return null;
    }

    return (<Stack>
      <List>
        <ListSubheader>
          <HeaderText>My reasoning</HeaderText>
        </ListSubheader>
        <MatrixText>{speak}</MatrixText>
      </List>
    </Stack>);
  }


  function body() {
    const content = (<>
      {messages.map((message, index) => (
        <MatrixText key={index}>
          {message}
        </MatrixText>
      ))}
      {thoughtsComponent()}
      {criticismComponent()}
      {reasoningComponent()}
      {plansComponent()}
      {speakComponent()}
      <div ref={messagesEndRef} />
    </>);


    return <ChatWindowContainer className={showHal ? 'hal_9000' : ''}>{content}</ChatWindowContainer>;

  }

  return (
    <>
      {body()}
    </>
  );
};

export default ChatWindow;
