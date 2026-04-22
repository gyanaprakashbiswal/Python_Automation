import json
import csv
import pandas as pd
from pathlib import Path
from config import DATA_DIR
from modules.logger import setup_logger

logger = setup_logger(__name__)

def save_json(data: dict, filename: str = "output.json"):
    """
    Saves a dictionary to a JSON file.
    """
    filepath = DATA_DIR / filename
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logger.info(f"Successfully saved data to {filepath}")
    except Exception as e:
        logger.error(f"Failed to save JSON to {filepath}. Error: {e}")

def save_csv(data: list[dict], filename: str = "output.csv"):
    """
    Saves a list of dictionaries to a CSV file.
    """
    if not data:
        logger.warning("No data provided to save_csv. Skipping.")
        return

    filepath = DATA_DIR / filename
    try:
        # Extract headers from the first dictionary
        headers = list(data[0].keys())
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
            
        logger.info(f"Successfully saved data to {filepath}")
    except Exception as e:
        logger.error(f"Failed to save CSV to {filepath}. Error: {e}")

def save_excel(data: list[dict], filename: str = "output.xlsx"):
    """
    Saves a list of dictionaries to an Excel file using pandas.
    """
    if not data:
        logger.warning("No data provided to save_excel. Skipping.")
        return

    filepath = DATA_DIR / filename
    try:
        df = pd.DataFrame(data)
        df.to_excel(filepath, index=False)
        logger.info(f"Successfully saved data to {filepath}")
    except Exception as e:
        logger.error(f"Failed to save Excel to {filepath}. Error: {e}")
