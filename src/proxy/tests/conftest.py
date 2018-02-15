import pytest
from falcon import testing

from proxy.app import api


@pytest.fixture()
def client():
    return testing.TestClient(api)
