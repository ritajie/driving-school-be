import logging
from urllib.parse import urljoin

import curl
import requests
from django.conf import settings

_WECHAT_API = "https://api.weixin.qq.com"
_ACCESS_TOKEN_PATH = f"/cgi-bin/token?grant_type=client_credential&appid={settings.WECHAT_APP_ID}&secret={settings.WECHAT_APP_SECRET}"
_WECHAT_ACCESS_TOKEN_PATH = f"/sns/oauth2/access_token?appid={settings.WECHAT_APP_ID}&secret={settings.WECHAT_APP_SECRET}&code={'{}'}&grant_type=authorization_code"
_WECHAT_USER_INFO_PATH = "/sns/userinfo?access_token={}&openid=OPENID&lang=zh_CN"
_SEND_MESSAGE_PATH = "/cgi-bin/message/template/send?access_token={}"

ACCESS_TOKEN_URL = urljoin(_WECHAT_API, _ACCESS_TOKEN_PATH)
WECHAT_ACCESS_TOKEN_URL = urljoin(_WECHAT_API, _WECHAT_ACCESS_TOKEN_PATH)
WECHAT_USER_INFO_URL = urljoin(_WECHAT_API, _WECHAT_USER_INFO_PATH)
SEND_MESSAGE_URL = urljoin(_WECHAT_API, _SEND_MESSAGE_PATH)


def wechat_request(url: str, method: str, **kwargs) -> dict:
    res = requests.request(method, url, **kwargs)
    res.encoding = "utf-8"
    logging.info(curl.parse(res, return_it=True))
    logging.info(
        f"wechat_request: url={url} method={method} kw={kwargs} resp={res.content.decode('utf-8')}",
    )
    if res.status_code != requests.codes.ok:
        raise Exception("wechat request error")
    return res.json()
