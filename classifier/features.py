"""Spectral features of the EEG between consecutive key presses.

Each trial window (from the previous key press to the current one) is
zero-padded to 2000 samples, transformed with a 2048-point real FFT per channel,
and summarised as 36 bands of 4 consecutive FFT bins, in dB.
The band layout assumes 256 Hz; the recordings are sampled at 250 Hz, so each
band is 0.49 Hz wide and the 36 bands cover 0-17.6 Hz.

Usage:
    from classifier.features import recording_features
    X = recording_features("data/eeg/S1_NonCongruent_1.xdf", click_times)
    # X.shape == (n_trials, 36, n_channels)
"""
import numpy as np
import pyxdf

PAD_SIZE = 2000  # samples per window after zero-padding
N_FFT = 2048
BINS_PER_BAND = 4
N_BANDS = 36


def read_eeg(xdf_path):
    """Return the EEG samples (n_samples, n_channels) and their timestamps (s) from an XDF file."""
    streams, _ = pyxdf.load_xdf(xdf_path)
    stream = next(s for s in streams if s["info"]["name"][0] == "EEG")
    return stream["time_series"], stream["time_stamps"]


def split_at_time_codes(eeg, timestamps, time_codes):
    """Cut the recording into consecutive windows ending at each time code (ms since recording start)."""
    elapsed_ms = (np.asarray(timestamps) - timestamps[0]) * 1000
    ends = np.maximum.accumulate(np.searchsorted(elapsed_ms, time_codes))
    return np.split(eeg, ends)[:-1]


def pad_windows(windows, size=PAD_SIZE):
    """Zero-pad every window at the end to ``size`` samples and stack them."""
    return np.stack([np.pad(w, ((0, size - len(w)), (0, 0))) for w in windows])


def band_power_db(windows):
    """Return the band power in dB, shape (n_windows, N_BANDS, n_channels).

    FFT coefficients are averaged within each band before taking the power.
    """
    spectrum = np.fft.rfft(windows, n=N_FFT, axis=1)[:, :-1, :]
    n_windows, n_bins, n_channels = spectrum.shape
    bands = spectrum.reshape(n_windows, n_bins // BINS_PER_BAND, BINS_PER_BAND, n_channels)
    bands = bands[:, :N_BANDS].mean(axis=2)
    return 10 * np.log10(np.abs(bands) ** 2)


def recording_features(xdf_path, time_codes):
    """Return the band-power features of every trial window of one recording."""
    eeg, timestamps = read_eeg(xdf_path)
    return band_power_db(pad_windows(split_at_time_codes(eeg, timestamps, time_codes)))
