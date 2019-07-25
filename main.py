import pytest


def run(self):
    pytest.main(['--capture=sys', '--capture=fd', 'tests', '-m', 'liveness'])


if __name__ == "__main__":
    run(None)
