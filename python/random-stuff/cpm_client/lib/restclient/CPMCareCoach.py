import json
from datetime import date


class CPM_CareCoach(object):

    def __init__(self):
        self.care_coach_id = 0
        self.created_date = date.today()
        self.first_name = ''
        self.last_name = ''
        self.email_address = ''
        self.office_phone = ''
        self.extension = ''
        self.address_line1 = ''
        self.address_line2 = ''
        self.city = ''
        self.state_code = ''
        self.zipcode = ''

    def is_valid(self):
        if self.care_coach_id <= 0:
            return False
        if self.first_name is '':
            return False
        if self.email_address is '':
            return False
        if self.office_phone is '':
            return False
        if self.address_line1 is '':
            return False
        if self.city is '':
            return False
        if self.state_code is '':
            return False
        if self.zipcode is '':
            return False
        return True

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)
