import pytest
from datetime import datetime
from app.data_processor import DataProcessor

@pytest.fixture
def sample_data():
    return {
        datetime(2023, 1, 1): {'close': 100},
        datetime(2023, 1, 2): {'close': 102},
        datetime(2023, 1, 3): {'close': 101},
        datetime(2023, 1, 4): {'close': 103},
        datetime(2023, 1, 5): {'close': 105},
    }

def test_calculate_percent_change():
    assert DataProcessor.calculate_percent_change(110, 100) == pytest.approx(10)
    assert DataProcessor.calculate_percent_change(90, 100) == pytest.approx(-10)
    assert DataProcessor.calculate_percent_change(100, 0) == 0

def test_calculate_daily_percent_changes(sample_data):
    percent_changes = DataProcessor.calculate_daily_percent_changes(sample_data)
    expected = {
        datetime(2023, 1, 2): 2.0,
        datetime(2023, 1, 3): -0.9803921568627451,
        datetime(2023, 1, 4): 1.9801980198019802,
        datetime(2023, 1, 5): 1.9417475728155338
    }
    for date, change in expected.items():
        assert percent_changes[date] == pytest.approx(change)

def test_check_consecutive_changes():
    percent_changes = {
        datetime(2023, 1, 1): 1.0,
        datetime(2023, 1, 2): 2.0,
        datetime(2023, 1, 3): -1.0,
        datetime(2023, 1, 4): 1.5,
        datetime(2023, 1, 5): 0.5,
    }
    result = DataProcessor.check_consecutive_changes(percent_changes, 2, 'positive')
    expected = {
        datetime(2023, 1, 2): True,
        datetime(2023, 1, 3): False,
        datetime(2023, 1, 4): False,
        datetime(2023, 1, 5): True,
    }
    assert result == expected

def test_check_threshold_change():
    percent_changes = {
        datetime(2023, 1, 1): 1.0,
        datetime(2023, 1, 2): 2.5,
        datetime(2023, 1, 3): -1.5,
        datetime(2023, 1, 4): 3.0,
    }
    result = DataProcessor.check_threshold_change(percent_changes, 2.0)
    expected = {
        datetime(2023, 1, 1): False,
        datetime(2023, 1, 2): True,
        datetime(2023, 1, 3): False,
        datetime(2023, 1, 4): True,
    }
    assert result == expected

def test_check_cumulative_change(sample_data):
    result = DataProcessor.check_cumulative_change(sample_data, 3, 3.0)
    expected = {
        datetime(2023, 1, 1): False,
        datetime(2023, 1, 2): False,
        datetime(2023, 1, 3): True,
        datetime(2023, 1, 4): True,
        datetime(2023, 1, 5): True,
    }
    assert result == expected