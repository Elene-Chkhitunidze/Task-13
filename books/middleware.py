import time
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time

        logger.info(f'Request to {request.path} took {duration:.4f} seconds')

        return response
