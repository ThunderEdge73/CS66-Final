from utils import load_game_data
from math import sqrt
class Location:
    def __init__(self, name, description, enemies, x, y):
        self.name = name
        self.description = description
        self.x = x
        self.y = y
        self.enemies = enemies
        # Adjacency List (see add_connection)
        self.connections = {} 

    def add_connection(self, direction, target_location, distance):
        self.connections[direction] = {
            "target": target_location, 
            "distance": distance
        }

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name

class World:
    def __init__(self):
        self.locations = {} 
        # Grid boundaries in case you want to use coordinates to draw the World map
        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0

    def add_node(self, location):
        self.locations[location.name] = location
        # Update map boundaries
        self.min_x = min(self.min_x, location.x)
        self.max_x = max(self.max_x, location.x)
        self.min_y = min(self.min_y, location.y)
        self.max_y = max(self.max_y, location.y)

    def add_edge(self, source_name, direction, target_name, distance=1):
        if source_name in self.locations and target_name in self.locations:
            source = self.locations[source_name]
            target = self.locations[target_name]
            source.add_connection(direction, target, distance)
            
            # For the map to look right, ensure x/y align with direction
            # (We won't enforce it programmatically here, but whatever you do in build_world must match)

    def __str__(self):
        final_string = ""
        max_w = 0
        for name, loc in self.locations.items():
            max_w = max(max_w, len(name))
        for i in range(self.max_y, self.min_y - 1, -1):
            row = ""
            for j in range(self.min_x, self.max_x + 1):
                found = False
                for _, loc in self.locations.items():
                    if loc.x == j and loc.y == i:
                        row += loc.name.center(max_w)
                        found = True
                if not found:
                    row += "_".center(max_w)
            final_string += row
            if i != self.min_y:
                final_string += "\n"
        return final_string # Implement a method to print the world's map or details. Many ways to do this, up to you.

def get_direction(start, end):
    direction = ""
    if start.y < end.y:
        direction += "north"
    elif start.y > end.y:
        direction += "south"
    if start.x < end.x:
        direction += "east"
    elif start.x > end.x:
        direction += "west"
    return str.capitalize(direction)

def get_distance(start, end):
    return int(sqrt((start.x - end.x) ** 2 + (start.y - end.y) ** 2) + 0.5)

"""TODO: Implement this function.

Defines the whole world! All the places, how they are accessible from each other or aren't, etc."""
def build_world():
    world = World()

    # You should load Locations out of the .json file, then build a graph (World).
    # Locations have (x,y) coordinates now.
    # (0,0) could be the center. North is +y, East is +x
    # The coordinates in the json file's locations should match this scheme, and if you choose to implement __str__ above, it could look very nice with some effort and can use these coordinates. But that is the only reason they are included. You do not *have* to stress over this - it's a minor detail, but do make sure you
    # corretly put the coordiante information onto the Location object when you make it.
    # Note also that locations include information about enemies.
    # You should pull all this info out and put it into a Location object, and then you can decide for yourself how you want locations to connect to each other. Establish those connections with the add_connection function above.

    #A start:
    data = load_game_data("game_data.json")
    location_data = data["assets"]["locations"]
    enemies = data["assets"]["enemies"]
    
    for name, loc in location_data.items(): # Don't know what the loc object looks like? Guess what I'm going to tell you that you should do.
        enemy_dicts = []
        for enemy in loc["enemies"]:
            for enemy_data in enemies:
                if enemy_data["name"] == enemy:
                    enemy_dicts.append(enemy_data)
        new_location = Location(name, loc["description"], enemy_dicts, loc["coords"][0], loc["coords"][1])
        world.add_node(new_location)

    # Next, define the connections (your call! but if you plan to build the map, connections should match coordinate info. You can feel free to modify the JSON file to align with your connetion schema).
    #TODO

    for loc_name, loc_data in world.locations.items():
        if loc_name == "Town":
            for other_loc_name, other_loc_data in world.locations.items():
                if other_loc_name in ["Cave", "Desert"]:
                    world.add_edge(loc_name, get_direction(loc_data, other_loc_data), other_loc_name, get_distance(loc_data, other_loc_data))
        elif loc_name == "City":
            for other_loc_name, other_loc_data in world.locations.items():
                if other_loc_name in ["Mountains", "Forest", "Cave", "Desert"]:
                    world.add_edge(loc_name, get_direction(loc_data, other_loc_data), other_loc_name, get_distance(loc_data, other_loc_data))
        elif loc_name == "Desert":
            for other_loc_name, other_loc_data in world.locations.items():
                if other_loc_name in ["Town", "Cave", "City", "Mountains"]:
                    world.add_edge(loc_name, get_direction(loc_data, other_loc_data), other_loc_name, get_distance(loc_data, other_loc_data))
        elif loc_name == "Mountains":
            for other_loc_name, other_loc_data in world.locations.items():
                if other_loc_name in ["Forest", "City", "Cave", "Desert"]:
                    world.add_edge(loc_name, get_direction(loc_data, other_loc_data), other_loc_name, get_distance(loc_data, other_loc_data))
        elif loc_name == "Forest":
            for other_loc_name, other_loc_data in world.locations.items():
                if other_loc_name in ["City", "Mountains"]:
                    world.add_edge(loc_name, get_direction(loc_data, other_loc_data), other_loc_name, get_distance(loc_data, other_loc_data))
        elif loc_name == "Cave":
            for other_loc_name, other_loc_data in world.locations.items():
                if other_loc_name in ["Town", "Desert", "Mountains", "City"]:
                    world.add_edge(loc_name, get_direction(loc_data, other_loc_data), other_loc_name, get_distance(loc_data, other_loc_data))
    # F
    # Ci M
    # Ca D
    # T 
    return world