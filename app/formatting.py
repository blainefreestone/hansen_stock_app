from dataclasses import dataclass
from typing import Callable, Dict, List, Union
from datetime import datetime

@dataclass
class FormatStyle:
    columns: Union[str, List[str]]  # Can be a single column name or a list of column names
    background_color: str           # Background color for the cell
    font_color: str = "black"       # Font color for the cell
    bold: bool = False              # Bold text

class FormattingRule:
    def __init__(self, condition: Callable, format_style: FormatStyle):
        self.condition = condition
        self.format_style = format_style

    def apply(self, data: Dict[datetime, Dict[str, float]]) -> Dict[datetime, FormatStyle]:
        """
        Apply the formatting rule to the data.

        Args:
            data (Dict[datetime, Dict[str, float]]): Dictionary of sorted_dates and their stock data.

        Returns:
            Dict[datetime, FormatStyle]: Dictionary of sorted_dates and their corresponding FormatStyle.
        """
        return {date: self.format_style if self.condition(data, date) else None
                for date in data.keys()}

class FormattingRuleFactory:
    @staticmethod
    def consecutive_change_rule(num_days: int, direction: str, columns: Union[str, List[str]], format_style: FormatStyle) -> FormattingRule:
        def condition(data, date):
            sorted_dates = sorted(key for key in data.keys() if key != 'stock_symbol')
            if date not in sorted_dates:
                return False
            index = sorted_dates.index(date)
            if index < num_days - 1:
                return False
            changes = [data[sorted_dates[i]].get('percent_change', 0) for i in range(index - num_days + 1, index + 1)]
            return all(change > 0 if direction == 'positive' else change < 0 for change in changes)
        
        style_dict = format_style.__dict__.copy()
        style_dict.pop('columns', None)
        style = FormatStyle(columns=columns, **style_dict)
        return FormattingRule(condition, style)

    @staticmethod
    def threshold_change_rule(percent_threshold: float, columns: Union[str, List[str]], format_style: FormatStyle) -> FormattingRule:
        def condition(data, date):
            return abs(data[date]['percent_change']) >= abs(percent_threshold) if 'percent_change' in data[date] else False
        
        style_dict = format_style.__dict__.copy()
        style_dict.pop('columns', None)
        style = FormatStyle(columns=columns, **style_dict)
        return FormattingRule(condition, style)

    @staticmethod
    def cumulative_change_rule(num_days: int, percent_threshold: float, columns: Union[str, List[str]], format_style: FormatStyle) -> FormattingRule:
        def condition(data, date):
            sorted_dates = sorted(key for key in data.keys() if key != 'stock_symbol')
            if date not in sorted_dates:
                return False
            index = sorted_dates.index(date)
            if index < num_days - 1:
                return False
            start_price = data[sorted_dates[index - num_days + 1]]['close']
            end_price = data[date]['close']
            cumulative_change = (end_price - start_price) / start_price * 100
            return abs(cumulative_change) >= abs(percent_threshold)
        
        style_dict = format_style.__dict__.copy()
        style_dict.pop('columns', None)
        style = FormatStyle(columns=columns, **style_dict)
        return FormattingRule(condition, style)
