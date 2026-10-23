#!/usr/bin/env python3
"""Type supplied text into the currently focused window."""

from __future__ import annotations

import argparse
import random
import sys
import time
from pathlib import Path
from threading import Event

try:
    from pynput.keyboard import Controller, Key, Listener
except ImportError:
    print(
        "Missing dependency: pynput\n"
        "Install it with: python -m pip install -r requirements.txt",
        file=sys.stderr,
    )
    raise SystemExit(1)


def non_negative_float(value: str) -> float:
    number = float(value)
    if number < 0:
        raise argparse.ArgumentTypeError("must be zero or greater")
    return number


def positive_int(value: str) -> int:
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return number


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Simulate keyboard typing in the currently focused window."
    )
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--text", help="text to type")
    source.add_argument(
        "--file", type=Path, help="UTF-8 text file whose contents should be typed"
    )
    parser.add_argument(
        "--interval",
        type=non_negative_float,
        default=0.05,
        help="seconds between keystrokes (default: 0.05)",
    )
    parser.add_argument(
        "--jitter",
        type=non_negative_float,
        default=0.0,
        help="random variation added to the interval, in seconds",
    )
    parser.add_argument(
        "--countdown",
        type=positive_int,
        default=5,
        help="seconds to wait before typing (default: 5)",
    )
    return parser


def get_text(args: argparse.Namespace) -> str:
    if args.text is not None:
        return args.text
    if args.file is not None:
        try:
            return args.file.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            raise SystemExit(f"Could not read {args.file}: {exc}") from exc

    print("Paste or enter the text to type.")
    print("Finish with Ctrl+Z then Enter on Windows, or Ctrl+D on macOS/Linux:")
    return sys.stdin.read()


def type_character(keyboard: Controller, character: str) -> None:
    special_keys = {"\n": Key.enter, "\t": Key.tab}
    key = special_keys.get(character)
    if key is None:
        keyboard.type(character)
    else:
        keyboard.press(key)
        keyboard.release(key)


def main() -> int:
    args = build_parser().parse_args()
    text = get_text(args)
    if not text:
        print("No text supplied; nothing to type.", file=sys.stderr)
        return 1

    cancelled = Event()

    def on_press(key: object) -> bool | None:
        if key == Key.esc:
            cancelled.set()
            return False
        return None

    print("Switch to the target window now. Press Esc at any time to cancel.")
    listener = Listener(on_press=on_press)
    listener.start()

    try:
        for remaining in range(args.countdown, 0, -1):
            if cancelled.is_set():
                print("Cancelled.")
                return 1
            print(f"Typing starts in {remaining}...", flush=True)
            time.sleep(1)

        keyboard = Controller()
        for character in text:
            if cancelled.is_set():
                print("\nCancelled.")
                return 1
            type_character(keyboard, character)
            delay = max(0.0, args.interval + random.uniform(-args.jitter, args.jitter))
            time.sleep(delay)
    finally:
        listener.stop()

    print("\nFinished typing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
