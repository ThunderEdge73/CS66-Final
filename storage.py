import pickle

def save_game(hero, filename="savegame.dat"):
    try:
        with open(filename, "wb") as f:
            # We save the Hero object. 
            # Note: We aren't saving the world state here to keep it simple,
            # but usually you'd save a dict {"hero": hero, "world": ...}
            # Feel free to make that update! It's a good exercise.
            pickle.dump(hero, f)
        print("Game saved successfully.")
    except Exception as e:
        print(f"Save failed: {e}")

def load_game(filename="savegame.dat"):
    try:
        with open(filename, "rb") as f:
            hero = pickle.load(f)
        print("Game loaded successfully.")
        return hero
    except FileNotFoundError:
        print("No save file found.")
        return None