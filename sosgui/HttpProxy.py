from django.shortcuts import get_object_or_404, render_to_response, redirect
from httpproxy import views
# from httpproxy.views import HttpProxy

class HttpProxyAuth(views.HttpProxy):

    base_url = None

    def dispatch(self, request, url, *args, **kwargs):
        log = open('/tmp/proxy','a')
        try:
            if request.user.is_authenticated():
                return super(HttpProxyAuth, self).dispatch(request, url, args, kwargs)
            return redirect('/')
        except Exception, e:
            log.write(repr(e)+'\n')
            return e

