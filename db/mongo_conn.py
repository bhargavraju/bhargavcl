from pymongo import MongoClient
import os

db_name = os.environ.get('MONGO_DB_NAME', 'app_db')
cluster_collection = os.environ.get('MONGO_CL_COLL', 'clusters')
machine_colletion = os.environ.get('MONGO_M_COLL', 'machines')


class MongoConnection:

    _client = None
    _clusters = None
    _machines = None

    @classmethod
    def _connect_to_mongodb(cls):
        client = MongoClient("localhost", 27017)
        cls._client = client
        # if mongo_auth_enabled:
        #     cls._client.the_database.authenticate(mongo_user, mongo_password, source=self.mongo_auth_db)

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


if __name__ == '__main__':
    print(db_name, cluster_collection, machine_colletion)
