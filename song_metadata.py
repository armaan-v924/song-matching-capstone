def add_metadata(title=None, artist=None, genre=None):
    """Creates a dictionary of all provided metadata

    Returns a dictionary of metadata provided for each given song ID. 
    This method will not include a category if its value is not specified.

    Parameters
    ----------
    title (optional) : string, song title
    artist (optional) : string, song artist
    genre (optional) : string, song genre

    Returns
    -------
    dict, key = song id, value = provided metadata

    """
    data = dict()
    if title is not None:
        data["title"] = title
    if artist is not None:
        data["artist"] = artist
    if genre is not None:
        data["genre"] = genre
    
    return data


def get_metadata(metadata, id, query=None):
    """Returns requested metadata for given song id

    If a query is specified, returns the value of the specific queried 
    metadata for the given song id

    If a query is not specific, returns a dictionary of all metadata 
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

    """
    if id in metadata:
        all_data = metadata[id]
        if query is not None:
            if query in all_data:
                return all_data[query]
            else:
                error_msg = "Error: "f"{query}"" was not found for this song. The available data for this song are: "f"{list(all_data.keys())}"
                return error_msg
        else:
            return str(all_data)
    else:
        return "Error: the song was not found in this database"