import React from 'react';
import Typography from '@material-ui/core/Typography';
import { Box } from '@material-ui/core';
import Parser from 'react-html-parser';

interface HighlightTextCardProps {
  text?: string;
}

const HighlightText = ({ text }: HighlightTextCardProps) => {
  return (
    <Box p={2}>
      <Box mt={2} mb={1}>
        {text ? (
          <Typography>{Parser(text)}</Typography>
        ) : (
          <Typography color='textSecondary'>Detection</Typography>
        )}
      </Box>
    </Box>
  );
};

export default HighlightText;
