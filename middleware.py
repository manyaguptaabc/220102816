import os, json
from django.utils import timezone

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        os.makedirs('logs', exist_ok=True)
        self.fn = os.path.join('logs', 'requests.log')

    def __call__(self, req):
        ts = timezone.now().isoformat()
        try:
            b = req.body.decode()[:200]
        except:
            b = ''
        data = {'time': ts, 'm': req.method, 'p': req.path, 'ip': req.META.get('REMOTE_ADDR',''), 'body':b}
        resp = self.get_response(req)
        data['status'] = resp.status_code
        with open(self.fn, 'a') as f:
            f.write(json.dumps(data)+'\n')
        return resp
