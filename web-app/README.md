This sub-project builds the React frontend for NTU NLP course.
## Install  
First, install npm dependencies:
```shell script
npm i
```

Before running or build, you should add the `src/config.js` according to your API server.  
The form of `config.js` is:
```ecmascript 6
export const api_host = '<server ip>';
export const api_port = 8000;    // port number
```

## Development Run  
Please run the script `npm start`.

## Product Run
To builds the app for production to the `build` folder, please run `npm run build`.
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more 
information.

**Use Docker**  
Build docker image by:
```shell script
docker build -t ntu-nlp-frontend .
```
And run docker by:
```shell script
docker run -p 80:80 ntu-nlp-frontend
```

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).
