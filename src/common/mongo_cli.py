import json
from src.common import logger
from pymongo import MongoClient
from bson.json_util import dumps
from src.common.log_decorator import automation_logger


class MongoCli:
    mongo_client = MongoClient('35.233.79.19', 27017)

    @classmethod
    @automation_logger(logger)
    def get_data_bases(cls):
        dbs = cls.mongo_client.list_database_names()
        logger.logger.info(f"List of DB's: {dbs}")
        return dbs

    @classmethod
    @automation_logger(logger)
    def find_by_query(cls, db_name, collection, query):
        db = cls.mongo_client.get_database(db_name)
        col = db.get_collection(collection)
        res = json.loads(dumps(col.find(query)[0]))
        logger.logger.info(f"Query result is: {res}")
        return res


# if __name__ == "__main__":
#     m = MongoCli
#     db_names = m.get_data_bases()[3]
#     db = m.mongo_client.get_database(db_names)
#     c = db.get_collection('areas')
#     r = m.find_by_query(db_names, 'areas', {"a": "1"})
#     pass
