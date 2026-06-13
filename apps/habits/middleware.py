import time
import logging

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        user = request.user if request.user.is_authenticated else 'Анонім'

        response = self.get_response(request)

        duration = round((time.time() - start_time) * 1000, 2)

        print(f'[{request.method}] {request.path} | юзер: {user} | {duration}мс | статус: {response.status_code}')

        return response
        