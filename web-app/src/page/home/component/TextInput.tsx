import React, { useCallback, useState } from 'react';
import { Box, Button, IconButton, TextField, Theme } from '@material-ui/core';
import CloseIcon from '@material-ui/icons/CloseRounded';
import { makeStyles } from '@material-ui/styles';
import { MicroserviceTNERReqType } from '../../../store/text/type';

const useStyles = makeStyles((theme: Theme) => ({
  textField: {
    width: `calc(100% - ${theme.spacing(6)}px)`,
  },
  textFieldInput: {
    lineHeight: 2.5,
  },
  iconContainer: {
    display: 'inline-block',
    position: 'absolute',
    top: 0,
    right: 0,
    width: 48,
    height: 48,
  },
  icon: {
    display: 'block',
    width: '100%',
    height: '100%',
  },
}));

interface TextInputProps {
  analyze: (props: MicroserviceTNERReqType) => any;
}

const sample =
  'In an announcement yesterday, Synagie said that its wholly owned ' +
  'subsidiary, BTFL, has signed a memorandum of understanding (MOU) with ' +
  "Lazada to provide services to manage and operate the e-commerce company's " +
  'brand stores on its online marketplaces in Southeast Asia.';

const TextInput = ({ analyze }: TextInputProps) => {
  const classes = useStyles();
  const [value, setValue] = useState('');

  const handleOnChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => setValue(e.target.value),
    [],
  );

  const handleClear = useCallback(() => setValue(''), []);

  const handleLoadSample = useCallback(() => setValue(sample), []);

  return (
    <Box p={2} position='relative'>
      <TextField
        className={classes.textField}
        label=''
        multiline
        value={value}
        onChange={handleOnChange}
        margin='normal'
        placeholder='Key in sentences to detect'
        inputProps={{ className: classes.textFieldInput }}
      />
      <Box display='flex' justifyContent='space-between'>
        <Button onClick={handleLoadSample}>Get a sample</Button>
        <Button color='primary' onClick={() => analyze({ text: value })}>
          Analyze
        </Button>
      </Box>
      {value ? (
        <IconButton className={classes.iconContainer} onClick={handleClear}>
          <CloseIcon className={classes.icon} />
        </IconButton>
      ) : null}
    </Box>
  );
};

export default TextInput;
