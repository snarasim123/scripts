import sys



class CareCoach(object):
    id: int
    mongo_id: str

    def __init__(self):
        self.id = 0
        self.mongo_id = '0x0'
        return None


    @property
    def carecoach_id(self):
        return self.id

    @carecoach_id.setter
    def carecoach_id(self, value):
        self.id = value


    @property
    def carecoach_mongo_id(self):
        return self.mongo_id

    @carecoach_mongo_id.setter
    def carecoach_mongo_id(self, value):
        self.mongo_id = value

