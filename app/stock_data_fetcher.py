from datetime import datetime
import requests

class StockDataFetcher:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_daily_stock_data(self, stock_symbol: str, date_start: datetime, date_end: datetime):
        function = 'TIME_SERIES_DAILY'
        url = f'https://www.alphavantage.co/query?function={function}&symbol={stock_symbol}&outputsize=full&apikey={self.api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'Time Series (Daily)' in data:
                time_series = data['Time Series (Daily)']
                stock_data = {
                    "stock_symbol": data['Meta Data']['2. Symbol']
                }
                for date, values in time_series.items():
                    date = datetime.strptime(date, '%Y-%m-%d')
                    if date_start <= date <= date_end:
                        stock_data[date] = {
                            "open": float(values['1. open']),
                            "high": float(values['2. high']),
                            "low": float(values['3. low']),
                            "close": float(values['4. close']),
                        }
                return stock_data
            else:
                return None
        else:
            return None