// ChatWindow.tsx
import React, { useEffect, useRef, useState } from 'react';
import { styled } from '@mui/system';
import { Divider, List, ListItem, ListItemAvatar, ListItemIcon, ListSubheader, Stack } from '@mui/material';
import { Avatar, ListItemText } from '@material-ui/core';
import './ChatWindow.css';
// @ts-ignore
import ReactTypingEffect from 'react-typing-effect';
import { AGENT_ROLE, SYSTEM_ROLE, USER_ROLE } from '../config/Constants';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faBan,
  faBrain,
  faCalendarAlt,
  faCog,
  faLightbulb,
  faMicrophone,
  faUserTie,
} from '@fortawesome/free-solid-svg-icons';

interface Props {
  agentState: any;
  sendMessage: any;
  chatHistory: any;
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

const ListHeaderText = styled('div')(({ theme }) => ({
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
  textAlign: 'center',
  color: theme.palette.customColors.brightPink,
}));

const ChatWindow: React.FC<Props> = ({ agentState, sendMessage, chatHistory }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const [messages, setMessages] = useState<string[]>([]);

  const [showHal, setShowHal] = useState<boolean>(false);

  const [typingSpeed, setTypingSpeed] = useState<number>(10);


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


  function planComponent(plan: any) {
    if (!plan) {
      return null;
    }

    const plans = (plan || '').split('\n');

    const plansComponents = plans.map((p: string, index: number) => (
      <ListItem key={index} disablePadding>
        <ListItemText>
          <PlanText>{index + 1}. {p}</PlanText>
        </ListItemText>
      </ListItem>
    ));
    return (<Stack>
      <ListItem>
        <ListItemIcon>
          <FontAwesomeIcon icon={faCalendarAlt} />
        </ListItemIcon>
        <List>
          {plansComponents}
        </List>
      </ListItem>
    </Stack>);
  }

  function contentEntryComponent(textComponent?: any, icon?: any) {
    return (
      <ListItem>
        <ListItemIcon>
          <FontAwesomeIcon icon={icon} />
        </ListItemIcon>
        <ListItemText>
          {textComponent}
        </ListItemText>
      </ListItem>
    );
  }


  function systemMessageComponent(content: any) {
    return (<ListItem>
      <ListItemAvatar>
        <FontAwesomeIcon icon={faCog} />
      </ListItemAvatar>

      <ListItemText>
        {content}
      </ListItemText>
    </ListItem>);
  }

  function agentMessageComponent(content: any) {
    const thoughts = content['thoughts'];

    if (!thoughts) {
      return null;
    }
    return (
      <ListItem>
        <ListItemAvatar>
          <Avatar src={process.env.PUBLIC_URL + '/agent_avatar.png'} />
        </ListItemAvatar>

        <List>
          {thoughts['text'] && contentEntryComponent((<ThoughtText>
            {thoughts['text']}
          </ThoughtText>), faLightbulb)}
          {thoughts['criticism'] && contentEntryComponent((<CriticismText>
            {thoughts['criticism']}
          </CriticismText>), faBan)}
          {thoughts['reasoning'] && contentEntryComponent((<ReasoningText>
            {thoughts['reasoning']}
          </ReasoningText>), faBrain)}
          {planComponent(thoughts['speak'])}
          {thoughts['speak'] && contentEntryComponent((<ReasoningText>
            {thoughts['speak']}
          </ReasoningText>), faMicrophone)}
        </List>
      </ListItem>
    );

  }

  function userMessageComponent(content: any) {
    return (<ListItem>
      <ListItemAvatar>
        <FontAwesomeIcon icon={faUserTie} />
      </ListItemAvatar>

      <ListItemText>
        {(content || '').replace('Human feedback:','')}
      </ListItemText>
    </ListItem>);
  }

  function messageComponent(message: any) {
    if (!message) {
      return null;
    }

    const role = message.role;
    const content = message.content;

    switch (role) {
      case USER_ROLE:
        return userMessageComponent(content);

      case AGENT_ROLE:
        return agentMessageComponent(content);

      case SYSTEM_ROLE:
        return systemMessageComponent(content);
      default:
        return 'This message has no role, this is a bug !!!';
    }
  }

  function body() {
    console.debug({ chatHistory });
    const content = (<>
      {(chatHistory || []).map((message: any, index: number) => (
        <>
          {messageComponent(message)}
          <Divider />
        </>
      ))}
      <div ref={messagesEndRef} />
    </>);


    return <ChatWindowContainer className={showHal ? 'hal_9000' : ''}>
      <List>
        <ListSubheader>
          <HeaderText>Chat</HeaderText>
        </ListSubheader>
        {content}
      </List>
    </ChatWindowContainer>;

  }

  return (
    <>
      {body()}
    </>
  );
};

export default ChatWindow;
