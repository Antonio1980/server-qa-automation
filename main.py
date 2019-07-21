import pytest


def run(self):
    pytest.main(['-v', 'tests', '-m', 'liveness'])
