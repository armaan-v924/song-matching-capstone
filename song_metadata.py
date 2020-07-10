def add_metadata(fingerprints):
    """Creates a dictionary of all user-inputted metadata

    Prompts the user to input known metadata (song title, artist, and 
    genre). Compiles the user-inputted information into a dictionary of 
    metadata and returns the dictionary.
    
    Parameters
    ----------
    fingerprints : int, number of fingerprints associated with the song

    Returns
    -------
    dict
    keys = metadata category (title, artist, genre)
    values = metadata provided via user input

    Notes
    -------
    This function prompts the user to input metadata in the following order:
    song title, artist, genre. For each category, this function asks the
    user if they would like to input a value. If an unknown response is 
    received, the function will keep prompting the user for a maximum of 5 
    times before moving on. If the user chooses to input a value, the 
    function will prompt the user to enter the value.
    
    """
    data = dict()
    data["fingerprints"] = fingerprints
    
    # ask user for song title
    query_count = 0
    check_title = input("Do you know the song title? (y/n): ")
    
    while not(check_title.lower()=="y") and not(check_title.lower()=="n"):
        if query_count < 4:
            check_title = input("That input was not recognized. Please input 'y' or 'n'. Do you know the song title? (y/n): ")
            query_count += 1
        else:
            print("Too many incorrect inputs have been given. Moving on...")
            break
    
    if check_title.lower()=="y":
        title = input("Song title: ")
        data["title"] = title
      
    # ask user for artist name
    query_count = 0
    check_artist = input("Do you know the artist's name? (y/n): ")
        
    while not(check_artist.lower()=="y") and not(check_artist.lower()=="n"):
        if query_count < 4:
            check_artist = input("That input was not recognized. Please input 'y' or 'n'. Do you know the artist's name? (y/n): ")
            query_count += 1
        else:
            print("Too many incorrect inputs have been given. Moving on...")
            break
                
    if check_artist.lower()=="y":
        artist = input("Artist: ")
        data["artist"] = artist

    # ask user for song genre 
    query_count = 0
    check_genre = input("Do you know the song's music genre? (y/n): ")
        
    while not(check_genre.lower()=="y") and not(check_genre.lower()=="n"):
        if query_count < 4:
            check_genre = input("That input was not recognized. Please input 'y' or 'n'. Do you know the song's music genre? (y/n): ")
            query_count += 1
        else:
            print("Too many incorrect inputs have been given. Moving on...")
            break

    if check_genre.lower()=="y":
        genre = input("Genre: ")
        data["genre"] = genre

    return data


def get_metadata(metadata, id, query=None):
    """Returns requested metadata for given song id

    If a query is specified, returns the value of the specific queried 
    metadata for the given song id

    If a query is not specified, returns a dictionary of all metadata 
    for the given song id

    Parameters
    ----------
    metadata: full metadata dictionary to search through
    id : int, pre-determined ID # that links song metadata to its fingerprints
    query (optional) : string, category of metadata to return (i.e. "title")

    Returns
    -------
    string : depending on the case, either the value of the queried data, 
    the string form of all metadata for the song, or an error that occured 
    when looking for the queried data

    Notes
    -------
    Do NOT use this function to find the fingerprints associated with the
    song ID. Please use get_fingerprints() instead.
    """
    if id in metadata:
        all_data = metadata[id]
        if query is not None:
            if query in all_data:
                return all_data[query]
            else:
                error_msg = "Error: "f"{query}"" was not found for this song. The available data for this song is: "f"{list(all_data.keys())}"
                return error_msg
        else:
            return str(all_data)
    else:
        return "Error: the song was not found in this database"

def get_fingerprints(metadata, id):
    """Returns number of fingerprints associated with given song id

    Parameters
    ----------
    metadata: full metadata dictionary to search through
    id : int, pre-determined ID # that links song metadata to its fingerprints

    Returns
    -------
    int : number of fingerprints associated with given song id, returns 0 if
          the song ID was not found or if the song ID has no saved fingerprints
          value

    """
    if id in metadata:
        all_data = metadata[id]
        if "fingerprints" in all_data:
            return all_data["fingerprints"]
        else:
            return 0
    else:
        return 0