import pickle

def write_save(game_state):
    with open('data.pickle', 'wb') as f:
        pickle.dump(game_state, f)

def read_save():
    with open('data.pickle', 'wb') as f:
        game_state = pickle.load(f)
    return game_state
