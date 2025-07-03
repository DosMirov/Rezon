def get_or_create_brief(user_id: int, daystamp: str) -> str:
    """
    Создаёт brief_id в формате: BRF-{user_id}_{daystamp}
    Пример: BRF-123456789_20250703
    """
    return f"BRF-{user_id}_{daystamp}"