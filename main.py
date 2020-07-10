import interface_functions as intFunc
from pathlib import Path

# Main
root = Path(".")
print("Developed by @therealshazam\n")
print("What would you like to do?")
function = input("1. Add a Song\n2. Find a song\n")
if function == '1':
    song_path = root / input("Please enter the relative path to the .mp3 file: ")
    intFunc.add_song(song_path, 'database.pickle')
elif function == '2':
    print("Would you like to record a song sample or import an audio file?")
    method = input("1. Record a song sample\n2. Import an audio file\n")
    if method == '1':
        duration = input("How long is your song clip? ")
        intFunc.find_song(int(duration), None, 'database.pickle')
    elif method == '2':
        song_path = root / input("Please enter the relative path to the .mp3 file: ")
        intFunc.find_song(0, song_path, 'database.pickle')
    else:
        print("Sorry something went wrong.")

else:
    print("Sorry something went wrong.")
