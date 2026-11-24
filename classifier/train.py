"""Train and evaluate the Random Forest attention classifier.

Random 70/30 split over the trials of the given subjects:
    python -m classifier.train --manifest data/recordings.csv --subjects S1 S2 S3 S4

Leave-one-subject-out (train on --subjects, test on --test-subject):
    python -m classifier.train --manifest data/recordings.csv --subjects S1 S2 S3 --test-subject S4
"""
import argparse

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

from classifier.dataset import read_manifest, stack_subjects, subject_datasets
from classifier.labels import CLASS_NAMES


def train_random_forest(X, y):
    """Fit a 100-tree Random Forest on (X, y)."""
    return RandomForestClassifier(n_estimators=100, random_state=42).fit(X, y)


def majority_baseline(y_train, y_test):
    """Accuracy obtained by always predicting the most frequent training class."""
    return np.mean(y_test == np.bincount(y_train).argmax())


def print_report(clf, X_test, y_test, y_train):
    """Print the confusion matrix (rows: true, columns: predicted), per-class metrics and the baseline."""
    labels = list(range(len(CLASS_NAMES)))
    y_pred = clf.predict(X_test)
    print(confusion_matrix(y_test, y_pred, labels=labels))
    print(classification_report(y_test, y_pred, labels=labels, target_names=CLASS_NAMES, zero_division=0))
    print(f"majority-class baseline accuracy: {majority_baseline(y_train, y_test):.3f}")


def split_data(datasets, args):
    """Return X_train, X_test, y_train, y_test for a random split or a held-out subject."""
    X, y = stack_subjects(datasets, args.subjects)
    if args.test_subject is None:
        return train_test_split(X, y, test_size=0.3, random_state=args.seed)
    X_test, y_test = stack_subjects(datasets, [args.test_subject])
    return X, X_test, y, y_test


def parse_args():
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--manifest", required=True, help="CSV file listing the recordings")
    parser.add_argument("--subjects", nargs="+", required=True, help="subjects used for training")
    parser.add_argument("--test-subject", help="held-out subject; random 70/30 split if omitted")
    parser.add_argument("--seed", type=int, default=0, help="seed of the random split")
    return parser.parse_args()


def main():
    """Build the dataset, train the classifier and print the test report."""
    args = parse_args()
    subjects = [*args.subjects, args.test_subject]
    recordings = [r for r in read_manifest(args.manifest) if r["subject"] in subjects]
    X_train, X_test, y_train, y_test = split_data(subject_datasets(recordings), args)
    print(f"train: {len(y_train)} trials, test: {len(y_test)} trials")
    print_report(train_random_forest(X_train, y_train), X_test, y_test, y_train)


if __name__ == "__main__":
    main()
