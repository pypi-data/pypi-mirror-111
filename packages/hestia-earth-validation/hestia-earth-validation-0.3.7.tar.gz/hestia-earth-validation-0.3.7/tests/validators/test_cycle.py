import json

from tests.utils import fixtures_path
from hestia_earth.validation.validators.cycle import (
    validate_cycle,
    validate_cycle_dates,
    validate_cycleDuration,
    validate_functionalUnitMeasure,
    validate_economicValueShare,
    validate_sum_aboveGroundCropResidue,
    validate_crop_residue_completeness
)


def test_validate_valid():
    with open(f"{fixtures_path}/cycle/valid.json") as f:
        node = json.load(f)
    assert validate_cycle(node) == [True] * 37


def test_validate_cycle_dates_valid():
    cycle = {
        'startDate': '2020-01-01',
        'endDate': '2020-01-02'
    }
    assert validate_cycle_dates(cycle) is True
    cycle = {
        'startDate': '2020-01',
        'endDate': '2020-01'
    }
    assert validate_cycle_dates(cycle) is True
    cycle = {
        'startDate': '2020',
        'endDate': '2020'
    }
    assert validate_cycle_dates(cycle) is True


def test_validate_cycle_dates_invalid():
    cycle = {
        'startDate': '2020-01-02',
        'endDate': '2020-01-01'
    }
    assert validate_cycle_dates(cycle) == {
        'level': 'error',
        'dataPath': '.endDate',
        'message': 'must be greater than startDate'
    }
    cycle = {
        'startDate': '2020-01-01',
        'endDate': '2020-01-01'
    }
    assert validate_cycle_dates(cycle) == {
        'level': 'error',
        'dataPath': '.endDate',
        'message': 'must be greater than startDate'
    }


def test_validate_cycleDuration_valid():
    cycle = {
        'startDate': '2020-01-02',
        'endDate': '2021-01-01',
        'cycleDuration': 365
    }
    assert validate_cycleDuration(cycle) is True


def test_validate_cycleDuration_invalid():
    cycle = {
        'startDate': '2020-01-02',
        'endDate': '2021-01-01',
        'cycleDuration': 200
    }
    assert validate_cycleDuration(cycle) == {
        'level': 'error',
        'dataPath': '.cycleDuration',
        'message': 'must equal to endDate - startDate in days (~365.0)'
    }


def test_validate_functionalUnitMeasure_valid():
    cycle = {
        'functionalUnitMeasure': '1 ha'
    }
    site = {
        'siteType': 'cropland'
    }
    assert validate_functionalUnitMeasure(cycle, site) is True


def test_validate_functionalUnitMeasure_invalid():
    cycle = {
        'functionalUnitMeasure': 'relative'
    }
    site = {
        'siteType': 'cropland'
    }
    assert validate_functionalUnitMeasure(cycle, site) == {
        'level': 'error',
        'dataPath': '.functionalUnitMeasure',
        'message': 'must equal to 1 ha'
    }


def test_validate_economicValueShare_valid():
    products = [{
        'economicValueShare': 10
    }, {
        'economicValueShare': 80
    }]
    assert validate_economicValueShare(products) is True


def test_validate_economicValueShare_invalid():
    products = [{
        'economicValueShare': 10
    }, {
        'economicValueShare': 90
    }, {
        'economicValueShare': 10
    }]
    assert validate_economicValueShare(products) == {
        'level': 'error',
        'dataPath': '.products',
        'message': 'economicValueShare should sum to 100 or less across all products',
        'params': {
            'sum': 110
        }
    }


def test_validate_sum_aboveGroundCropResidue_valid():
    with open(f"{fixtures_path}/cycle/aboveGroundCropResidue/valid.json") as f:
        data = json.load(f)
    assert validate_sum_aboveGroundCropResidue(data.get('products')) is True


def test_validate_sum_aboveGroundCropResidue_invalid():
    with open(f"{fixtures_path}/cycle/aboveGroundCropResidue/invalid.json") as f:
        data = json.load(f)
    assert validate_sum_aboveGroundCropResidue(data.get('products')) == {
        'level': 'error',
        'dataPath': '.products[0].value',
        'message': 'must be more than or equal to '
        '(aboveGroundCropResidueBurnt + aboveGroundCropResidueLeftOnField)'
    }


def test_validate_crop_residue_completeness_valid():
    with open(f"{fixtures_path}/cycle/dataCompleteness-cropResidue/valid.json") as f:
        data = json.load(f)
    assert validate_crop_residue_completeness(data, data.get('site')) is True


def test_validate_crop_residue_completeness_invalid():
    with open(f"{fixtures_path}/cycle/dataCompleteness-cropResidue/invalid.json") as f:
        data = json.load(f)
    assert validate_crop_residue_completeness(data, data.get('site')) == {
        'level': 'error',
        'dataPath': '.products',
        'message': 'the sum of above ground crop residue and below ground crop residue must be greater than zero'
    }
