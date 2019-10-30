"""
feature for Speech Recognition
get_librosa_melspectrogram : get Mel-Spectrogram feature using librosa library
get_librosa_mfcc : get MFCC (Mel-Frequency-Cepstral-Coefficient) feature using librosa library

FRAME_LENGTH : 21ms
STRIDE : 5.2ms ( 75% duplicated )

FRAME_LENGTH = N_FFT / SAMPLE_RATE => N_FFT = 336
STRIDE = HOP_LENGTH / SAMPLE_RATE => STRIDE = 168

+++++
remove silence Using librosa
+++++

 - Soo-Hwan -
"""

import torch
import librosa
import numpy as np

SAMPLE_RATE = 16000
N_FFT = 336
HOP_LENGTH = 84

def get_librosa_melspectrogram(filepath, n_mels = 80, rm_silence = True):
    sig, sr = librosa.core.load(filepath, SAMPLE_RATE)
    if rm_silence:
        non_silence_indices = librosa.effects.split(sig, top_db = 30)
        y = np.concatenate([sig[start:end] for start, end in non_silence_indices])
        mel_spectrogram = librosa.feature.melspectrogram(y, n_mels = n_mels, n_fft = N_FFT, hop_length = HOP_LENGTH)
        mel_spectrogram = torch.FloatTensor(mel_spectrogram).transpose(0, 1)
    else:
        mel_spectrogram = librosa.feature.melspectrogram(y, n_mels=n_mels, n_fft=N_FFT, hop_length=HOP_LENGTH)
        mel_spectrogram = torch.FloatTensor(mel_spectrogram).transpose(0, 1)
    return mel_spectrogram


def get_librosa_mfcc(filepath, n_mfcc = 40, rm_silence = True):
    sig, sr = librosa.core.load(filepath, SAMPLE_RATE)
    if rm_silence:
        non_silence_indices = librosa.effects.split(sig, top_db=30)
        y = np.concatenate([sig[start:end] for start, end in non_silence_indices])
        mfccs = librosa.feature.mfcc(y = y, sr = sr, hop_length = HOP_LENGTH, n_mfcc = n_mfcc, n_fft = N_FFT)
        mfccs = torch.FloatTensor(mfccs).transpose(0, 1)
    else:
        mfccs = librosa.feature.mfcc(y = sig, sr=sr, hop_length=HOP_LENGTH, n_mfcc=n_mfcc, n_fft=N_FFT)
        mfccs = torch.FloatTensor(mfccs).transpose(0, 1)
    return mfccs

