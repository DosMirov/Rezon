from datetime import datetime

def get_daystamp() -> str:
    return datetime.utcnow().strftime("%Y%m%d")

def format_human_time() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M")
