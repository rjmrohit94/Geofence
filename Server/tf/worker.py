import redis
from rq import Worker, Queue, Connection
from settings import REDIS_URL, REDIS_JOB_QUEUE_NAME

listen = [REDIS_JOB_QUEUE_NAME]

print(REDIS_URL)
conn = redis.from_url(REDIS_URL)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
