from dataclasses import dataclass
from typing import Callable, Dict, List, Union
from datetime import datetime
from app.data_processor import DataProcessor  # Import DataProcessor

@dataclass
class FormatStyle:
    columns: Union[str, List[str]]
    background_color: str
    font_color: str = "black"
    bold: bool = False

class FormattingRule:
    def __init__(self, condition: Callable, format_style: FormatStyle):
        self.condition = condition
        self.format_style = format_style

    def apply(self, data: Dict[datetime, Dict[str, float]]) -> Dict[datetime, FormatStyle]:
        return {date: self.format_style if self.condition(data, date) else None
                for date in data.keys()}

class FormattingRuleFactory:
    @staticmethod
    def consecutive_change_rule(num_days: int, direction: str, columns: Union[str, List[str]], format_style: FormatStyle) -> FormattingRule:
        def condition(data, date):
            percent_changes = DataProcessor.calculate_daily_percent_changes(data)
            consecutive_changes = DataProcessor.check_consecutive_changes(percent_changes, num_days, direction)
            return consecutive_changes.get(date, False)
        
        style_dict = format_style.__dict__.copy()
        style_dict.pop('columns', None)
        style = FormatStyle(columns=columns, **style_dict)
        return FormattingRule(condition, style)

    @staticmethod
    def threshold_change_rule(percent_threshold: float, columns: Union[str, List[str]], format_style: FormatStyle) -> FormattingRule:
        def condition(data, date):
            percent_changes = DataProcessor.calculate_daily_percent_changes(data)
            threshold_changes = DataProcessor.check_threshold_change(percent_changes, percent_threshold)
            return threshold_changes.get(date, False)
        
        style_dict = format_style.__dict__.copy()
        style_dict.pop('columns', None)
        style = FormatStyle(columns=columns, **style_dict)
        return FormattingRule(condition, style)

    @staticmethod
    def cumulative_change_rule(num_days: int, percent_threshold: float, columns: Union[str, List[str]], format_style: FormatStyle) -> FormattingRule:
        def condition(data, date):
            cumulative_changes = DataProcessor.check_cumulative_change(data, num_days, percent_threshold)
            print(cumulative_changes)
            return cumulative_changes.get(date, False)
        
        style_dict = format_style.__dict__.copy()
        style_dict.pop('columns', None)
        style = FormatStyle(columns=columns, **style_dict)
        return FormattingRule(condition, style)