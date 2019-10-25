import _ from 'lodash';
import { Action, Dispatch } from 'redux';
import { appendCredential, getCookie } from './utils';
import { HttpMethod, XMLParameter } from './type';

function get(
  dispatch: Dispatch,
  url: string,
  jsonDecoder = (json: Object) => json,
  request: (...args: any[]) => Action,
  receiveSuccess: Function,
  receiveFailure: Function,
  formData?: FormData,
  headers: { [propName: string]: string } = {},
) {
  const xhr = new XMLHttpRequest();

  function onStateChange() {
    if (xhr.readyState === 4) {
      if (xhr.status >= 200 && xhr.status <= 300) {
        try {
          const json = JSON.parse(xhr.responseText);
          const data = jsonDecoder(json.data);
          dispatch(receiveSuccess({ ...json, data }));
        } catch (e) {
          return dispatch(
            receiveFailure({ data: 'Error in mapping response json to list' }),
          );
        }
      }
    }
    return dispatch(receiveFailure({ data: `Other error: ${xhr.statusText}` }));
  }

  // GET start
  dispatch(request());

  xhr.open('GET', url, true);
  xhr.onreadystatechange = onStateChange;
  _.forOwn(headers, (value, key) => xhr.setRequestHeader(key, value));
  xhr.send(formData);

  return xhr;
}

function post(
  progressListener: Function | undefined,
  dispatch: Dispatch,
  url: string,
  jsonDecoder = (json: Object) => json,
  request: (...args: any[]) => Action,
  receiveSuccess: Function,
  receiveFailure: Function,
  formData?: FormData,
  headers: { [propName: string]: string } = {
    'Accept-Charset': 'application/json',
  },
) {
  const xhr = new XMLHttpRequest();

  function onLoad() {
    if (xhr.status >= 200 && xhr.status < 300) {
      const json = JSON.parse(xhr.responseText);
      const data = jsonDecoder(json.data);
      dispatch(receiveSuccess({ ...json, data }));
    } else
      dispatch(receiveFailure({ data: `${xhr.status} (${xhr.statusText})` }));
  }

  const onProgress = progressListener
    ? (event: ProgressEvent) =>
        progressListener(event.lengthComputable, event.loaded, event.total)
    : null;

  // POST start
  dispatch(request());
  xhr.open('POST', url, true);
  xhr.onload = onLoad;
  xhr.onprogress = onProgress;
  _.forOwn(headers, (value, key) => xhr.setRequestHeader(key, value));
  xhr.send(formData);

  return xhr;
}

function patch(
  dispatch: Dispatch,
  url: string,
  // eslint-disable-next-line no-unused-vars
  jsonDecoder = (json: Object) => json,
  request: (...args: any[]) => Action,
  receiveSuccess: Function,
  receiveFailure: Function,
  formData?: FormData,
  headers: { [propName: string]: string } = {},
) {
  const xhr = new XMLHttpRequest();

  function onLoad() {
    if (xhr.status >= 200 && xhr.status < 300) {
      dispatch(receiveSuccess(JSON.parse(xhr.responseText)));
    } else
      dispatch(
        receiveFailure({
          data: `${xhr.status} Error: ${xhr.statusText}`,
        }),
      );
  }

  // UPDATE start
  dispatch(request());

  xhr.open('PATCH', url, true);
  xhr.withCredentials = true;
  xhr.onload = onLoad;
  xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
  _.forOwn(headers, (value, key) => xhr.setRequestHeader(key, value));
  xhr.send(formData);

  return xhr;
}

function del(
  dispatch: Dispatch,
  url: string,
  // eslint-disable-next-line no-unused-vars
  jsonDecoder = (json: Object) => json,
  request: (...args: any[]) => Action,
  receiveSuccess: Function,
  receiveFailure: Function,
  formData?: FormData,
  headers: { [propName: string]: string } = {},
) {
  const xhr = new XMLHttpRequest();

  function onLoad() {
    if (xhr.status >= 200 && xhr.status < 300)
      dispatch(receiveSuccess(JSON.parse(xhr.responseText)));
    else
      dispatch(
        receiveFailure({
          data: `${xhr.status} Error: ${xhr.statusText}`,
        }),
      );
  }

  // DELETE start
  dispatch(request());

  xhr.open('DELETE', url, true);
  xhr.withCredentials = true;
  xhr.onload = onLoad;
  appendCredential(xhr);
  _.forOwn(headers, (value, key) => xhr.setRequestHeader(key, value));
  xhr.send(formData);

  return xhr;
}

// eslint-disable-next-line import/prefer-default-export
export function xmlHttpRequest(
  dispatch: Dispatch,
  method: HttpMethod,
  {
    url,
    jsonDecoder,
    request,
    receiveSuccess,
    receiveFailure,
    progressListener,
    formData = undefined,
    headers = {},
  }: XMLParameter & Partial<{ progressListener: (e: ProgressEvent) => any }>,
): XMLHttpRequest | void {
  const param = [
    dispatch,
    url,
    jsonDecoder,
    request,
    receiveSuccess,
    receiveFailure,
    formData,
    headers,
  ] as const;
  switch (method.toString().toUpperCase()) {
    case 'GET':
      return get(...param);
    case 'POST':
      return post(progressListener, ...param);
    case 'PATCH':
      return patch(...param);
    case 'DELETE':
      return del(...param);
    default:
      return undefined;
  }
}
