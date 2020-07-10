"""Interface Database Functions
saving and loading the database

inspecting the list of songs (and perhaps artists) that exist in the database

providing the ability to switch databases (optional)

deleting a song from a database (optional)

guarding against the adding the same song to the database multiple times (optional)

Parameters
---------------
metadata = a dictionary with {song ID: [Title: song_title, Name: song_name, Genre : genre_name] }
database = a dictionary with parameter fingerprints (key): list of song IDs
matchdatabase = a dictionary with {song ID: fingerprints}
file_name = seperate file
"""
import numpy as np
import pickle 
import uuid
import matplotlib.pyplot as plt
from microphone import record_audio
import librosa as lib
import matplotlib.mlab as mlab
from pathlib import Path
import conversion as c
import find_peaks as fp
import manageFingerprints as mf
import song_metadata as sm
from scipy.ndimage.morphology import generate_binary_structure

metadata = {}
database = {}
def meta_save(metadata, database, file_name):
    """Saves both complete databases onto a specified file.

    Generates a tuple, for which the first element is the metadata database
    and the second element is the song fingerprint database. Saves the tuple
    to a file specified by file_name. 

    Parameters
    ----------
    metadata : dict, stores song ID #'s as keys and known song
               metadata as values
    database : dict, stores song fingerprints as keys and songs that
               have those fingerprints as values
    file_name : string, points to file in which the two databases will
                be saved
    """

    with open(file_name, mode ="wb") as opened_file:
        pickle.dump((metadata, database), opened_file)

def meta_load(file_name):
    """Loads both complete databases from a specified file.

    Saves the two dictionary elements of the tuple from the specified file
    as the global variables "metadata" and "database", respectively.
    Parameters
    ----------
    file_name : string, points to file from which the two databases will
                be saved
    """

    with open(file_name, mode="rb") as opened_file:
        metadata, database  = pickle.load(opened_file)

def add_song(mp3_file_path, file_path):
    """Processes and adds the song (mp3 file) into the database of songs
    
    Collects the digital audio data from the file by creating samples out 
    of the file. Then creates and addd fingerprints to a dict(database) with
    its value as a generated song_id from uuid. Prompts the user for data
    about the song and adds the song_id as the key and the song's data as a 
    dictionary onto another dict(metadata)
    
    Parameters
    ------------
    mp3_file_path : string, points to file for a song that will be processed
                    and added to the database
    file_path : file, consists of tuple(metadata, database) that will be updated 
    as songs and fingerprints are added into both dictionaries.
    """ 
    metadata, database = meta_load(file_path)
    spectrogram, rate  = c.file_to_samples(mp3_file_path)
    fingerprints = fp.create_fingerprints(spectrogram, rate, len(spectrogram))
    song_id = uuid.uuid1()
    updated_database = mf.add_fingerprints(fingerprints, song_id, database)
    database = updated_database
    meda = sm.add_metadata()
    metadata[song_id] = meda
    meta_save(metadata,database,file_name)

def find_song(duration):
    """Records audio for the specified duration and prints out the song that
    the audio most closely matches
    
    Processes recorded audio and compares the processed data to a database of
    song data. Prints out the name, artist, and genre of the song that most
    closely matches the audio recording.
    
    Parameters
    ------------
    duration : int, duration of audio recording to match to a song in the
               database

    Notes
    ------------
    Uses the Fast Fourier Transform to process the recorded audio data, which
    is then converted into a spectrogram to be used to find key fingerprints
    in the recording. These fingerprints, and the times in which they occur
    in the recording are compared to the existing database of songs and the 
    best match is displayed for the user.
    """ 

    #mic_to_samples -> fingerprint -> tally -> highest tally (find_song_id)
    spectrogram, rate = c.mic_to_samples(duration)
    fpe = generate_binary_structure(2, 1)
    threshold = np.percentile(spectrogram, 75) #75th percentile amplitude
    peaks = local_peak_locations(spectrogram, fpe, threshold)
    fingerprints = fp.create_fingerprints(peaks, rate, len(spectrogram))
    tallies = mf.tally_fingerprints(fingerprints, database)
    song_id = mf.find_song_id(tallies, 0.05 ,metadata)
    if song_id == "No match found":
        print("No match found. Please try again.")
    else:
        print("You are currently listening to \"" + metadata[song_id][0] + "\" by " + metadata[song_id][1] + ". Genre: " + metadata[song_id][2])
def print_song_database():
    """Prints out a list of songs that are already in the database

    Song data is printed out in the format "(title) by (artist). Genre: (genre)"
    """ 

    print("List of Songs")
    print("------------------")
    for key in metadata:
        print("\"" + metadata[key][0] +"\" by "  + metadata[key][1] + ". Genre: " + metadata[key][2])
    print("------------------")
