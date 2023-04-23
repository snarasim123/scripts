import sys



class CareTeam(object):

    ct_id: int
    mongo_id: str
    pt_erehab_id: int
    pt_mongoid: str
    cc_id: int
    cc_mongoid: str

    def __init__(self):
        self.ct_id = 0
        self.mongo_id = '0x0'
        self.pt_erehab_id = 0
        self.pt_mongoid = '0x0'
        self.cc_id = 0
        self.cc_mongoid = '0x0'
        return None


    @property
    def careteam_id(self):
        return self.ct_id

    @careteam_id.setter
    def careteam_id(self, value):
        self.ct_id = value

    @property
    def careteam_mongo_id(self):
        return self.mongo_id

    @careteam_mongo_id.setter
    def careteam_mongo_id(self, value):
        self.mongo_id = value

    @property
    def patient_id(self):
        return self.pt_erehab_id

    @patient_id.setter
    def patient_id(self, value):
        self.pt_erehab_id = value

    @property
    def patient_mongoid(self):
        return self.pt_mongoid

    @patient_mongoid.setter
    def patient_mongoid(self, value):
        self.pt_mongoid = value

    @property
    def carecoach_id(self):
        return self.cc_id

    @carecoach_id.setter
    def carecoach_id(self, value):
        self.cc_id = value

    @property
    def carecoach_mongoid(self):
        return self.cc_mongoid

    @carecoach_mongoid.setter
    def carecoach_mongoid(self, value):
        self.cc_mongoid = value
