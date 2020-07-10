import interface_functions as intFunc
# Main
print("Developed by @therealshazam\n")
print("What would you like to do?")
function = input("1. Add a Song\n2. Find a song\n")
if function == 1:
    song_path = prompt("Please enter the full path to the .mp3 file: ")
    intFunc.add_song(song_path.encode('unicode_escape'))
elif function == 2:
    duration = input("How long is your song clip?: ")
    find_song(duration)
else:
    print("Sorry something went wrong.")
