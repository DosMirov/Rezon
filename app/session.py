# app/session.py

from typing import Dict, Any, List, Optional

_USER_SESSIONS: Dict[int, Dict[str, Any]] = {}

def get_session(user_id: int) -> Dict[str, Any]:
    if user_id not in _USER_SESSIONS:
        _USER_SESSIONS[user_id] = {
            "user_id": user_id,
            "fragments": [],
            "state": None,        # <-- FSM state по-умолчанию
        }
    return _USER_SESSIONS[user_id]

def set_state(user_id: int, state: str) -> None:
    session = get_session(user_id)
    session["state"] = state

def get_state(user_id: int) -> Optional[str]:
    session = get_session(user_id)
    return session.get("state")

def append_fragment(user_id: int, fragment: Dict[str, Any]) -> None:
    session = get_session(user_id)
    session["fragments"].append(fragment)

def get_fragments(user_id: int) -> List[Dict[str, Any]]:
    return get_session(user_id)["fragments"]

def clear_session(user_id: int) -> None:
    if user_id in _USER_SESSIONS:
        del _USER_SESSIONS[user_id]
