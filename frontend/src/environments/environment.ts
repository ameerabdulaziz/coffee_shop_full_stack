export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-k4h6i0dh.us', // the auth0 domain prefix
    audience: 'image', // the audience set for the auth0 app
    clientId: 'RjwxnfcudqujMdm1QnSWAKPXESiwPV4L', // the client id generated for the auth0 app
    callbackURL: 'http://127.0.0.1:4200', // the base url of the running ionic application.
  }
};
