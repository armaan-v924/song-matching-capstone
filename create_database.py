import pickle

a = ({},{})
with open("database.pickle", mode="wb") as opened_file:
    pickle.dump(a, opened_file)