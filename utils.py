import re
import datetime

def escape_markdown_v2(text: str) -> str:
    escape_chars = r'\\_*[]()~>#+-=|{}.!'
    pattern = re.compile(f'([{re.escape(escape_chars)}])')
    return pattern.sub(r'\\\1', text)

def get_pasaran_jawa(date: datetime.date) -> str:
    acuan = datetime.date(2025, 5, 28)
    pasaran_list = ["legí", "pahing", "pon", "wage", "kliwon"]
    delta_days = (date - acuan).days
    pasaran_index = (4 + delta_days) % 5
    return pasaran_list[pasaran_index]

def bulan_masehi_id(month_num: int) -> str:
    bulan_map = {
        1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei",
        6: "Juni", 7: "Juli", 8: "Agustus", 9: "September",
        10: "Oktober", 11: "November", 12: "Desember"
    }
    return bulan_map.get(month_num, "Unknown")

def bulan_to_number(bulan_str: str) -> int:
    bulan_map = {
        "januari":1, "februari":2, "maret":3, "april":4, "mei":5, "juni":6,
        "juli":7, "agustus":8, "september":9, "oktober":10, "november":11, "desember":12
    }
    return bulan_map.get(bulan_str.lower(), 0)
