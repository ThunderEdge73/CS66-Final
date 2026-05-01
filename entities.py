from containers import QuestLog

class Enemy:
    def __init__(self, name, hp, attack, speed):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.speed = speed
    
    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0: self.hp = 0

    def __str__(self):
        return f"[ENEMY] {self.name} (HP: {self.hp})"
    
class Ally:
    def __init__(self, name, hp, attack, speed):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.speed = speed

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0: self.hp = 0
    
    def __str__(self):
        return f"[ALLY] {self.name} | HP: {self.hp} | ATK: {self.attack} | SPD: {self.speed}"

class Hero:
    def __init__(self, name, base_stats):
        self.name = name
        self.hp = base_stats['hp']
        self.attack = base_stats['attack']
        self.defense = base_stats['defense']
        self.mana = base_stats['mana']
        self.xp = base_stats['xp']
        self.speed = base_stats['speed'] # This decides whether you or your enemy strikes first
        self.party = Party()
        
        # (Assignment 4 stuff)
        self.inventory = []       
        self.quest_log = QuestLog() 
  
        # (New stuff)
        self.skills_unlocked = [] 
        self.location = None 

    def learn_skill(self, skill_name):
        self.skills_unlocked.append(skill_name)
    
    def log_event(self, description):
        self.quest_log.add_entry(description)

    def __str__(self):
        return f"[HERO] {self.name} | HP: {self.hp} | ATK: {self.attack} | SPD: {self.speed}"

    def __add__(self, item):
        self.inventory.append(item)
        return self
    
class Party:
    def __init__(self):
        self.limit = 2
        self.members = []

    def add_member(self, ally):
        if len(self.members) == self.limit:
            return "Party limit reached."
        self.members.append(ally)
        return f"{ally.name} has been added to the party."

    def remove_member(self, ally):
        self.members.remove(ally)

    def get_allies(self):
        return self.members

    def __str__(self):
        party_print = ""
        for i in range(self.limit):
            x = str(print(self.members[i]))
            party_print += f"{x} \n"
        if party_print == "":
            party_print = "You have no party members"
        return party_print
        