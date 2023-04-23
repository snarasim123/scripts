import time
import json
import requests
from .CPMCareCoach import CPM_CareCoach

stagebase_url = 'https://stage-westus2-dfappl-careportal-migration-api.ontrak2-staging.appserviceenvironment.net'
prodbase_url =  'https://prod-westus2-dfappl-careportal-migration-api.ontrak2.appserviceenvironment.net'

fake_api = False


# noinspection PyBroadException
class CPM_Client(object):
    cpm_carecoach: CPM_CareCoach
    env: str = ''
    prod: bool = False
    stage: bool = True
    current_base_url: str = ''
    response: dict

    def __init__(self):
        self.cpm_carecoach = CPM_CareCoach()
        self.env = 'stage'
        self.current_base_url = stagebase_url
        self.response = dict()

    def get_carecoach(self):
        return self.cpm_carecoach

    def set_carecoach(self, **kwargs):
        for key, value in kwargs.items():
            if key is 'carecoach_id':
                self.cpm_carecoach.care_coach_id = value
            elif key is 'created_date':
                self.cpm_carecoach.created_date = value
            elif key is 'first_name':
                self.cpm_carecoach.first_name = value
            elif key is 'last_name':
                self.cpm_carecoach.last_name = value
            elif key is 'email_address':
                self.cpm_carecoach.email_address = value
            elif key is 'office_phone':
                self.cpm_carecoach.office_phone = value
            elif key is 'extension':
                self.cpm_carecoach.extension = value
            elif key is 'address_line1':
                self.cpm_carecoach.address_line1 = value
            elif key is 'address_line2':
                self.cpm_carecoach.address_line2 = value
            elif key is 'city':
                self.cpm_carecoach.city = value
            elif key is 'state_code':
                self.cpm_carecoach.state_code = value
            elif key is 'zipcode':
                self.cpm_carecoach.zipcode = value

    def carecoach_read(self):
        base_url: str = self.current_base_url
        search_url: str = '{0}/v1/catasys/CareCoach'.format(base_url)
        op_success: bool = True

        headers = {
            'Content-Type': 'application/json',
        }

        if fake_api:
            time.sleep(1)
            return None

        try:
            response = requests.get(search_url)
            if not response.ok:
                return None

            response_dict = json.loads(response.text.encode('utf8'))
            self.cpm_carecoach.mongo_id = response_dict['id']
        except Exception as e:
            pass
        return self.cpm_carecoach

    def carecoach_post(self):
        base_url: str = self.current_base_url
        post_url: str = '{0}/v1/catasys/CareCoach'.format(base_url)
        op_success: bool = True

        headers = {
            'Content-Type': 'application/json;charset=utf-8',
        }

        try:
            print('Posting to url {}\n'.format(post_url))
            print('Posting header {}\n'.format(headers))
            print('Posting json {}\n'.format(self.cpm_carecoach.toJson()))
            response = requests.post(post_url, headers=headers, json=json.loads(self.cpm_carecoach.toJson()))
            if not response.ok:
                print('Error posting Carecoach {}'.format(response.text))
                return None

            response_dict = json.loads(response.text.encode('utf8'))
            self.response = response_dict
        except Exception as e:
            print('Exception posting Carecoach - {}'.format(e))
        return self.response

    def set_env(self, **kwargs):
        for key, value in kwargs.items():
            if key is 'prod':
                self.prod = True
                self.stage = False
                self.current_base_url = prodbase_url

            if key is 'stage':
                self.prod = False
                self.stage = True
                self.current_base_url = stagebase_url

