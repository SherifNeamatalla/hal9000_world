// ChatWindow.tsx
import React, { useEffect, useRef, useState } from 'react';
import { styled } from '@mui/system';
import {
  Divider,
  IconButton,
  List,
  ListItem,
  ListItemAvatar,
  ListItemIcon,
  ListItemSecondaryAction,
  Stack,
  Tooltip,
  useTheme,
} from '@mui/material';
import { Avatar, ListItemText } from '@material-ui/core';
import './ChatWindow.css';
// @ts-ignore
import ReactTypingEffect from 'react-typing-effect';
import { AGENT_ROLE, PERMISSION_DENIED, PERMISSION_GRANTED, SYSTEM_ROLE, USER_ROLE } from '../config/Constants';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faBan,
  faBrain,
  faCalendarAlt,
  faCheckCircle,
  faCircleXmark,
  faCog,
  faExclamationTriangle,
  faLightbulb,
  faMicrophone,
  faSpinner,
  faUserTie,
} from '@fortawesome/free-solid-svg-icons';
import { commandNeedsPermission } from '../util/commands_util';
import AudioPlayer from '../components/AudioPlayer';

interface Props {
  agentState: any;
  sendMessage: any;
  chatHistory: any;
  onResendMessage: any;
  onAgentAct: any;
  command: any;
  showHal: boolean;
  audioUrl?: string;
}

const ChatWindowContainer = styled('div')(({ theme }) => ({
  backgroundColor: theme.palette.matrix.main,
  height: '100%',
  overflowY: 'auto',
  padding: theme.spacing(2),
  display: 'flex',
  flexDirection: 'column',
  borderRadius: '10px',
  position: 'unset',
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

const Hal = styled('div')(({ theme }) => ({
  position: 'absolute',
  top: '50%',
  right: '50%',
  left: '50%',
  bottom: '50%',
  width: '100px',
  height: '100px',
  backgroundColor: 'red',
  borderRadius: '50%',
  transform: 'translate(-50%, -50%)',
  opacity: 0,
  animation: 'pulse 5s infinite',


}));
const ChatWindow: React.FC<Props> = ({
                                       audioUrl,
                                       agentState,
                                       command,
                                       chatHistory,
                                       onResendMessage,
                                       onAgentAct,
                                       showHal,
                                     }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const theme = useTheme();
  const [messages, setMessages] = useState<string[]>([]);
  const containerRef = useRef<HTMLDivElement | null>(null);
  const [typingSpeed, setTypingSpeed] = useState<number>(10);


  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [chatHistory]);
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


  function systemMessageComponent(content: any, index: number) {
    return (<ListItem key={index}>
      <ListItemAvatar>
        <FontAwesomeIcon icon={faCog} />
      </ListItemAvatar>

      <ListItemText>
        {content}
      </ListItemText>
    </ListItem>);
  }

  function speakComponent(thoughts: any, index: number) {
    if (!thoughts?.['speak']) {
      return null;
    }
    if (index === chatHistory.length - 1) {
      return (contentEntryComponent((<MatrixText>
        <ReactTypingEffect text={thoughts['speak']} eraseDelay={9999999} speed={typingSpeed}/>
      </MatrixText>), faMicrophone));
    }
    return (contentEntryComponent((<MatrixText>
      {thoughts['speak']}
    </MatrixText>), faMicrophone));
  }

  function agentMessageComponent(content: any, index: number) {
    const thoughts = content['thoughts'];

    if (!thoughts) {
      return null;
    }
    return (
      <ListItem key={index}>
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
          {planComponent(thoughts['plan'])}
          {speakComponent(thoughts, index)}
        </List>
      </ListItem>
    );

  }


  const renderIcon = (confirmedStatus: any) => {
    if (confirmedStatus === 'error') {
      return (<Tooltip title='Woops! Message did not go through!'>
        <FontAwesomeIcon
          icon={faExclamationTriangle}
          onClick={() => onResendMessage()}
          style={{ cursor: 'pointer' }}
        />
      </Tooltip>);
    } else if (confirmedStatus === 'pending') {
      return <FontAwesomeIcon icon={faSpinner} spin />;
    }
    return null;
  };

  function userMessageComponent(content: any, confirmedStatus: any, index: number) {

    return (<ListItem key={index}>
      <ListItemAvatar>
        <FontAwesomeIcon icon={faUserTie} />
      </ListItemAvatar>

      <ListItemText>
        {(content || '').replace('Human feedback:', '')}
      </ListItemText>

      {renderIcon(confirmedStatus) && (
        <ListItemSecondaryAction>
          {renderIcon(confirmedStatus)}
        </ListItemSecondaryAction>
      )}
    </ListItem>);
  }

  function messageComponent(message: any, index: number) {
    if (!message) {
      return null;
    }

    const role = message.role;
    const content = message.content;
    const confirmedStatus = message.confirmed || null;


    switch (role) {
      case USER_ROLE:
        return userMessageComponent(content, confirmedStatus, index);

      case AGENT_ROLE:
        return agentMessageComponent(content, index);

      case SYSTEM_ROLE:
        return systemMessageComponent(content, index);
      default:
        return 'This message has no role, this is a bug !!!';
    }
  }

  function commandMessageComponent() {
    if (!command || !commandNeedsPermission(command?.['name']) || showHal) {
      return null;
    }


    return (<ListItem>
      <ListItemAvatar>
        <Tooltip title={'Waiting for user permission!'}>
          <FontAwesomeIcon icon={faExclamationTriangle} />
        </Tooltip>
      </ListItemAvatar>

      <ListItemText>
        Your response to the command (Send a message instead to provide feedback)
      </ListItemText>

      <ListItemSecondaryAction>
        <IconButton>
          <FontAwesomeIcon icon={faCheckCircle}
                           style={{ color: (theme.palette as any).matrix.contrastText }}
                           onClick={() => {
                             onAgentAct(PERMISSION_GRANTED);
                           }}
          />
        </IconButton>

        <IconButton>
          <FontAwesomeIcon icon={faCircleXmark}
                           onClick={() => {
                             onAgentAct(PERMISSION_DENIED);
                           }}
                           style={{ color: (theme.palette as any).customColors.brightOrange2 }}
          />
        </IconButton>
      </ListItemSecondaryAction>
    </ListItem>);
  }

  function body() {
    const content = (<>
      {(chatHistory || []).map((message: any, index: number) => (
        <>
          {messageComponent(message, index)}
          <Divider />
        </>
      ))}
      <div ref={messagesEndRef} />
    </>);


    return <ChatWindowContainer className={'scrollable-container'} ref={containerRef}>
      <List className={'scrollable-content'}>
        {content}
        {commandMessageComponent()}
      </List>
      {showHal && <Hal />}
      {audioUrl && (
        <AudioPlayer audioStreamUrl={audioUrl} />
      )}
    </ChatWindowContainer>;

  }

  return (
    <>
      {body()}
    </>
  );
};

export default ChatWindow;
