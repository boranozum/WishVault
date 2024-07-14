import hashlib


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
