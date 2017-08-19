# -*- coding: utf-8 -*-
import json
import requests

try:
    from thrift.protocol import fastbinary
except:
    fastbinary = None

class url(object):
    LINE_HOST_DOMAIN = 'https://gd2.line.naver.jp'
    LINE_NOMA_DOMAIN = 'https://gf.line.naver.jp'
    LINE_SECO_DOMAIN = 'https://gsx.line.naver.jp'

    LINE_AUTH_QUERY_PATH            = '/api/v4/TalkService.do'
    LINE_SESSION_LINE_QUERY_PATH    = '/authct/v1/keys/line'
    LINE_SESSION_NAVER_QUERY_PATH   = '/authct/v1/keys/naver'

    LINE_API_QUERY_PATH_FIR         = '/S4'
    LINE_API_QUERY_PATH_SEC         = '/F4'
    LINE_POLL_QUERY_PATH_FIR        = '/P4'
    LINE_POLL_QUERY_PATH_SEC        = '/E4'
    LINE_POLL_QUERY_PATH_THI        = '/H4'
    LINE_NORMAL_POLL_QUERY_PATH     = '/NP4'
    LINE_COMPACT_MESSAGE_QUERY_PATH = '/C5'
    LINE_CALL_QUERY_PATH            = '/V4'
    LINE_CERTIFICATE_PATH           = '/Q'
    LINE_CHAN_QUERY_PATH            = '/CH4'
    LINE_SHOP_QUERY_PATH            = '/SHOP4'

    UserAgent   = 'DESKTOP:MAC:10.10.2-YOSEMITE-x64(4.5.0)'
    AppName     = 'DESKTOPMAC 10.10.2-YOSEMITE-x64    MAC 4.5.0'
    port        = 443
    systemname  = 'VODKA-PC'
    ip          = '8.8.8.8'
    _session = requests.session()
    Headers = {}
    _pincode = None

    @classmethod
    def parseUrl(self, path):
        return self.LINE_HOST_DOMAIN + path

    @classmethod
    def get_json(self, url, allowHeader=False):
        if allowHeader is False:
            return json.loads(self._session.get(url).text)
        else:
            return json.loads(self._session.get(url, headers=self.Headers).text)

    @classmethod
    def set_Headers(self, argument, value):
        self.Headers[argument] = value
