import sys
import time
import json
import requests
from utilities.httpstatus import http_status
from utilities.log_util import log_to_file, create_log_file

from DFCareTeam import CareTeam
from DFCareCoach import CareCoach
from DFPatient import Patient

devbase_url = 'https://dev-westus2-dfcore-fhir-lifecycle-service.azurewebsites.net'
stagebase_url = 'https://stage-westus2-dfcore-fhir-lifecycle-service.ontrak2-staging.appserviceenvironment.net'
prodbase_url = 'https://prod-westus2-dfcore-fhir-lifecycle-service.ontrak2.appserviceenvironment.net'
current_base_url = stagebase_url
fake_api = False


class DFClient(object):
    erehab_id: int = 0
    counter: int = 0
    error: int = 0
    log_file: str
    careteam: CareTeam
    patient: Patient
    carecoach: CareCoach

    def __init__(self):
        self.counter = 0
        self.careteam = CareTeam()
        self.patient = Patient()
        self.carecoach = CareCoach()
        self.log_file = create_log_file()
        return None

    def validate_careteam(self, erehab_id):
        self.erehab_id = erehab_id
        self.patient_read(self.erehab_id)
        self.careteam_read(self.patient.patient_mongo_id)
        return self.careteam

    def get_carecoach(self):
        return self.carecoach

    def get_patient(self):
        return self.patient

    def patient_read(self, mongo_id):
        # {{BaseUrl}}/R4/Patient/5dc1b80f77042212cdff611c
        base_url: str = current_base_url
        search_url: str = '{0}/R4/Patient/{1}'.format(base_url, mongo_id)
        op_success: bool = True

        headers = {
            'Content-Type': 'application/json',
        }

        if fake_api:
            time.sleep(1)
            log_to_file(self.log_file,
                        "Fake read Patient -> {0} , Header -> {1} , Url -> {2}\n"
                        .format(mongo_id, headers, search_url))
            self.counter += 1
            return None

        try:
            response = requests.get(search_url)
            log_to_file(self.log_file,
                        "Patient Mongo id {0},  HTTP status code -> {1}\n".format(mongo_id, response.status_code))
            if not response.ok:
                log_to_file(self.log_file,
                            "Error Patient,  Mongo id {0}, response content {1} \n".format(mongo_id,
                                                                                           response.text))
                self.error += 1
                return None
            response_dict = json.loads(response.text.encode('utf8'))

            identifiers = response_dict['identifier']
            for x in identifiers:
                if x['type']['text'] == 'eRehab_Id':
                    self.patient.erehab_id = x['value']
            self.patient.patient_mongo_id = response_dict['id']
            self.counter += 1
        except Exception as e:
            log_to_file(self.log_file, "Error Patient,  -> exception msg: " + str(e) + "\n")
            log_to_file(self.log_file,
                        "*** Error Patient, Exception  -> {0} , Url -> {1}\n".format(mongo_id, search_url))
            self.error += 1

        return self.patient

    def careteam_read(self, mongoid):
        base_url: str = current_base_url
        search_url: str = '{0}/R4/CareTeam/{1}'.format(base_url, mongoid)
        op_success: bool = True

        headers = {
            'Content-Type': 'application/json',
        }

        if fake_api:
            time.sleep(1)
            log_to_file(self.log_file,
                        "\nFake Read Careteam -> {0} , Header -> {1} , Url -> {2} "
                        .format(mongoid, headers, search_url))
            self.counter += 1
            return None

        try:
            response = requests.get(search_url)
            if not response.ok:
                log_to_file(self.log_file,
                            "Error , Careteam Mongo id {0}, response content {1} \n".format(mongoid, response.text))
                self.error += 1
                return None

            log_to_file(self.log_file,
                        "Careteam Mongo id {0}, HTTP status code -> {1}\n".format(mongoid, response.status_code))
            response_dict = json.loads(response.text.encode('utf8'))
            self.careteam.careteam_mongo_id = response_dict['id']
            self.careteam.cc_mongoid = response_dict['participant'][0]['member']['reference']
            self.careteam.pt_mongoid = response_dict['subject']['reference']
            self.counter += 1
        except Exception as e:
            log_to_file(self.log_file, "Error Careteam,  -> exception msg: " + str(e) + "\n")
            log_to_file(self.log_file,
                        "*** Error Careteam, Exception  -> {0} , Url -> {1}\n".format(mongoid, search_url))
            self.error += 1
        return self.careteam

    def carecoach_read(self, mongoid):
        # {{BaseUrl}}/R4/Practitioner/5d9e8579596bef3a465ca1b0
        base_url: str = current_base_url
        search_url: str = '{0}/R4/Practitioner/{1}'.format(base_url, mongoid)
        op_success: bool = True

        headers = {
            'Content-Type': 'application/json',
        }

        if fake_api:
            time.sleep(1)
            log_to_file(self.log_file,
                        "\nFake Read Carecoach -> {0} , Header -> {1} , Url -> {2} "
                        .format(mongoid, headers, search_url))
            self.counter += 1
            return None

        try:
            response = requests.get(search_url)
            if not response.ok:
                log_to_file(self.log_file,
                            "Error , CareCoach Mongo id {0}, response content {1} \n".format(mongoid, response.text))
                self.error += 1
                return None

            log_to_file(self.log_file,
                        "CareCoach Mongo id {0}, HTTP status code -> {1}\n".format(mongoid, response.status_code))
            response_dict = json.loads(response.text.encode('utf8'))
            self.carecoach.mongo_id = response_dict['id']
            self.counter += 1
        except Exception as e:
            log_to_file(self.log_file, "Error CareCoach,  -> exception msg: " + str(e) + "\n")
            log_to_file(self.log_file,
                        "*** Error CareCoach, Exception  -> {0} , Url -> {1}\n".format(mongoid, search_url))
            self.error += 1
        return self.carecoach
