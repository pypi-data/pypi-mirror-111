import json

from tests.utils import fixtures_path
from hestia_earth.validation.validators.organisation import validate_organisation, validate_organisation_dates


def test_validate_valid():
    with open(f"{fixtures_path}/organisation/valid.json") as f:
        node = json.load(f)
    assert validate_organisation(node) == [True] * 8


def test_validate_organisation_dates_valid():
    organisation = {
        'startDate': '2020-01-01',
        'endDate': '2020-01-02'
    }
    assert validate_organisation_dates(organisation) is True


def test_validate_organisation_dates_invalid():
    organisation = {
        'startDate': '2020-01-02',
        'endDate': '2020-01-01'
    }
    assert validate_organisation_dates(organisation) == {
        'level': 'error',
        'dataPath': '.endDate',
        'message': 'must be greater than startDate'
    }
