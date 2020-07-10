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
    spectrogram, rate  = file_to_samples(mp3_file_path)
    fingerprints = 9
    song_id = uuid.uuid1()
    #adds fingerprints and ids into 
    database = add_fingerprints(fingerprints, song_id, database)
    tallies = tally_fingerprints(fingerprints, database)
    song_id = find_song_id(tallies, 77)
    #add metadata = returns dictionary of values used. Then put it as a value of random song_id
    meda = add_metadata()
    metadata.add(song_id, meda)

