import React, { useCallback } from 'react';
import Typography from '@material-ui/core/Typography';
import { Box } from '@material-ui/core';
import _ from 'lodash';
import Star from '@material-ui/icons/StarRounded';
import StarBorder from '@material-ui/icons/StarBorderRounded';
import StarHalf from '@material-ui/icons/StarHalfRounded';

interface HighlightTextCardProps {
  stars: number;
}

const StarResult = ({ stars }: HighlightTextCardProps) => {
  const toStar = useCallback((star: number) => {
    let starCap = 0;
    if (star >= 5) starCap = 5;
    else if (star > 0) starCap = star;

    const starNum = Math.round(starCap * 2) / 2;
    const half = !Number.isInteger(starNum);
    const whole = Math.floor(starNum);
    const starIcons = [
      ..._.fill(Array(whole), Star),
      ..._.fill(Array(5 - whole), StarBorder),
    ];
    if (half) starIcons[whole] = StarHalf;
    return starIcons;
  }, []);

  return (
    <Box px={2}>
      <Box mt={2} mb={1}>
        {stars !== -1 ? (
          <Typography>
            {toStar(stars).map((Compo, index) => (
              // eslint-disable-next-line react/no-array-index-key
              <Compo key={index} />
            ))}
          </Typography>
        ) : null}
      </Box>
    </Box>
  );
};

export default StarResult;
