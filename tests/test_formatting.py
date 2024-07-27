import pytest
from datetime import datetime, timedelta
from app.formatting import FormatStyle, FormattingRule, FormattingRuleFactory

# Updated test data
test_data = {
    datetime(2023, 1, 1): {"close": 100, "percent_change": 0},
    datetime(2023, 1, 2): {"close": 102, "percent_change": 2},
    datetime(2023, 1, 3): {"close": 105, "percent_change": 2.94},
    datetime(2023, 1, 4): {"close": 103, "percent_change": -1.90},
    datetime(2023, 1, 5): {"close": 106, "percent_change": 2.91},
    datetime(2023, 1, 6): {"close": 110, "percent_change": 3.77},
    datetime(2023, 1, 7): {"close": 113, "percent_change": 2.73},
}

@pytest.fixture
def format_style():
    return FormatStyle(columns=["close", "percent_change"], background_color="yellow", font_color="red", bold=True)

def test_formatting_rule():
    style = FormatStyle(columns="percent_change", background_color="green")
    rule = FormattingRule(lambda data, date: data[date]["percent_change"] > 0, style)
    
    result = rule.apply(test_data)
    
    assert result[datetime(2023, 1, 1)] is None
    assert result[datetime(2023, 1, 2)] == style
    assert result[datetime(2023, 1, 3)] == style
    assert result[datetime(2023, 1, 4)] is None
    assert result[datetime(2023, 1, 5)] == style

def test_consecutive_change_rule():
    factory = FormattingRuleFactory()
    style = FormatStyle(columns="percent_change", background_color="blue")
    rule = factory.consecutive_change_rule(3, "positive", "percent_change", style)
    
    result = rule.apply(test_data)
   
    assert result[datetime(2023, 1, 1)] is None
    assert result[datetime(2023, 1, 2)] is None
    assert result[datetime(2023, 1, 3)] is None
    assert result[datetime(2023, 1, 4)] is None
    assert result[datetime(2023, 1, 5)] == style
    assert result[datetime(2023, 1, 6)] == style
    assert result[datetime(2023, 1, 7)] == style

def test_threshold_change_rule():
    factory = FormattingRuleFactory()
    style = FormatStyle(columns="percent_change", background_color="red")
    rule = factory.threshold_change_rule(2.5, "percent_change", style)
    
    result = rule.apply(test_data)
    
    assert result[datetime(2023, 1, 1)] is None
    assert result[datetime(2023, 1, 2)] is None
    assert result[datetime(2023, 1, 3)] == style
    assert result[datetime(2023, 1, 4)] is None
    assert result[datetime(2023, 1, 5)] == style
    assert result[datetime(2023, 1, 6)] == style
    assert result[datetime(2023, 1, 7)] == style

def test_cumulative_change_rule():
    factory = FormattingRuleFactory()
    style = FormatStyle(columns="close", background_color="purple")
    rule = factory.cumulative_change_rule(3, 5, "close", style)
    
    result = rule.apply(test_data)
    
    assert result[datetime(2023, 1, 1)] == style
    assert result[datetime(2023, 1, 2)] == style
    assert result[datetime(2023, 1, 3)] == style
    assert result[datetime(2023, 1, 4)] == style
    assert result[datetime(2023, 1, 5)] == style
    assert result[datetime(2023, 1, 6)] == style
    assert result[datetime(2023, 1, 7)] == style 

def test_multiple_columns_format_style():
    style = FormatStyle(columns=["close", "percent_change"], background_color="orange")
    rule = FormattingRule(lambda data, date: data[date]["close"] > 104, style)
    
    result = rule.apply(test_data)
    
    assert result[datetime(2023, 1, 1)] is None
    assert result[datetime(2023, 1, 2)] is None
    assert result[datetime(2023, 1, 3)] == style
    assert result[datetime(2023, 1, 4)] is None
    assert result[datetime(2023, 1, 5)] == style
    assert result[datetime(2023, 1, 6)] == style
    assert result[datetime(2023, 1, 7)] == style

def test_format_style_properties(format_style):
    assert format_style.columns == ["close", "percent_change"]
    assert format_style.background_color == "yellow"
    assert format_style.font_color == "red"
    assert format_style.bold == True

def test_formatting_rule_with_missing_data():
    style = FormatStyle(columns="percent_change", background_color="gray")
    rule = FormattingRule(lambda data, date: data[date].get("percent_change", 0) > 1, style)
    
    incomplete_data = test_data.copy()
    incomplete_data[datetime(2023, 1, 8)] = {"close": 115}  # Missing percent_change
    
    result = rule.apply(incomplete_data)
    
    assert result[datetime(2023, 1, 2)] == style
    assert result[datetime(2023, 1, 8)] is None

if __name__ == "__main__":
    pytest.main()