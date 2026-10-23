# Keyboard Typer

A small Python command-line program that types supplied text into the currently
focused application.

## Setup

```powershell
cd "C:\Users\Admin\Documents\Codex\2026-08-12\ple\outputs\keyboard_typer"
python -m pip install -r requirements.txt
```

## Use

Pass text directly:

```powershell
python type_text.py --text "Hello, world!"
```

Or type the contents of a UTF-8 text file:

```powershell
python type_text.py --file "C:\path\to\message.txt"
```

With no `--text` or `--file`, the program reads text from the terminal. Finish
input with Ctrl+Z then Enter on Windows, or Ctrl+D on macOS/Linux.

After starting the command, switch to the window where the text should appear.
Typing begins after a five-second countdown. Press Escape to cancel.

## Options

```text
--interval 0.05   Seconds between keystrokes
--jitter 0.02     Random speed variation (plus or minus seconds)
--countdown 5     Seconds before typing begins
```

Example with a slightly more natural rhythm:

```powershell
python type_text.py --text "This is a typing test." --interval 0.06 --jitter 0.025
```

Only use keyboard automation where it is permitted, and avoid entering secrets
into untrusted applications.
