import json
import logging
import os
from glob import glob

from elasticsearch import Elasticsearch

import settings


def init_schema():
    es = Elasticsearch(f'{settings.ES_SCHEMA}://{settings.ES_HOST}:{settings.ES_PORT}',
                       max_retries=settings.ES_MAX_RETRIES)

    for path in glob(settings.ES_SCHEMAS_PATH):
        with open(path, 'r') as f:
            try:
                filename = os.path.basename(path)
                index = filename.split('.')[0]
                schema = json.load(f)
                es.indices.create(index=index, settings=schema['settings'], mappings=schema['mappings'])
                logging.info(f'{index} index configured')
            except Exception as e:
                logging.info(e)


if __name__ == '__main__':
    init_schema()
