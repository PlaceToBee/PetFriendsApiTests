import os
import pytest

from api import PetFriends
from settings import valid_email, valid_password, not_valid_email, not_valid_password


pf = PetFriends()


@pytest.fixture(autouse=True)
def get_key():
    pf = PetFriends()
    status, key = pf.get_api_key(email=valid_email, passwd=valid_password)
    assert status == 200
    assert 'key' in key
    return key