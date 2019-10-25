import { ActionReceive, ActionReceiveFactory } from '../constant/lib';

export function getCookie(name: string): string {
  const value = `; ${document.cookie}`;
  const parts = value.split(`;  ${name}=`);
  if (parts.length === 2)
    // @ts-ignore
    return parts
      .pop()
      .split(';')
      .shift();
  return '';
}

export function deleteCookie(name: string) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`;  ${name}=`);
  if (parts.length === 2)
    document.cookie = parts[0] + parts[1].slice(`${parts[1]};`.indexOf(';'));
}

export function appendCredential(xhr: XMLHttpRequest) {
  xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
}

/**
 * Wrap a sequence of inserted function
 * @param {...function(...param: any): any} funcs: a sequence of callback function before the actual returned
 * function. The last item of [funcs] accept one argument and return its result.
 * @return {function(json: Object): ActionReceiveSuccess}
 */
export function callbackWrapper<D, J>(
  ...funcs: CallableFunction[]
): (json: Object) => ActionReceiveFactory<ActionReceive<D>, J> {
  return json => {
    const tail = funcs.splice(funcs.length - 1)[0];
    funcs.forEach(func => func());
    return tail(json);
  };
}

export function setTitleEffectFactory(title: string): () => () => void {
  return () => {
    const titleOld = document.title;
    document.title = title;
    return () => {
      document.title = titleOld;
    };
  };
}

export function stringToColor(str: string): string {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash);
  }
  let colour = '#';
  for (let i = 0; i < 3; i++) {
    const value = (hash >> (i * 8)) & 0xff;
    colour += `00${value.toString(16)}`.substr(-2);
  }
  return colour;
}

/**
 * Get object unique ID.
 */
let id = 0;

export function getUniqueID() {
  id += 1;
  return id.toString();
}
