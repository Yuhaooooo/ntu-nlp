import json

import requests_async as requests

from config import configs
from serving import Controller, mapping
from serving.controller import json_wrapper


class MaxAudioClassifierController(Controller):
    def __init__(self, fast_api):
        super().__init__(fast_api, base_url='/review')

        mac_configs = configs['review_classifier']
        self._host_url = 'http://{}:{}'.format(mac_configs['host'], mac_configs['port'])

    @mapping('predict', methods=['POST'])
    async def classify(self, *, sentence: str):
        params = {'sentence': sentence}

        response = await requests.post(self._host_url + '/predict', params=params)

        # parse response
        response_dict = json.loads(response.text)
        data = None
        message = ''
        if response.ok:
            data = {
                'review': response_dict['review'],
            }
        else:
            message = response_dict['message']

        return json_wrapper(data, status_code=response.status_code, message=message)
