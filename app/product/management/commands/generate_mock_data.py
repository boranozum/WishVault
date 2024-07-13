import json
import logging
import os
import random
from django.utils import timezone
from django.conf import settings

from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Generate mock data for the project'
    command_name = 'generate_mock_data'

    def __init__(self):
        super(Command, self).__init__()
        self.logger = logging.getLogger()
        self.current_time = timezone.now()
        self.log_file_name = self.command_name

    def add_arguments(self, parser):
        parser.add_argument(
            '--log_level',
            type=str,
            default='WARNING',
            help='Log level for the logger',
        )
        parser.add_argument(
            '--verbose',
            const=True,
            action="store_const"
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=1000,
            help='Limit the number of records to be generated',
        )
        parser.add_argument(
            '--log_dir',
            type=str,
            default=os.path.join(settings.MEDIA_ROOT, 'healthcheck/logs', self.current_time.astimezone().strftime('%Y/%m/%d')),
            help='Logs will be printed to this directory. Non-absolute paths will automatically go under MEDIA_ROOT directory.',
        )

    def _pre_logging(self, **options):
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        if options['verbose']:
            log_level = getattr(logging, options['log_level'])
            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

        # If log directory does not exist, make it
        if not os.path.exists(options['log_dir']):
            os.makedirs(options['log_dir'])

        # Create unique file name with absolute path
        self.log_file_path = os.path.join(
            options['log_dir'],
            f"{self.log_file_name}_{self.current_time.astimezone().strftime(f'%H-%M-%S-%f')}.log",
        )

        file_handler = logging.FileHandler(self.log_file_path)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def handle(self, *args, **options):
        self._pre_logging(**options)
        self.logger.info('Mock data generation started')
        with open('product/management/mock_data.json', 'r') as mock_data_file:
            mock_data = json.load(mock_data_file)

        # E-Commerce site generation
        self.logger.info('Generating e-commerce site data')
        model = apps.get_model("product", mock_data['site']['model'])
        count = 0
        site_ids = []
        for site in mock_data['site']['data']:
            self.logger.info(f'Generating data for {site["name"]}')
            site['created_by_id'] = 0
            instance, is_created = model.objects.update_or_create(**site)
            if is_created:
                count += 1
            site_ids.append(instance.id)

        self.logger.info(f'{count} E-commerce site generated')

        # Product generation
        self.logger.info('Generating product data')
        model = apps.get_model("product", mock_data['product']['model'])
        count = 0
        for idx, product in enumerate(mock_data['product']['data']):
            self.logger.info(f'Generating data for {product["name"]}')
            product['created_by_id'] = 0
            name = product.pop('name')
            _, is_created = model.objects.update_or_create(name=name, sold_at_id=random.choice(site_ids), defaults=product)
            if is_created:
                count += 1

            if idx == options['limit']:
                break


        self.logger.info(f'{count} products generated')
        self.logger.info('Mock data generation completed')
        self.logger.info(f'Log file saved at {self.log_file_path}')
