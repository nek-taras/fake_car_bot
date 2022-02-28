# Import required modules
from __future__ import annotations

from typing import List
import logging
import gspread

from config import APP_CONFIG
from dataclasses import dataclass
from cachetools.func import ttl_cache

from oauth2client.service_account import ServiceAccountCredentials


scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]


logger = logging.getLogger(__name__)


@dataclass
class Car:
    """Class for storing car info"""

    city: str
    name: str
    plate_number: str

    @property
    def search_string(self) -> str:
        return f"{self.city} {self.name} {self.plate_number}".lower()

    @staticmethod
    def build_from_record(sheet_title: str, record: dict) -> Car:
        name = record["марка авто"]
        plate_number = record["номер"]
        return Car(sheet_title, name, plate_number)

    def __repr__(self) -> str:
        return f"❗❗❗*{self.plate_number.upper()}*❗❗❗ \n 🚗{self.name} 📍{self.city} "


@ttl_cache(ttl=int(APP_CONFIG["TTL_CACHE_TIME"]))
def read_data() -> List[Car]:
    # Assign credentials ann path of style sheet
    creds = ServiceAccountCredentials.from_json_keyfile_name("gsheet_creds.json", scope)
    client = gspread.authorize(creds)
    data_file = client.open(APP_CONFIG["SPREADSHEET_NAME"])
    cars = []
    for sheet in data_file.worksheets():
        title = sheet.title
        for record in sheet.get_all_records():
            try:
                car = Car.build_from_record(title, record)
                cars.append(car)
            except:
                logger.error("WRONG RECORD", extra={"record": record})
    return cars


def search_data(query: str) -> List[Car]:
    cars = read_data()
    return [c for c in cars if query.lower() in c.search_string]
