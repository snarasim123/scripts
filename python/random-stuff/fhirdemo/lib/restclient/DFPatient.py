import sys



class Patient(object):
    id: int
    mongo_id: str

    def __init__(self):
        self.id = 0
        self.mongo_id = '0x0'
        return None


    @property
    def erehab_id(self):
        return self.id

    @erehab_id.setter
    def erehab_id(self, value):
        self.id = value

    @property
    def patient_mongo_id(self):
        return self.mongo_id

    @patient_mongo_id.setter
    def patient_mongo_id(self, value):
        self.mongo_id = value

