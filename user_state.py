import time
from dataclasses import dataclass
from typing import Dict, Tuple, Optional

@dataclass
class GameState:
    level: str
    start_time: float
    correct_answers: int
    errors: int
    current_question: Optional[Tuple[int, int]]
    last_error: Optional[Tuple[int, int]]

class UserState:
    _states: Dict[int, GameState] = {}

    @classmethod
    def start_new_game(cls, user_id: int, level: str):
        """Initialize new game state for user."""
        cls._states[user_id] = GameState(
            level=level,
            start_time=time.time(),
            correct_answers=0,
            errors=0,
            current_question=None,
            last_error=None
        )

    @classmethod
    def get_user_state(cls, user_id: int) -> Optional[GameState]:
        """Get current game state for user."""
        return cls._states.get(user_id)

    @classmethod
    def clear_user_state(cls, user_id: int):
        """Clear user's game state."""
        if user_id in cls._states:
            del cls._states[user_id]