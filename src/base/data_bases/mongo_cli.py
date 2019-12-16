import json
from src.base.utils import logger
from pymongo import MongoClient
from bson.json_util import dumps
from src.base.automation_error import AutomationError
from src.base.utils.log_decorator import automation_logger


class MongoCli:
    def __init__(self):
        self.mongo_client = MongoClient('35.233.79.19', 27017)

    @automation_logger(logger)
    def get_data_bases(self):
        try:
            dbs = self.mongo_client.list_database_names()
            logger.logger.info(f"List of DB's: {dbs}")
            return dbs
        except Exception as e:
            logger.logger.error(f"{e}")
            raise AutomationError(f"get_data_bases failed with error: {e}")

    @automation_logger(logger)
    def find_by_query(self, db_name, collection, query):
        try:
            db = self.mongo_client.get_database(db_name)
            col = db.get_collection(collection)
            res = json.loads(dumps(col.find(query)[0]))
            logger.logger.info(f"Query result is: {res}")
            return res
        except Exception as e:
            logger.logger.error(f"{e}")
            raise AutomationError(f"find_by_query failed with error: {e}")
