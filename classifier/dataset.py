"""Build the (features, labels) dataset from a manifest of recordings.

The manifest is a CSV file with one row per EEG recording and the columns
    subject, xdf_path, db_path, email, session_id, test_id, double_sent
(paths relative to the working directory, ``test_id`` 1 = congruent arrows,
2 = non-congruent arrows, ``double_sent`` 1 for sessions recorded with the early
front end that sent every trial twice, else 0).

Usage:
    from classifier.dataset import read_manifest, subject_datasets, stack_subjects
    datasets = subject_datasets(read_manifest("data/recordings.csv"))
    X, y = stack_subjects(datasets, ["S1", "S2"])
"""
import csv

import numpy as np

from classifier.features import recording_features
from classifier.labels import reaction_time_labels
from classifier.session_data import load_click_events


def read_manifest(csv_path):
    """Return the manifest rows as dicts with typed ``session_id``, ``test_id`` and ``double_sent``."""
    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        row["session_id"] = int(row["session_id"])
        row["test_id"] = int(row["test_id"])
        row["double_sent"] = bool(int(row["double_sent"]))
    return rows


def recording_dataset(recording):
    """Return the features (n_trials, 36, n_channels) and labels (n_trials,) of one recording."""
    reaction_times, click_times = load_click_events(recording)
    return recording_features(recording["xdf_path"], click_times), reaction_time_labels(reaction_times)


def subject_datasets(recordings):
    """Return {subject: (X, y)} with the trials of all recordings of each subject concatenated."""
    per_subject = {}
    for recording in recordings:
        per_subject.setdefault(recording["subject"], []).append(recording_dataset(recording))
    return {
        subject: (np.concatenate([X for X, _ in parts]), np.concatenate([y for _, y in parts]))
        for subject, parts in per_subject.items()
    }


def stack_subjects(datasets, subjects):
    """Concatenate the trials of ``subjects`` and flatten the features to (n_trials, n_features)."""
    X = np.concatenate([datasets[s][0] for s in subjects])
    y = np.concatenate([datasets[s][1] for s in subjects])
    return X.reshape(len(X), -1), y
