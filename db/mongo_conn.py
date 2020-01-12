from pymongo import MongoClient

db_name = 'app_db'
cluster_collection = 'clusters'
machine_colletion = 'machines'


class MongoConnection:

    _client = None
    _clusters = None
    _machines = None

    @classmethod
    def _connect_to_mongodb(cls):
        client = MongoClient("mongodb+srv://bhargav:bhargav@cluster0-0hnph.mongodb.net/test?retryWrites=true&w=majority")
        cls._client = client

    def _get_database(self):
        if MongoConnection._client is None:
            self._connect_to_mongodb()
        db = MongoConnection._client[db_name]
        return db

    def _create_cluster_collection(self):
        if MongoConnection._clusters is None:
            database = self._get_database()
            MongoConnection._clusters = database[cluster_collection]

    def get_cluster_collection(self):
        self._create_cluster_collection()
        return MongoConnection._clusters

    def _create_machine_collection(self):
        if MongoConnection._machines is None:
            database = self._get_database()
            MongoConnection._machines = database[machine_colletion]

    def get_machine_collection(self):
        self._create_machine_collection()
        return MongoConnection._machines


