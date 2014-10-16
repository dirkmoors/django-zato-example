from django.conf import settings

from zato.client import AnyServiceInvoker

ZATO_SETTINGS = getattr(settings, "ZATO_SETTINGS", {})
ZATO_HOST = ZATO_SETTINGS.get("host", "localhost")
ZATO_PORT = ZATO_SETTINGS.get("port", 11223)
ZATO_PATH = ZATO_SETTINGS.get("path", "/")
ZATO_USER = ZATO_SETTINGS.get("user", "zato")
ZATO_PASSWD = ZATO_SETTINGS.get("passwd", "zato")

class ZatoMiddleware(object):
    def process_request(self, req):
        req.zato_client = AnyServiceInvoker(
            'http://%s:%s'%(ZATO_HOST, ZATO_PORT),
            ZATO_PATH,
            (ZATO_USER, ZATO_PASSWD))
