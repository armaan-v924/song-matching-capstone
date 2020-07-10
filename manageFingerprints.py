# database: keys: pairing/fingerprint value: list of song ids

def add_fingerprints(fingerprints, song_id, database):
    '''
    Adds a list of fingerprints into the fingerprint database
    This database has keys: fingerprints and values: list of song ids

    Returns the updated fingerprint database (database)

    Parameters
    -----------
    song_id: id of a song
    database: fingerprint database (dictionary)
    fingerprints: numpy array containing all fingerprints for a certain song

    Returns
    --------
    Updated fingerprint database including all of the new fingerprints and song_id
    '''
    for fingerprint in fingerprints:
        if fingerprint in database:
            print(fingerprint)
            database[fingerprint].append(song_id)
        else:
            database[fingerprint] = [song_id]
    return database


def tally_fingerprints(pairings, database):
    '''
    Tallies all of the songs that contain each pairing in pairings (fingerprints)

    Returns a dictionary that contains a list of songs and the number of tallies (key: song_id, value: tallies)

    Parameters
    -----------
    pairings: a numpy array containing fingerprints
    database: database of fingerprints (key: fingerprint, value: list of song_ids

    Returns
    --------
    tallies - a dictionary that is keeping track of the tallies (key: song_ids, value: number of tallies)
    '''

    tallies = {}
    for pairing in pairings:
        song_ids = database[pairing]
        for song_id in song_ids:
            if song_id in tallies:
                tallies[song_id] = tallies[song_id] + 1
            else:
                tallies[song_id] = 1
    return tallies

def add_song_fingerprints(database, fingerprints, song_id):
    '''
    Keeps track of all the fingerprints in a song
    
    Returns a database with keys: song_id and values: numpy array of fingerprints
    
    Parameters
    -----------
    database: database with keys: song_id and values: numpy array of fingerprints
    fingerprints: numpy array of fingerprints for a song
    song_id: id of a certain song
    
    Returns
    --------
    database containing the updated fingerprints and song_id
    '''
    database[song_id] = fingerprints
    return database

def find_song_id(tallies, threshold,database):
    '''
    finds the song_id with the max value of tallies and sees if that value is above the threshold

    Returns song_id if there is a match, otherwise returns "No match found"

    Parameters
    -----------
    tallies: dictionary with keys: song_id and values: number of tallies
    threshold: a percentage to see if there are enough tallies to consider a match
    database: database with key: song_id and value: numpy array of fingerprints

    Returns
    --------
    returns song_id if there is a match or "No match found"
    '''

    song_id = max(tallies, key=tallies.get)
    return song_id if tallies[song_id] / len(database[song_id]["fingerprints"]) >= threshold else "No match found"
