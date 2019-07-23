import pytest


def run(self):
    pytest.main(['-v', 'tests', '-m', 'liveness'])


if __name__ == "__main__":
    run(None)
