from threading import RLock
from lib.mongo_docker.docker import stop_container, is_mongo_running, create_mongo_instance, start_mongo_instance
import atexit
import pymongo

KEY_ID = '_key_id'
DEFAULT_MONGO_IMAGE = 'mongo:4'

class MongoDB:
    def __init__(self, database_name="pipelineprod",
                 auto_commit=True, container_name="default", stop_at_exit=False, data_path=None):

        self.container_name = "mongo_4_" + container_name
        # self.container, self.server_url = create_mongo_instance(self.container_name, data_path=data_path)
        # if stop_at_exit:
        #     atexit.register(stop_container, self.container)
        # if self.container is None:
        self.container, self.server_url = start_mongo_instance(self.container_name, data_path=data_path)

        self.client = pymongo.MongoClient(self.server_url)
        # self.client.drop_database()
        self.database_name = database_name
        self.database = self.client[database_name]
        self.auto_commit = auto_commit
        self.lock = RLock()
        self.session, self.transaction = None, None

    def commit(self):
        self.session.commit_transaction()
        self.session.end_session()
        self.session, self.transaction = None, None

    def save(self):
        self.commit()

    def rollback(self):
        self.session.abort_transaction()
        self.session.end_session()
        self.session, self.transaction = None, None

    def start_transaction(self):
        if self.session is not None or self.transaction is not None:
            raise ValueError("Transaction already started")
        self.session = self.client.start_session()
        self.transaction = self.session.start_transaction()

    def __getitem__(self, key, collection):
        return collection.find_one({KEY_ID: key})

    def __setitem__(self, key, value, collection):
        doc = dict(value)
        doc[KEY_ID] = key
        collection.replace_one({KEY_ID: key}, doc, upsert=True, session=self.session)

    def __delitem__(self, key, collection):
        collection.delete_one({KEY_ID: key}, session=self.session)

    def __contains__(self, key, collection):
        return collection.find_one({KEY_ID: key}) is not None

    def __iter__(self, collection):
        for doc in collection.find():
            yield doc[KEY_ID], doc

    def __enter__(self):
        self.lock.acquire()
        self.start_transaction()

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is None:
                self.commit()
            else:
                self.rollback()
        finally:
            self.lock.release()

    def create_collection(self, collection_name):
        if collection_name not in self.database.collection_names():
            collection = self.database[collection_name]
            collection.create_index(KEY_ID, unique=True)
            return collection
