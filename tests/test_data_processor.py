import pytest
from datetime import datetime
from app.data_processor import DataProcessor

@pytest.fixture
def sample_data():
    return {
        datetime(2023, 1, 1): {'close': 100, 'percent_change': 0},
        datetime(2023, 1, 2): {'close': 102, 'percent_change': 2},
        datetime(2023, 1, 3): {'close': 105, 'percent_change': 2.94},
        datetime(2023, 1, 4): {'close': 103, 'percent_change': -1.9},
        datetime(2023, 1, 5): {'close': 106, 'percent_change': 2.91},
        datetime(2023, 1, 6): {'close': 110, 'percent_change': 3.77},
        datetime(2023, 1, 7): {'close': 113, 'percent_change': 2.73}
    }

def test_calculate_percent_change():
    assert DataProcessor.calculate_percent_change(102, 100) == pytest.approx(2)
    assert DataProcessor.calculate_percent_change(98, 100) == pytest.approx(-2)
    assert DataProcessor.calculate_percent_change(100, 0) == 0

def test_calculate_daily_percent_changes(sample_data):
    percent_changes = DataProcessor.calculate_daily_percent_changes(sample_data)
    expected = {
        datetime(2023, 1, 2): 2.0,
        datetime(2023, 1, 3): 2.94,
        datetime(2023, 1, 4): -1.9,
        datetime(2023, 1, 5): 2.91,
        datetime(2023, 1, 6): 3.77,
        datetime(2023, 1, 7): 2.73
    }
    for date, change in expected.items():
        assert percent_changes[date] == pytest.approx(change, rel=1e-1)

def test_check_consecutive_changes(sample_data):
    percent_changes = {date: data['percent_change'] for date, data in sample_data.items() if date != datetime(2023, 1, 1)}
    result = DataProcessor.check_consecutive_changes(percent_changes, 2, 'positive')
    expected = {
        datetime(2023, 1, 2): False,
        datetime(2023, 1, 3): True,
        datetime(2023, 1, 4): False,
        datetime(2023, 1, 5): False,
        datetime(2023, 1, 6): True,
        datetime(2023, 1, 7): True
    }
    print(result)
    assert result == expected

def test_check_threshold_change(sample_data):
    percent_changes = {date: data['percent_change'] for date, data in sample_data.items() if date != datetime(2023, 1, 1)}
    result = DataProcessor.check_threshold_change(percent_changes, 3.0)
    expected = {
        datetime(2023, 1, 2): False,
        datetime(2023, 1, 3): False,
        datetime(2023, 1, 4): False,
        datetime(2023, 1, 5): False,
        datetime(2023, 1, 6): True,
        datetime(2023, 1, 7): False
    }
    assert result == expected

def test_check_cumulative_change(sample_data):
    result = DataProcessor.check_cumulative_change(sample_data, 3, 5)
    expected = {
        datetime(2023, 1, 1): True,
        datetime(2023, 1, 2): True,
        datetime(2023, 1, 3): True,
        datetime(2023, 1, 4): True,
        datetime(2023, 1, 5): True,
        datetime(2023, 1, 6): True,
        datetime(2023, 1, 7): True
    }
    assert result == expected