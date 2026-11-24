"""Load and clean the attention-test results stored by the web app.

The web app writes one row per arrow trial in the ``result`` table of its SQLite
database (reaction time in ms, time code in ms since the start of the test,
correctness). Early versions of the front end sent every trial twice and stored
the arrow onset and key press as separate time codes; ``double_sent`` handles that.

Usage:
    from classifier.session_data import load_click_events
    recording = {"db_path": "data/attention.db", "email": "s1@example.com",
                 "session_id": 1, "test_id": 2, "double_sent": True}
    reaction_times, click_times = load_click_events(recording)
"""
import sqlite3
from contextlib import closing

MISS_REACTION_TIME = 1700  # ms, stored by the web app when no key is pressed in time

QUERY = (
    "SELECT reactionTime, timeCode, isCorrect FROM result "
    "WHERE email = ? AND sessionId = ? AND testId = ? ORDER BY timeCode"
)


def read_session(db_path, email, session_id, test_id):
    """Return reaction times, time codes and correctness of one test session, ordered by time code."""
    with closing(sqlite3.connect(db_path)) as conn:
        rows = conn.execute(QUERY, (email, session_id, test_id)).fetchall()
    reaction_times, time_codes, is_correct = (list(column) for column in zip(*rows))
    return reaction_times, time_codes, is_correct


def drop_duplicates(values):
    """Keep one row out of two (rows were sent twice by early versions of the front end)."""
    return values[: len(values) // 2 * 2 : 2]


def click_time_codes(reaction_times, time_codes, is_correct):
    """Map each trial to the time code of its key press.

    ``time_codes`` alternates arrow onset and key press; a missed trial has no
    key press, so its end is set to onset + MISS_REACTION_TIME.
    Returns the reaction times, click time codes and correctness of the trials kept.
    """
    kept_times, clicks, kept_correct = [], [], []
    j = 0
    for reaction_time, correct in zip(reaction_times, is_correct):
        if j + 1 >= len(time_codes):
            break
        kept_times.append(reaction_time)
        kept_correct.append(correct)
        if reaction_time != MISS_REACTION_TIME:
            clicks.append(time_codes[j + 1])
            j += 2
        else:
            clicks.append(time_codes[j] + MISS_REACTION_TIME)
            j += 1
    return kept_times, clicks, kept_correct


def mark_errors(reaction_times, is_correct):
    """Set the reaction time of wrong answers to MISS_REACTION_TIME."""
    return [rt if correct else MISS_REACTION_TIME for rt, correct in zip(reaction_times, is_correct)]


def load_click_events(recording):
    """Return the cleaned reaction times and key-press time codes of one recording (manifest row)."""
    reaction_times, time_codes, is_correct = read_session(
        recording["db_path"], recording["email"], recording["session_id"], recording["test_id"]
    )
    if recording["double_sent"]:
        reaction_times, time_codes, is_correct = (
            drop_duplicates(v) for v in (reaction_times, time_codes, is_correct)
        )
        reaction_times, time_codes, is_correct = click_time_codes(reaction_times, time_codes, is_correct)
    return mark_errors(reaction_times, is_correct), time_codes
