# eeg-attention-classification — attention tests synchronised with EEG and a Random Forest attention classifier

**eeg-attention-classification** contains a Flask web app that runs attention and memory tests while a
64-channel EEG cap records the participant, and a pipeline that turns the EEG between two answers into
band-power features and classifies the trial as a slow, typical or fast reaction with a Random Forest.

<img height="400" src="figures/confusion_matrix_random_split.png" />

*Test confusion matrix of the pooled random split (rows: predicted, columns: true; 0 slow, 1 typical, 2 fast).*

## Overview

- **Problem**: decode the attention level of a person from EEG, as a first step towards a wearable neurofeedback device.
- **Approach**: the web app logs every arrow trial (reaction time, correctness, time code in ms); the time codes cut
  the EEG recording into one window per trial; reaction times relative to the session mean give the labels.
- **Context**: Télécom Paris first-year team project (PROJ104 "AIoT"), February to June 2024, five students supervised
  by Van-Tam Nguyen, with the PhD students of the lab. Recordings were made on the team members.

## Results

Random Forest (100 trees) on 36 bands x 64 channels, from `notebooks/01_random_forest_eeg.ipynb`.
The baseline always predicts the most frequent class ("typical").

| Evaluation | Test trials | Accuracy | Majority-class baseline |
|---|---|---|---|
| Random 70/30 split, 4 subjects pooled (3,222 trials) | 967 | 0.689 | 0.698 |
| Random 70/30 split, 1 subject (706 trials) | 212 | 0.599 | 0.665 |
| Leave-one-subject-out (train on 3, test on the 4th) | 725 | 0.152 | 0.745 |

The classifier does not beat the majority-class baseline. Training accuracy is 1.0 in every setting, and on the
held-out subject the model predicts "slow" for every trial. Per-class recall on the pooled split is 0.176 (slow),
0.924 (typical) and 0.095 (fast). With four subjects and one feature per channel and frequency band, the
classifier overfits the training subjects.

## Installation

```bash
python -m venv .venv && source .venv/bin/activate   # Python 3.12
pip install -r requirements.txt
```

## Quick start

Run the tests in a browser (results go to `webapp/instance/attention.db`):

```bash
cd webapp
python app.py
```

Train and evaluate the classifier on your own recordings, listed in `data/recordings.csv` (see [Data](#data)):

```bash
python -m classifier.train --manifest data/recordings.csv --subjects S1 S2 S3 S4
python -m classifier.train --manifest data/recordings.csv --subjects S1 S2 S3 --test-subject S4
```

The first command uses a random 70/30 split, the second holds out one subject. Both print the confusion matrix,
per-class precision and recall, and the majority-class baseline. On the original recordings the second command
gives the same confusion matrix as the notebook.

Plot the reaction times of one session:

```bash
python -m classifier.plot_reaction_times --db webapp/instance/attention.db --email s1@example.com --session 1 --test 2
```

## Repository structure

- `webapp/app.py`: Flask routes (sign-up, tests, result storage, leaderboard); `webapp/models.py`: SQLite tables.
- `webapp/templates/`, `webapp/static/`: arrow tests (`script.js`), ball game (`sketch.js`), image and word memory games (`prisha.js`).
- `webapp/Manon/`: React build of the number-sequence memory game; `webapp/images/`: images of the image-recall game.
- `classifier/session_data.py`: reads and cleans the trials of one session from the database.
- `classifier/features.py`: EEG windows between answers and band power; `classifier/labels.py`: reaction-time labels.
- `classifier/dataset.py`: builds (X, y) per subject from the manifest; `classifier/train.py`: training and evaluation.
- `notebooks/01_random_forest_eeg.ipynb`: original experiments with their outputs.
- `docs/`: test protocols, protocol meeting notes and the team progress log (in French).

## Method

- **Tests**: a central arrow appears above or below the screen centre and the participant presses the matching arrow
  key. The flanking arrows point the same way (congruent test, `testId` 1, preceded by an alert sound) or the opposite
  way (non-congruent test, `testId` 2). A trial without an answer within 1700 ms is a miss. Each of the four subjects
  in the results has 1 congruent and 3 non-congruent recordings.
- **Synchronisation**: the time codes of the web app (ms since the start of the test) are compared with the EEG
  timestamps (ms since the first sample), assuming the recording and the test start together.
- **Features**: the window from the previous key press to the current one is zero-padded to 2000 samples,
  transformed with a 2048-point real FFT per channel and averaged into 36 bands of 4 bins, in dB. The band layout
  assumes 256 Hz while the cap samples at 250 Hz, so the bands are 0.49 Hz wide and cover 0-17.6 Hz.
- **Labels**: per recording, with mu and sigma the mean and standard deviation of answered reaction times:
  fast if below mu - sigma, slow if above mu + sigma (misses and wrong answers included), typical otherwise.
- **Classifier**: scikit-learn `RandomForestClassifier(n_estimators=100, random_state=42)` on the flattened
  36 x 64 features.

## Data

The EEG recordings (XDF, 64 channels, 250 Hz) and the web app databases contain personal data of the participants
and are not included. To run the classifier, put your files in `data/` (gitignored) and list one recording per row:

```csv
subject,xdf_path,db_path,email,session_id,test_id,double_sent
S1,data/eeg/S1_NonCongruent_1.xdf,data/attention.db,s1@example.com,1,2,1
```

`double_sent` is 1 for sessions recorded with the early front end that sent every trial twice, 0 otherwise.
In the original data, one congruent recording has 49 of its 51 trials marked as misses or wrong answers.

## Team

Students: Quentin Revillon, Charles Kayssieh, Félicité Yvert (attention tests), Prisha Chandiramani,
Manon Strasser (memory tests).

- Quentin Revillon: Flask back end and database, EEG/web-app synchronisation, signal processing, Random Forest classifier.
- Charles Kayssieh: arrow tests and leaderboard, reaction-time analysis and labelling.
- Prisha Chandiramani: image-recall and word-sequence memory games, protocol for the ethics committee.
- Manon Strasser: number-sequence memory game.

Supervisor: Van-Tam Nguyen (Télécom Paris). PhD students: Nasim Bagheri Shouraki, Rémi Nahon, Aël Quélennec,
Yinghao Wang, Anh Dung Nguyen.
