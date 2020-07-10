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

metadata = {}
database = {}

def meta_save(metadata, database, file_name):
    #saves the metadata onto a seperate file
    with open(file_name, mode ="wb") as opened_file:
        pickle.dump((metadata, database), opened_file)
def meta_load(file_name):
    #loads the tuple into two seperate variables based on metadata and database.
    with open(file_name, mode="rb") as opened_file:
        metadata, database  = pickle.load(opened_file)
def add_song(mp3_file_path):
    # put mp3 into tuple, unpack it, then generates song_id .
    spectrogram, rate  = c.file_to_samples(mp3_file_path)
    fingerprints = fp.create_fingerprints(spectrogram, rate, len(spectrogram))
    song_id = uuid.uuid1()
    #adds fingerprints and ids into 
    database = mf.add_fingerprints(fingerprints, song_id, database)
    #add metadata = returns dictionary of values used. Then put it as a value of random song_id
    meda = sm.add_metadata()
    metadata.add(song_id, meda)
def find_song(recording):
    #mic_to_samples -> fingerprint -> tally -> highest tally (find_song_id)
    spectrogram, rate = c.mic_to_samples(recording)
    fingerprints = fp.create_fingerprints(peak_locations, rate, len(spectrogram)):
    tallies = mf.tally_fingerprints(fingerprints, database)
    song_id = mf.find_song_id(tallies, 0.05 ,metadata)
    print("You are currently listening to \"" + metadata[song_id][0] + "\" by " + metadata[song_id][1] + ". Genre: " + metadata[song_id][2]
def print_song_database():
    print("List of Songs")
    print("------------------")
    for key in metadata:
        print("\"" + metadata[key][0] +"\" by  + metadata[key][1] + . Genre: " + metadata[key][2])
    print("------------------")
