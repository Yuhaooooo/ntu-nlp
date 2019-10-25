import React, { useEffect } from 'react';
// @ts-ignore
import SwaggerUi, { presets } from 'swagger-ui';
import 'swagger-ui/dist/swagger-ui.css';
import HeaderPlaceHolder from '../../common/HeaderPlaceHolader';
import { setTitleEffectFactory } from '../../utils/utils';
import { api_host as apiHost, api_port as apiPort } from '../../config';

const Swagger = () => {
  useEffect(() => {
    SwaggerUi({
      dom_id: '#swagger-container',
      url: `${apiHost}:${apiPort}/openapi.json`,
      presets: [presets.apis],
    });
  });

  useEffect(setTitleEffectFactory('API Test'), []);

  return (
    <>
      <HeaderPlaceHolder />
      <div id='swagger-container' />
    </>
  );
};

export default Swagger;
