from prometheus_client import Counter, generate_latest
from flask import request

http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP Requests',
    ['method', 'endpoint', 'status_code']
)


def prometheus_middleware(func):
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            http_requests_total.labels(
                method=request.method,
                endpoint=request.path,
                status_code=response.status
            ).inc()
        except Exception as e:
            http_requests_total.labels(
                method=request.method,
                endpoint=request.path,
                status_code=500
            ).inc()
            raise e
        return response

    wrapper.__name__ = func.__name__
    return wrapper


def get_latest_metrics():
    return generate_latest()
