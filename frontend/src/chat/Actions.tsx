import React from 'react';
import { styled } from '@mui/system';
import SendIcon from '@material-ui/icons/Send';
import { InputAdornment } from '@material-ui/core';
import { TextField } from '@mui/material';

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

interface Props {
  onActionClick: (action: string) => void;
}

const Actions: React.FC<Props> = ({ onActionClick }) => {

  const handleActionClick = (action: string) => {
    onActionClick(action);
  };

  return (
    <ActionsContainer>
      <TextAreaContainer>
        <TextArea
          InputProps={{
            endAdornment: <InputAdornment
              style={{ cursor: 'pointer' }}
              onClick={() => handleActionClick('send')}
              position='end'><SendIcon
              style={{ transform: 'rotate(-45deg)' }}
            /></InputAdornment>,
          }}
          placeholder='Type your message...' />
      </TextAreaContainer>
    </ActionsContainer>
  );
};

export default Actions;
