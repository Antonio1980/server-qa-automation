import json
import requests
from src.common.utils import logger
from config_definitions import BaseConfig
from src.common.utils.log_decorator import automation_logger


class AuthorizationZero:
    auth_zero_base_url = BaseConfig.AUTH_ZERO
    headers = {"Content-Type": "application/json"}

    @classmethod
    @automation_logger(logger)
    def get_authorization_token(cls):
        uri = cls.auth_zero_base_url + "oauth/token"
        data = {
            "username": BaseConfig.AUTH_ZERO_USER,
            "password": BaseConfig.AUTH_ZERO_PASSWORD,
            "grant_type": "password",
            "client_id": "Nv9gx8S4hKVwBgKljvbZ1gTpXo0K0LGo",
            "audience": BaseConfig.AUTH_ZERO + "api/v2/",
            "scope": "openid profile",
            "connection": "Username-Password-Authentication"
        }
        payload = json.dumps(data).encode()
        try:
            _response = requests.post(uri, data=payload, headers=cls.headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} get_authorization_token failed with error: {e}")
            raise e
