import hashlib
import redis
from django.core.cache import cache
import traceback


def hash_url(url):
    """
    Hash the URL to avoid long filenames
    """
    return hashlib.md5(url.encode()).hexdigest()


def get_price_and_currency(text):
    """
    Extract the price and currency from a string
    """
    price = None
    currency = None

    for word in text.split():
        if word.replace('.', '').replace(',', '').isnumeric():
            price = float(word.replace(',', '.'))
        elif word.isalpha():
            currency = word.upper()

    return price, currency


def is_redis_available():
    try:
        client = cache.client.get_client()
        client.ping()
        return client
    except redis.ConnectionError:
        print('Redis connection failed!')
        print(traceback.format_exc())

    return None
