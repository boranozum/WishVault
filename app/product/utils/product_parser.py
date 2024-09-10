import json
import os
import pickle
import requests

from bs4 import BeautifulSoup

from django.conf import settings

from base.functions import hash_url, get_price_and_currency
from product.models import ECommerceSite, Product


# from product.utils.category_predictor import CategoryPredictor


class ProductParser:
    def __init__(self):
        self.soup = None
        self.object_dir = os.path.join(settings.MEDIA_ROOT, 'product_parser')

    def save_soup(self, url):
        """
        For debugging purposes, save the soup object to a file to avoid 503 errors
        """
        if not os.path.exists(self.object_dir):
            os.makedirs(self.object_dir)

        hashed_url = hash_url(url)
        with open(os.path.join(self.object_dir, f'{hashed_url}.pkl'), 'wb') as file:
            pickle.dump(self.soup, file)

    def load_soup(self, url):
        """
        For debugging purposes, load the soup object from a file to avoid 503 errors
        """
        if not os.path.exists(os.path.join(self.object_dir, f'{url}.pkl')):
            return None

        with open(os.path.join(self.object_dir, f'{url}.pkl'), 'rb') as file:
            soup = pickle.load(file)

        return soup

    def retrieve_attribute(self, scrape_map, root=None, use_attr=None):
        if root:
            element = root.find(scrape_map['search_tag'], **scrape_map.get('search_attrs', {}))
        else:
            element = self.soup.find(scrape_map['search_tag'], **scrape_map.get('search_attrs', {}))

        if not element:
            return None

        if 'children' in scrape_map:
            return self.retrieve_attribute(scrape_map['children'], root=element, use_attr=use_attr)

        if use_attr:
            text = element.get(use_attr)
        else:
            text = element.text.strip()

        if text.isnumeric():
            return float(text)

        return text

    def parse(self, product_url):
        response = requests.get(product_url)
        if response.status_code == 200:
            self.soup = BeautifulSoup(response.text, 'html.parser')
            self.save_soup(product_url)
        else:
            self.soup = self.load_soup(product_url)
            if not self.soup:
                return None

        e_commerce_site = ECommerceSite.objects.get_from_url(product_url)
        if not e_commerce_site.exists():
            return None

        e_commerce_site_dict = e_commerce_site.values("id", "scrape_map").first()
        scrape_map = json.loads(e_commerce_site_dict['scrape_map'])

        price, currency = get_price_and_currency(self.retrieve_attribute(scrape_map['price']))
        title = self.retrieve_attribute(scrape_map['title'])
        product = {
            'cover_photo': self.retrieve_attribute(scrape_map['cover_photo'], use_attr='src'),
            'title': title,
            'price': price,
            'currency': currency,
            'url': product_url,
            'rating': self.retrieve_attribute(scrape_map['rating']),
            'sold_at_id': e_commerce_site_dict['id'],
            # 'category': CategoryPredictor().predict(title),
        }

        return product
