from datetime import datetime

AURA_DT_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


def parse_aura_dt(aura_dt_str: str):
    return datetime.strptime(aura_dt_str, AURA_DT_FORMAT)


def get_utc_now():
    return datetime.utcnow()


def format_dt_to_aura(dt: datetime):
    return dt.strftime(AURA_DT_FORMAT)
