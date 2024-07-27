import numpy as np
from typing import List, Dict, Tuple
from datetime import datetime

class DataProcessor:
    @staticmethod
    def calculate_percent_change(current_value: float, previous_value: float) -> float:
        """
        Calculate the percent change between two values.

        Args:
            current_value (float): The current value.
            previous_value (float): The previous value.

        Returns:
            float: The calculated percent change.
        """
        if previous_value == 0:
            return 0
        return ((current_value - previous_value) / previous_value) * 100

    @staticmethod
    def calculate_daily_percent_changes(data: Dict[datetime, Dict[str, float]]) -> Dict[datetime, float]:
        """
        Calculate daily percent changes for closing prices.

        Args:
            data (Dict[datetime, Dict[str, float]]): Dictionary of dates and their stock data.

        Returns:
            Dict[datetime, float]: Dictionary of dates and their percent changes.
        """
        sorted_dates = sorted(key for key in data.keys() if key != 'stock_symbol')
        percent_changes = {}
        for i in range(1, len(sorted_dates)):
            current_date = sorted_dates[i]
            previous_date = sorted_dates[i-1]
            current_close = data[current_date]['close']
            previous_close = data[previous_date]['close']
            
            percent_changes[current_date] = DataProcessor.calculate_percent_change(current_close, previous_close)
        
        return percent_changes

    @staticmethod
    def check_consecutive_changes(percent_changes: Dict[datetime, float], num_days: int, direction: str) -> Dict[datetime, bool]:
        """
        Check for consecutive positive or negative percent changes.
        
        Args:
            percent_changes (Dict[datetime, float]): Dictionary of dates and their percent changes.
            num_days (int): Number of consecutive days to check.
            direction (str): 'positive' or 'negative'.

        Returns:
            Dict[datetime, bool]: Dictionary of dates and boolean indicating if the date is part of a consecutive change streak.
        """
        sorted_dates = sorted(percent_changes.keys())
        result = {date: False for date in sorted_dates}
        
        for i in range(len(sorted_dates) - num_days + 1):
            consecutive = True
            for j in range(num_days):
                change = percent_changes[sorted_dates[i+j]]
                if (direction == 'positive' and change <= 0) or (direction == 'negative' and change >= 0):
                    consecutive = False
                    break
            
            if consecutive:
                for j in range(num_days):
                    result[sorted_dates[i+j]] = True
        
        return result

    @staticmethod
    def check_threshold_change(percent_changes: Dict[datetime, float], percent_threshold: float, direction: str) -> Dict[datetime, bool]:
        """
        Check if daily percent change is higher or lower than a threshold in the specified direction.
        
        Args:
            percent_changes (Dict[datetime, float]): Dictionary of dates and their percent changes.
            percent_threshold (float): Threshold for percent change.
            direction (str): 'positive' or 'negative'.

        Returns:
            Dict[datetime, bool]: Dictionary of dates and boolean indicating if the condition is met.
        """
        if direction == 'positive':
            return {date: change >= percent_threshold for date, change in percent_changes.items()}
        elif direction == 'negative':
            return {date: change <= -percent_threshold for date, change in percent_changes.items()}
        else:
            raise ValueError("Direction must be either 'positive' or 'negative'")

    @staticmethod
    def check_cumulative_change(data: Dict[datetime, Dict[str, float]], num_days: int, percent_threshold: float) -> Dict[datetime, bool]:
        """
        Check if there is a cumulative percent change of threshold over num_days.
        
        Args:
            data (Dict[datetime, Dict[str, float]]): Dictionary of dates and their stock data.
            num_days (int): Number of days to check for cumulative change.
            percent_threshold (float): Threshold for cumulative percent change.

        Returns:
            Dict[datetime, bool]: Dictionary of dates and boolean indicating if the condition is met.
        """
        sorted_dates = sorted(key for key in data.keys() if key != 'stock_symbol')
        result = {date: False for date in sorted_dates}
        
        for i in range(len(sorted_dates) - num_days + 1):
            start_date = sorted_dates[i]
            end_date = sorted_dates[i + num_days - 1]
            start_price = data[start_date]['close']
            end_price = data[end_date]['close']
            
            cumulative_change = DataProcessor.calculate_percent_change(end_price, start_price)
            if abs(cumulative_change) >= abs(percent_threshold):
                for j in range(num_days):
                    result[sorted_dates[i + j]] = True
        
        return result