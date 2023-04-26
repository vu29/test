"""DateTime Utils"""

from datetime import datetime as dt


def to_iso_format(datetime):
    return datetime.isoformat().replace("+00:00", "Z")


def parse_iso_format(datetime: str):
    return dt.fromisoformat(datetime.replace("Z", "+00:00"))
