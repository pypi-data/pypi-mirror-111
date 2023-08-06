import hmac
import base64
import smtplib
from base64 import b64encode
from smtplib import SMTPException, SMTPAuthenticationError
from localstack.utils.common import to_bytes, to_str


def base64_encode(s):
    result = to_str(b64encode(to_bytes(s))).strip()
    return result


class SMTP(smtplib.SMTP):

    # this patch fixes the following problem in smtplib which causes
    # the code to fail when connecting to some SMTP servers
    # https://bugs.python.org/issue27820

    def login(self, user, password):
        """Log in on an SMTP server that requires authentication.

        The arguments are:
            - user:     The user name to authenticate with.
            - password: The password for the authentication.

        If there has been no previous EHLO or HELO command this session, this
        method tries ESMTP EHLO first.

        This method will return normally if the authentication was successful.

        This method may raise the following exceptions:

         SMTPHeloError            The server didn't reply properly to
                                  the helo greeting.
         SMTPAuthenticationError  The server didn't accept the username/
                                  password combination.
         SMTPException            No suitable authentication method was
                                  found.
        """

        def encode_cram_md5(challenge, user, password):
            challenge = base64.decodestring(challenge)
            response = user + ' ' + hmac.HMAC(password, challenge).hexdigest()
            return base64_encode(response)

        def encode_plain(user, password):
            return base64_encode('\0%s\0%s' % (user, password))

        AUTH_PLAIN = 'PLAIN'
        AUTH_CRAM_MD5 = 'CRAM-MD5'
        AUTH_LOGIN = 'LOGIN'

        self.ehlo_or_helo_if_needed()

        if not self.has_extn('auth'):
            raise SMTPException('SMTP AUTH extension not supported by server.')

        # Authentication methods the server supports:
        authlist = self.esmtp_features['auth'].split()

        # List of authentication methods we support: from preferred to
        # less preferred methods. Except for the purpose of testing the weaker
        # ones, we prefer stronger methods like CRAM-MD5:
        preferred_auths = [AUTH_CRAM_MD5, AUTH_PLAIN, AUTH_LOGIN]

        # Determine the authentication method we'll use
        authmethod = None
        for method in preferred_auths:
            if method in authlist:
                authmethod = method
                break

        if authmethod == AUTH_CRAM_MD5:
            tmp = self.docmd('AUTH', AUTH_CRAM_MD5)
            code = tmp[0]
            resp = tmp[1]
            if code == 503:
                # 503 == 'Error: already authenticated'
                return (code, resp)
            tmp = self.docmd(encode_cram_md5(resp, user, password))
            code = tmp[0]
            resp = tmp[1]
        elif authmethod == AUTH_PLAIN:
            tmp = self.docmd('AUTH', AUTH_PLAIN + ' ' + encode_plain(user, password))
            code = tmp[0]
            resp = tmp[1]
        elif authmethod == AUTH_LOGIN:
            # PATCH: instead of sending the login name directly, wait for server response

            # Example 1 (original logic in smtplib):
            #     250 AUTH LOGIN PLAIN CRAM-MD5
            #     auth login avlsdkfj
            #     334 UGFzc3dvcmQ6
            #     avlsdkfj
            #
            # Example 2 (our patch):
            #     250 AUTH LOGIN PLAIN CRAM-MD5
            #     auth login
            #     334 VXNlcm5hbWU6
            #     avlsdkfj
            #     334 UGFzc3dvcmQ6
            #     avlsdkfj

            # original code:
            # (code, resp) = self.docmd('AUTH',
            #     '%s %s' % (AUTH_LOGIN, encode_base64(user, eol='')))
            # if code != 334:
            #     raise SMTPAuthenticationError(code, resp)
            # (code, resp) = self.docmd(encode_base64(password, eol=''))

            encoded_username = base64_encode(user)
            encoded_password = base64_encode(password)
            tmp = self.check_codes(encoded_username, encoded_password)
            code = tmp[0]
            resp = tmp[1]
        elif authmethod is None:
            raise SMTPException('No suitable authentication method found.')

        if code not in (235, 503):
            # 235 == 'Authentication successful'
            # 503 == 'Error: already authenticated'
            raise SMTPAuthenticationError(code, resp)
        return (code, resp)

    def check_codes(self, encoded_username, encoded_password):
        AUTH_LOGIN = 'LOGIN'

        # new code:
        tmp = self.docmd('AUTH', AUTH_LOGIN)
        code = tmp[0]
        resp = tmp[1]
        if code != 334:
            raise SMTPAuthenticationError(code, resp)

        tmp = self.docmd(encoded_username)
        code = tmp[0]
        resp = tmp[1]
        if code != 334:
            raise SMTPAuthenticationError(code, resp)

        tmp = self.docmd(encoded_password)
        code = tmp[0]
        resp = tmp[1]
        if code != 235:
            raise SMTPAuthenticationError(code, resp)

        return code, resp
