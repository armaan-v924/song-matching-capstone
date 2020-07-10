import matplotlib.pyplot as plt
from microphone import record_audio
import librosa as lib
import matplotlib.mlab as mlab
import numpy as np
from pathlib import Path


def file_to_samples(song, sampling_rate=44100):
    """Converts given song file to numpy array of Fourier coefficients
    
    Parameters:
    -----------
    song: str; .mp3 file path  / accepts pathlib.Path or raw string path
    sampling_rate: int; Sampling Rate of the song, Hz
                        Defaults to 44100 Hz

    Returns: 
    --------
    spectrogram: 2D numpy array; rows - freqs, columns - times, elements - Fourier coefficients
    rate: int; sampling rate

    """

    # Collect samples & rate using librosa
    samples, rate = lib.load(song, sr=sampling_rate, mono=True)

    # Generate spectrogram using matplotlib
    spectrogram, freqs, times = mlab.specgram(
        samples,
        NFFT=4096,
        Fs=rate,
        window=mlab.window_hanning,
        noverlap=int(4096 / 2)
    )

    return spectrogram, rate

def mic_to_samples(duration: float):
    """Records audio sample & converts to numpy array of Fourier coefficients

    Parameters
    ----------
    duration: clip length; 

    Returns: 
    --------
    spectrogram: 2D numpy array; rows - freqs, columns - times, elements - Fourier coefficients
    rate: int; sampling rate
    """
    
    # Record audio using Microphone
    frames, rate = record_audio(duration)

    # Generate samples using numpy
    samples = np.hstack([np.frombuffer(i, np.int16) for i in frames])

    # Generate spectrogram using matplotlib
    spectrogram, freqs, times = mlab.specgram(
        samples,
        NFFT=4096,
        Fs=rate,
        window=mlab.window_hanning,
        noverlap=int(4096 / 2)
    )    
    return spectrogram, rate