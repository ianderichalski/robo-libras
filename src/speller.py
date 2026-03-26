import time

from typing import Callable
from src.config import SPELL_START_DELAY, SPELL_LETTER_DELAY, SPELL_SPACE_DELAY
from src.poses import get_pose, normalize_text

_FLEX = {0: "ab", 0.33: "po", 0.66: "me", 1: "fe"}

def spell(
    text: str,
    apply_fn: Callable[[dict], None],
    rest_fn: Callable[[], None],
    letter_delay: float = SPELL_LETTER_DELAY,
    space_delay: float = SPELL_SPACE_DELAY,
    should_stop: Callable[[], bool] | None = None,
    on_char: Callable[[str, dict | None], None] | None = None,
) -> None:
    """Soletra um texto na mão robótica, chamando apply_fn para cada pose."""
    normalized = normalize_text(text)
    rest_fn()
    time.sleep(SPELL_START_DELAY)

    for char in normalized:
        if should_stop and should_stop():
            break

        if char == " ":
            if on_char:
                on_char(" ", None)
            rest_fn()
            time.sleep(space_delay)
            continue

        pose = get_pose(char)
        if pose is None:
            continue

        if on_char:
            on_char(char, pose)

        apply_fn(pose)
        time.sleep(letter_delay)

    rest_fn()

def format_pose_line(char: str, pose: dict) -> str:
    parts = "  ".join(f"{k[:3].upper()}:{_FLEX.get(v, str(v))}" for k, v in pose.items())
    return f"   {char.upper()}  →  {parts}"