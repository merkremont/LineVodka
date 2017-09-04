# -*- coding: utf-8 -*-
import json ,rsa

from ..LineThrift import TalkService
from ..LineThrift import MessageService
from ..LineThrift.ttypes import *

from .LineServer import url

from thrift.transport import THttpClient
from thrift.protocol import TCompactProtocol

from .LineTransport import LineTransport
from .LineCallback import LineCallback

try:
    from thrift.protocol import fastbinary
except:
    fastbinary = None

class LineApi(object):
    _thriftTransport = None
    _thriftProtocol = None
    isLogin = False
    revision = None
    authToken = ""
    certificate = ""

    def __init__(self):
        self._transportOpen(url.LINE_HOST_DOMAIN)
        self.callback = LineCallback(self.defaultCall)
        self.urls=url()
        self.urls.set_Headers('User-Agent', url.UserAgent)
        self.urls.set_Headers('X-Line-Application', url.AppName)

    def onLogin(self):
        self.revision = self._client.getLastOpRevision()
        self.isLogin = True

    def _transportOpen(self, host, path=None):
        if path is not None:
            self._thriftTransport = LineTransport(host + path)
        else:
            self._thriftTransport = LineTransport(host)
        self._thriftProtocol = TCompactProtocol.TCompactProtocol(
            self._thriftTransport)
        self._client = TalkService.Client(self._thriftProtocol)

    def _login(self, email, passwordd, certificate=None, loginName=url.systemname):
        self._thriftTransport.targetPath(url.LINE_AUTH_QUERY_PATH)
        session_json = url.get_json(url.parseUrl(url.LINE_SESSION_LINE_QUERY_PATH))
        self.certificate = certificate
        session_key = session_json['session_key']
        message = (chr(len(session_key)) + session_key +
                   chr(len(email)) + email +
                   chr(len(passwordd)) + passwordd).encode('utf-8')
        keyname, n, e = session_json['rsa_key'].split(",")
        pub_key = rsa.PublicKey(int(n, 16), int(e, 16))
        crypto = rsa.encrypt(message, pub_key).encode('hex')
        self._thriftTransport.targetPath(url.LINE_AUTH_QUERY_PATH)
        result = self._client.loginWithIdentityCredentialForCertificate(
            IdentityProvider.LINE, keyname, crypto, True, '127.0.0.1', loginName, certificate)

        if result.type == 3:
            url._pincode = result.pinCode
            self.callback.Pinverified(url._pincode)
            getAccessKey = url.get_json(
                url.parseUrl(url.LINE_CERTIFICATE_PATH), allowHeader=True)
            self.verifier = getAccessKey['result']['verifier']
            result = self._client.loginWithVerifierForCerificate(self.verifier)
            self.certificate = result.certificate
            self.authToken = result.authToken
            self.urls.set_Headers('X-Line-Access', result.authToken)

            self._thriftTransport.setAccesskey(self.authToken)
            self.onLogin()
            self._thriftTransport.targetPath(url.LINE_API_QUERY_PATH_FIR)

        elif result.type == 2:
            pass

        elif result.type == 1:
            self.authToken = result.authToken
            self.urls.set_Headers('X-Line-Access', result.authToken)
            self._thriftTransport.setAccesskey(self.authToken)
            self.onLogin()
            self._thriftTransport.targetPath(url.LINE_API_QUERY_PATH_FIR)

    def _tokenLogin(self, authToken):
        self._thriftTransport.targetPath(url.LINE_AUTH_QUERY_PATH)
        self.urls.set_Headers('X-Line-Access', authToken)
        self._thriftTransport.setAccesskey(authToken)
        self.authToken = authToken
        self.onLogin()
        self._thriftTransport.targetPath(url.LINE_API_QUERY_PATH_FIR)

    def _qrLogin(self, keepLoggedIn=True, systemName=url.systemname):
        self._thriftTransport.targetPath(url.LINE_AUTH_QUERY_PATH)
        qr = self._client.getAuthQrcode(keepLoggedIn, systemName)
        self.callback.QrUrl("line://au/q/" + qr.verifier)
        url.set_Headers('X-Line-Application', url.AppName)
        url.set_Headers('X-Line-Access', qr.verifier)
        verified = url.get_json(
            url.parseUrl(url.LINE_CERTIFICATE_PATH), allowHeader=True)
        vr = verified['result']['verifier']
        lr = self._client.loginWithVerifierForCertificate(vr)
        self._thriftTransport.setAccesskey(lr.authToken)
        self.authToken = lr.authToken
        print self.authToken
        self.onLogin()
        self._thriftTransport.targetPath(url.LINE_API_QUERY_PATH_FIR)

    def setCallback(self, callback):
        self.callback = LineCallback(callback)

    def endPoint(self, path):
        self._thriftTransport.targetPath(path)

    def defaultCall(self, str):
        print str

    def _logout(self):
        self._client.logoutSession(self.authToken)
        self._thriftTransport.setAccesskey("")
