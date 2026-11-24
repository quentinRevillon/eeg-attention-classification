"""Attention labels derived from reaction times.

Within one recording, with mu and sigma the mean and standard deviation of the
reaction times of answered trials:
    2 (fast)     reaction time < mu - sigma
    1 (typical)  mu - sigma <= reaction time <= mu + sigma
    0 (slow)     reaction time > mu + sigma, including misses and wrong answers

Usage:
    from classifier.labels import reaction_time_labels
    y = reaction_time_labels([520, 610, 1700, 480])
"""
import numpy as np

from classifier.session_data import MISS_REACTION_TIME

CLASS_NAMES = ["slow", "typical", "fast"]


def reaction_time_labels(reaction_times):
    """Return one label in {0, 1, 2} per trial (see module docstring)."""
    rt = np.asarray(reaction_times, dtype=float)
    answered = rt[rt != MISS_REACTION_TIME]
    mu, sigma = answered.mean(), answered.std()
    labels = np.ones(len(rt), dtype=int)
    labels[rt < mu - sigma] = 2
    labels[rt > mu + sigma] = 0
    return labels
