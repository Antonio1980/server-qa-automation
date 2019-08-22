import requests
from bs4 import BeautifulSoup
from src.common import logger
from elasticsearch import Elasticsearch
from config_definitions import BaseConfig
from elasticsearch.serializer import JSONSerializer
from src.common.automation_error import AutomationError
from src.common.log_decorator import automation_logger


class SetEncoder(JSONSerializer):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return JSONSerializer.default(self, obj)


class KibanaCli:
    if "kibana" in BaseConfig.KIBANA:
        kibana_client = Elasticsearch([{'host': BaseConfig.KIBANA}], serializer=SetEncoder())
    else:
        kibana_client = Elasticsearch([{'host': BaseConfig.KIBANA, 'port': int(BaseConfig.KIBANA_PORT)}],
                                      serializer=SetEncoder())

    @classmethod
    @automation_logger(logger)
    def check_connection(cls):
        try:
            _response = requests.get(BaseConfig.KIBANA_HOST + ":" + BaseConfig.KIBANA_PORT)
            assert _response.status_code == 200
            assert _response.reason == "OK"
            content = BeautifulSoup(_response.content, 'html5lib')
            logger.logger.info(f"Connection success, content received: {content}")
            return content
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} No connection were made, failed with error: {e}")
            raise AutomationError(f"No connection were made, failed with error: {e}")

    @classmethod
    @automation_logger(logger)
    def search_document(cls, index_, query):
        html_ = cls.check_connection()
        if html_.div.text == 'Loading Kibana':
            try:
                doc = cls.kibana_client.search(index=index_, body=query)
                logger.logger.info(f"Query result is: {doc}")
                return doc
            except Exception as e:
                logger.logger.error(f"{e}")
                raise AutomationError(f"search_document failed with error: {e}")
