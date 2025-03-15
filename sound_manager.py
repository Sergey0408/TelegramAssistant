import logging
from typing import Literal

logger = logging.getLogger(__name__)

SoundType = Literal["button", "correct", "wrong"]

async def play_sound(sound_type: SoundType) -> None:
    """
    Simulate playing sound effects with logging.

    Args:
        sound_type: Type of sound to play ("button", "correct", or "wrong")
    """
    sound_effects = {
        "button": "click.mp3",
        "correct": "success.mp3",
        "wrong": "error.mp3"
    }

    sound_file = sound_effects.get(sound_type)
    if sound_file:
        logger.info(f"Playing sound effect: {sound_type} ({sound_file})")
    else:
        logger.warning(f"Unknown sound type: {sound_type}")