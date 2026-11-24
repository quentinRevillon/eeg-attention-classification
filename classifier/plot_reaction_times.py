"""Plot the reaction times of one attention-test session.

    python -m classifier.plot_reaction_times --db data/attention.db --email s1@example.com --session 1 --test 2

Shows the reaction-time histogram, then the reaction time and error rate over
the session with a moving average over --window trials.
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np

from classifier.session_data import read_session


def moving_average(values, window):
    """Return the moving average of ``values`` over ``window`` points (valid part only)."""
    return np.convolve(values, np.ones(window) / window, mode="valid")


def plot_histogram(reaction_times):
    """Plot the reaction-time distribution."""
    plt.figure(figsize=(10, 6))
    plt.hist(reaction_times, bins=30)
    plt.xlabel("Reaction time (ms)")
    plt.ylabel("Trials")
    plt.grid(True)


def plot_trend(reaction_times, time_codes, is_correct, window):
    """Plot reaction time and error rate against the time code, with their moving averages."""
    codes, index = np.unique(time_codes, return_inverse=True)
    counts = np.bincount(index)
    mean_rt = np.bincount(index, weights=reaction_times) / counts
    error_rate = np.bincount(index, weights=1 - np.asarray(is_correct)) / counts
    smooth_codes = codes[: len(codes) - window + 1]
    fig, ax_rt = plt.subplots(figsize=(10, 6))
    ax_rt.plot(codes, mean_rt, "o", color="tab:blue", label="reaction time")
    ax_rt.plot(smooth_codes, moving_average(mean_rt, window), color="tab:blue", label="moving average")
    ax_rt.set_xlabel("Time code (ms)")
    ax_rt.set_ylabel("Reaction time (ms)", color="tab:blue")
    ax_err = ax_rt.twinx()
    ax_err.plot(smooth_codes, moving_average(error_rate, window), color="tab:red", label="error rate")
    ax_err.set_ylim(-0.1, 0.9)
    ax_err.set_ylabel("Error rate", color="tab:red")
    fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))
    fig.tight_layout()


def parse_args():
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--db", required=True, help="SQLite database written by the web app")
    parser.add_argument("--email", required=True, help="participant account")
    parser.add_argument("--session", type=int, required=True, help="session id")
    parser.add_argument("--test", type=int, required=True, help="1 = congruent, 2 = non-congruent")
    parser.add_argument("--window", type=int, default=10, help="moving-average window, in trials")
    return parser.parse_args()


def main():
    """Load the session and show both plots."""
    args = parse_args()
    reaction_times, time_codes, is_correct = read_session(args.db, args.email, args.session, args.test)
    plot_histogram(reaction_times)
    plot_trend(reaction_times, time_codes, is_correct, args.window)
    plt.show()


if __name__ == "__main__":
    main()
