import pandas as pd
from pandas.api.types import is_datetime64tz_dtype

class CSVExporter:
    """
    Responsible for exporting market data to CSV files
    """

    @staticmethod
    def export(data: pd.DataFrame, file_path: str) -> None:
        """Export the given DataFrame to a CSV file"""
        data.to_csv(file_path, index=True)

class ExcelExporter:
    """
    Responsible for exporting market data to Excel files
    """
    
    @staticmethod
    def export(data: pd.DataFrame, file_path: str) -> None:
        """Export the given DataFrame to an Excel file"""
        data.to_excel(file_path, index=True)