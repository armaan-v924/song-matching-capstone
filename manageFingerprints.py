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
    Updated fingerprint database including all of the fingerprints and song_id
    '''
    
    for fingerprint in fingerprints:
        if fingerprint in database:
            database[fingerprint] = database[fingerprint].append(song_id)
        else:
            database[fingerprint] = [song_id]
    return database


def tally_fingerprints(pairings, database):
    '''
    params: pairings, database
    returns: tallies - dictionary key: song_id, values: tallies of each song_id
    '''


    tallies = {}
    for pairing in pairings:
        song_ids = database[pairings]
        for song_id in song_ids:
            if song_id in tallies:
                tallies[song_id] = tallies[song_id] + 1
            else:
                tallies[song_id] = 1
    return tallies

def