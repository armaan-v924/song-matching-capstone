# database: keys: pairing/fingerprint value: list of song ids

def add_fingerprints(fingerprints, song_id, database):
    '''
    params:song ID, database,fingerprints
    return database
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