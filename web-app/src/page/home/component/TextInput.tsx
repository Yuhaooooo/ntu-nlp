import React, { useCallback, useState } from 'react';
import { Box, Button, IconButton, TextField, Theme } from '@material-ui/core';
import CloseIcon from '@material-ui/icons/CloseRounded';
import { makeStyles } from '@material-ui/styles';
import { ReviewReqType } from '../../../store/text/type';

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
    top: 4,
    right: 4,
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
  analyze: (props: ReviewReqType) => any;
}

const sample =
  'Not sure what pool service should entail but I get inconsistent service.' +
  '  Sometimes they add chlorine tabs, sometimes not, sometimes they sweep,' +
  ' sometimes not.  This is a rental house where I hired a professional to' +
  ' maintain my equipment and relieve my tenants of the burden but there is a' +
  ' lack of communication somewhere.  Water level dropped to point that it' +
  ' burned up my motor and then they explained their policy about not filling' +
  ' the pool to run up my bill.  The expensive repair on that could have ' +
  'bought about 50,000 extra gallons:(';

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
        <Button color='primary' onClick={() => analyze({ sentence: value })}>
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
