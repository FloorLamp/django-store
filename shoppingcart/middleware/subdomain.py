import threading
from django.conf import settings

_request_local = threading.local()

class SubdomainMiddleware:
    def process_request(self, request):
        """Parse out the subdomain from the request"""
        request.subdomain = 'default'
        host = request.META.get('HTTP_HOST', '')
        host_s = host.replace('www.', '').split('.')
        if len(host_s) > 2:
            request.subdomain = ''.join(host_s[:-2])
        _request_local.subdomain = request.subdomain
        
class DatabaseRouter(object):
    def _default_db(self):
        if hasattr(_request_local, 'subdomain') and _request_local.subdomain in settings.DATABASES:
            return _request_local.subdomain
        else:
            return 'default'
    def db_for_read(self, model, **hints):
        return self._default_db()
    def db_for_write(self, model, **hints):
        return self._default_db()