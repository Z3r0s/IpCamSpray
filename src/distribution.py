import redis
from rq import Queue
from src.request_handler import perform_request

redis_conn = redis.Redis()
task_queue = Queue(connection=redis_conn)

def enqueue_task(target_url, user, pwd, proxy_config):
    task_queue.enqueue(perform_request, target_url, (user, pwd), proxy_config)