import requests
import logging

from requests.adapters import HTTPAdapter
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
TIMEOUT = (1.0, 3.0)
HEADERS = {}


class Client(BaseModel):
    api_key: str
    url: str = 'http://localhost:8080'

    def create_project(self, *args, **kwargs):
        from .project import Project
        return Project(self, *args, **kwargs)

    def create_config(self, *args, **kwargs):
        from .label_config import LabelConfig
        return LabelConfig(self, *args, **kwargs)

    def get_session(self):
        session = requests.Session()
        session.headers.update(HEADERS)
        session.mount('http://', HTTPAdapter(max_retries=MAX_RETRIES))
        session.mount('https://', HTTPAdapter(max_retries=MAX_RETRIES))
        return session

    def make_request(self, method, url, *args, **kwargs):
        session = self.get_session()
        if not 'timeout' in kwargs:
            kwargs['timeout'] = TIMEOUT
        logger.debug(f'{method}: {url} with args={args}, kwargs={kwargs}')
        response = session.request(method, url, *args, **kwargs)
        response.raise_for_status()
        json_response = response.json()
        logger.debug(f'Response: {json_response}')
        return json_response
