import os
from dotenv import load_dotenv
load_dotenv()

MONGODB_SETTINGS = {
    'db': os.getenv('MONGO_DATABASE'),
    'host': os.getenv('MONGO_HOST'),
    'port': int(os.getenv('MONGO_PORT'))
}
REDIS_HOSTNAME = os.getenv('REDIS_HOSTNAME')
REDIS_PORT_NO = os.getenv('REDIS_PORT_NO')
REDIS_URL = 'redis://{0}:{1}'.format(REDIS_HOSTNAME, REDIS_PORT_NO)
