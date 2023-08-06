SIGNIN_FORM_MARKUP = """
<html>
<head>
    <meta content="text/html;charset=utf-8" http-equiv="Content-Type" />
    <meta content="utf-8" http-equiv="encoding" />
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" />
    <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
    <script src="https://sdk.amazonaws.com/js/aws-sdk-2.599.0.min.js"></script>
    <style>
    body, html { height: 100%; width: 100%; background-color: #ddd; }
    button { width: 100%; }
    table td { padding: 5px; }
    .box {
        background-color: #fefefe; border: 1px solid #999; border-radius: 10px; padding: 15px;
        box-shadow: 0 0 10px rgba(0,0,0,0.6);
    }
    .loading {
        background-image: url(https://upload.wikimedia.org/wikipedia/commons/7/7a/Ajax_loader_metal_512.gif);
        background-position: center center; background-size: 22px; background-repeat: no-repeat;
        color: rgba(0, 0, 0, 0.0);
    }
    .wrapper {
        display: flex; flex-direction: column;
        position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
    }
    .invisible {
        display: none;
    }
    </style>
    <script>
    const COGNITO_IDP_URL = 'http://localhost:4566';
    const COGNITO_REGION = 'us-east-1';
    const STATE = {};
    const IDP_PROVIDERS = %IDP_PROVIDERS%;
    const CALLBACK_URL = '%CALLBACK_URL%';

    $(function() {
        $('.signup:not(.signin)').hide();
        $('.newpass').hide();
        const client = getClient();
        const params = getParams();
        addIdpLinks();
        if (!params[0] || !params[1] || !params[2]) {
            alert('Error: Please provide query parameters "response_type", "client_id", and "redirect_uri" in the URL');
        }
    });
    function getClient() {
        const params = {
            region: getUrlParam('region') || COGNITO_REGION, endpoint: COGNITO_IDP_URL,
            accessKeyId: 'test', secretAccessKey: 'test'
        };
        return new AWS.CognitoIdentityServiceProvider(params);
    }
    function getParams() {
        const params = new URLSearchParams(location.search);
        return [getUrlParam('response_type'), getUrlParam('client_id'), getUrlParam('redirect_uri')];
    }
    function getUrlParam(name) {
        return new URLSearchParams(location.search).get(name);
    }
    function setLoading(element, loading = true) {
        loading && $(element).addClass('loading');
        !loading && $(element).removeClass('loading');
        $(element).prop('disabled', loading);
    }
    async function signIn() {
        setLoading('#signIn');
        const [response_type, client_id, redirect_uri] = getParams();
        const auth = {};
        const username = $('#username').val();
        const password = $('#password').val();
        const params = {
            ClientId: client_id, AuthFlow: 'USER_PASSWORD_AUTH', AuthParameters: auth,
            AuthParameters: { USERNAME: username, PASSWORD: password }
        };
        try {
            const result = await getClient().initiateAuth(params).promise();
            if (result.ChallengeName === 'NEW_PASSWORD_REQUIRED') {
                STATE.password = $('#password').val();
                STATE.username = $('#username').val();
                STATE.challenge = result;
                show('newpass');
            } else if (result.AuthenticationResult) {
                const data = { username: username, password: password };
                $.ajax({type: 'POST', url: window.location.href, data,
                success: function(result, status, request) {
                    const location = request.getResponseHeader('Location');
                    if (location) {
                        window.location.href = location;
                    } else {
                        alert(`Invalid redirect URL received: ${location}`);
                    }
                }, error: function(err) {
                    if (err.responseText) {
                        err = JSON.parse(err.responseText);
                        err = err.message || err;
                    }
                    alert(`An unknown error occurred: ${err}`);
                } });
            }
        } catch (e) {
            alert(`Unable to initiate authentication via Cognito API: ${e}`);
        } finally {
            setLoading('#signIn', false);
        }
    }
    async function signUp() {
        setLoading('#signUp', false);
        const [response_type, client_id, redirect_uri] = getParams();
        const username = $('#username').val();
        const password = $('#password').val();
        try {
            const params = { ClientId: client_id, Username: username, Password: password };
            const result = await getClient().signUp(params).promise();
            if (!result.UserSub) {
                throw new Error(`Unknown error occurred: ${result}`);
            }
            alert('Sign up succeeded. Please proceed to login.');
            show('signin');
        } catch (e) {
            alert(`Unable to sign up via Cognito API: ${e}`);
        } finally {
            setLoading('#signUp', false);
        }
    }
    async function updatePassword() {
        setLoading('#update');
        try {
            const newPass = $('#newPassword').val();
            const passConfirm = $('#confirmation').val();
            if (newPass !== passConfirm) {
                return alert('Passwords do not match.');
            }
            const [response_type, client_id, redirect_uri] = getParams();
            const params = {
                ChallengeName: 'NEW_PASSWORD_REQUIRED',
                ChallengeResponses: { NEW_PASSWORD: newPass, USERNAME: STATE.username },
                ClientId: client_id, Session: STATE.challenge.Session };
            const result = await getClient().respondToAuthChallenge(params).promise();
            if (!(result.AuthenticationResult || {}).AccessToken) {
                throw new Error(`Unknown error occurred: ${result}`);
            }
            alert('Password successfully updated. Please proceed to login.');
            show('signin');
        } catch (e) {
            alert(`Unable to update password via Cognito API: ${e}`);
        } finally {
            setLoading('#update', false);
        }
    }
    function idpLogin(idp_name) {
        const idp = IDP_PROVIDERS.filter(idp => idp.name === idp_name)[0];
        const details = idp.details || {};
        const url = `${details.authorize_url}?response_type=code&redirect_uri=${CALLBACK_URL}&` +
            `client_id=${details.client_id}&scope=${details.authorize_scopes}`;
        document.location.href = url;
    }
    function addIdpLinks() {
        IDP_PROVIDERS.forEach(idp => {
            const markup = `<button class="btn btn-primary signin" onClick="idpLogin('${idp.name}')">` +
                `${idp.name} (${idp.type || 'OIDC'})</button>`;
            $('#idpProviders').html($('#idpProviders').html() + markup);
        });
        if (!IDP_PROVIDERS.length) {
            $('#idpProvidersWrapper').hide();
        }
    }
    function show(clazz) {
        $('.signin').hide();
        $('.signup').hide();
        $('.newpass').hide();
        $('.' + clazz).show();
    }
    </script>
</head>
<body>
    <div class="wrapper">
    <div>
        <div class="box">
            <table>
                <tr>
                    <td colspan="2">
                        <span class="signin">Sign in with your username and password</span>
                        <span class="signup">Sign up with a new account</span>
                        <span class="newpass">Password needs to be updated. Please choose a new password below.</span>
                    </td>
                </tr><tr>
                    <td>
                        <span class="signin signup">Username:</span>
                        <span class="newpass">Password:</span>
                    </td>
                    <td>
                        <span class="signin signup"><input id="username" class="form-control"/></span>
                        <span class="newpass"><input id="newPassword" type="password" class="form-control"/></span>
                    </td>
                </tr><tr>
                    <td>
                        <span class="signin signup">Password:</span>
                        <span class="newpass">Confirm Password:</span>
                    </td>
                    <td>
                        <span class="signin signup"><input id="password" type="password" class="form-control"/></span>
                        <span class="newpass"><input id="confirmation" type="password" class="form-control"/></span>
                </tr><tr>
                    <td colspan="2">
                        <button class="btn btn-primary signin" id="signIn" onClick="signIn()">Sign In</button>
                        <button class="btn btn-primary signup" id="signUp" onClick="signUp()">Sign Up</button>
                        <button class="btn btn-primary newpass" id="update" onClick="updatePassword()">
                            Update Password</button>
                    </td>
                </tr><tr>
                    <td colspan="2">
                        <span class="signin">Need an account? <a href="#" onClick="show('signup')">
                            Sign up</a></span>
                        <span class="signup">Already have an account? <a href="#" onClick="show('signin')">
                            Sign in</a></span>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div id="idpProvidersWrapper">
        <div class="box">
            <span class="signin">Sign in via Identity Provider:</span>
            <div id="idpProviders"></div>
        </div>
    </div>
    </div>
</body>
</html>
"""
