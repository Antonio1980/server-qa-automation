import os
import pytest


if 'ENV' in os.environ.keys():
    env = os.environ.get('ENV')
    if isinstance(env, str):
        if env.lower() == "prod":
            pytest.skip("Those tests shouldn't run on production!", allow_module_level=True)
