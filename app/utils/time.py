from datetime import datetime

def get_daystamp() -> str:
    """
    Возвращает текущую дату в формате YYYYMMDD
    Например: "20250703"
    """
    return datetime.utcnow().strftime("%Y%m%d")

def get_timestamp() -> str:
    """
    Возвращает текущий UTC timestamp в формате ISO
    Например: "2025-07-03T14:22:01Z"
    """
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

def format_human_time() -> str:
    """
    Возвращает человекочитаемое время для сообщений в канал
    Например: "2025-07-03 14:22"
    """
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M")