import React, { useEffect } from 'react';
import { styled } from '@mui/system';
import SendIcon from '@material-ui/icons/Send';
import { InputAdornment } from '@material-ui/core';
import { TextField } from '@mui/material';
import { commandNeedsPermission } from '../util/commands_util';
import './ChatWindow.css';

const ActionsContainer = styled('div')(({ theme }) => ({
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  flexDirection: 'row',
  width: '100%',
  backgroundColor: theme.palette.background.paper,
}));
const TextAreaContainer = styled('div')(({ theme }) => ({
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  flexDirection: 'row',
  backgroundColor: theme.palette.background.paper,
  width: '100%',
}));

const TextArea = styled(TextField)(({ theme }) => ({
  width: '100%',
  padding: theme.spacing(2),
  backgroundColor: theme.palette.background.default,
  borderRadius: theme.shape.borderRadius,
  resize: 'none',
  '&:focus': {
    outline: 'none',
    borderColor: theme.palette.primary.main,
  },
  '& input': {
    color: theme.palette.customColors.brightGreen2,
  },
}));


const Actions: React.FC<any> = ({ onSendMessage, selectedAgentId, command, onAgentAct }) => {

  const [message, setMessage] = React.useState<string>('');


  useEffect(() => {
    setMessage('');
  }, [selectedAgentId]);


  const handleActionClick = async () => {
    setMessage('');

    let result = null;

    if (command && commandNeedsPermission(command?.['name'])) {
      result = await onAgentAct(message);
    } else {
      result = await onSendMessage(message);
    }

    console.debug({ result });
  };

  const handleKeyPress = (event: any) => {
    if (event.key === 'Enter') {
      handleActionClick();
    }
  };


  if (!selectedAgentId) {
    return null;
  }

  return (
    <ActionsContainer>
      <TextAreaContainer>
        <TextArea
          InputProps={{
            endAdornment: (
              <InputAdornment
                style={{ cursor: 'pointer' }}
                onClick={() => handleActionClick()}
                position='end'
              >
                <SendIcon
                  className={'icon-rotator'}
                  style={{ transform: 'rotate(-45deg)' }} />
              </InputAdornment>
            ),
          }}
          placeholder={command ? 'Type your feedback...' : 'Type your message...'}
          value={message}
          onChange={(event) => setMessage(event.target.value)}
          onKeyPress={handleKeyPress}
        />
      </TextAreaContainer>
    </ActionsContainer>
  );
};

export default Actions;
