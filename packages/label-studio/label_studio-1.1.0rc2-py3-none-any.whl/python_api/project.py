import time

from typing import Optional, Union, List
from .label_config import LabelConfig
from .common import ClientObject


class Project(ClientObject):
    label_config: LabelConfig
    title: Optional[str]

    def is_completed(self):
        status = self.client.make_request(method='GET', url=f'/api/projects/{self.id}/status')
        return status.get('is_completed')

    def import_tasks_from_list(self, data: List[str]):
        """
        Import tasks from list of strings
        :param data: list of strings, each item is a text representation of task (text or url
        :return:
        """
        data_fields = self.label_config.get_data_fields()
        if len(data_fields) > 1:
            raise ValueError(f"Can't create tasks from list with multiple data fields: {data_fields}")
        data_field = data_fields[0]
        tasks = [{data_field: item} for item in data]
        self.client.make_request(method='POST', url=f'/api/projects/{self.id}/import', json=tasks)

    def annotate(self):
        """
        Wait until annotation process is finished
        :return:
        """
        while not self.is_completed():
            time.sleep(10)

    def get_results(self, minify=False):
        """
        Get annotation results in specified format
        :param minify: if True, outputs minified form of annotation results, otherwise raw full JSON results
        :return:
        """
        results = self.client.make_request(method='GET', url=f'/api/projects/{self.id}/export?raw=true')
        if minify:
            results = self.label_config.minify_results(results)
        return results
