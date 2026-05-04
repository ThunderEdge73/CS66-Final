from containers import *

class Enemy:
    def __init__(self, name, enemy_stats):
        self.name = name
        self.hp = enemy_stats['hp']
        self.attack = enemy_stats['attack']
        self.speed = enemy_stats['speed']
        self.xp = enemy_stats['xp']
        self.mana = enemy_stats['mana']
    
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
        self.max_hp = base_stats['max_hp']
        self.defense = base_stats['defense']
        self.attack = base_stats['attack']
        self.strength = base_stats['strength']
        self.mana = base_stats['mana']
        self.luck = base_stats['luck']
        self.xp = XPBar()
        self.level = 1
        self.speed = base_stats['speed'] # This decides whether you or your enemy strikes first
        self.party = Party()
        
        # (Assignment 4 stuff)
        self.inventory = []       
        self.quest_log = QuestLog() 
  
        # (New stuff)
        self.skills_unlocked = [] 
        self.location = None 

    def learn_skill(self, skill):
        self.skills_unlocked.append(skill.name)
        self.mana -= skill.cost
        self.process_skill(skill)

    def process_skill(self, skill):
        effect = skill.effect
        modifier = float(effect[1])
        stat = effect[2]
        return_string = f"You learned {skill.name}! "
        if len(effect) == 4:
            self.strength += modifier
            self.defense += modifier
            return_string += f"STR and DEF increased by {modifier}"
        elif stat == "max_hp":
            self.max_hp += int(modifier)
            return_string += f"MAX HP increased by {int(modifier)}"
            return_string += f"DEF increased by {modifier}"
        elif stat == "speed":
            self.speed += int(modifier)
            return_string += f"SPD increased by {int(modifier)}"
        elif stat == "luck":
            self.luck += modifier
            return_string += f"LUCK increased by {modifier}"
        print(return_string)
    
    def log_event(self, description):
        self.quest_log.add_entry(description)
    
    def level_up_message(self, message):
        return_string = f"You leveled up! LVL: {self.level} | Stat Growth:"
        for stat in message:
            if stat == "max_hp":
                return_string += "\nMAX HP increased by 10"
            elif stat == "defense":
                return_string += "\nDEF increased by 0.1"
            elif stat == "attack":
                return_string += "\nATK increased by 1"
            elif stat == "strength":
                return_string += "\nSTR increased by 0.1"
            elif stat == "speed":
                return_string += "\nSPD increased by 2"
            else:
                return_string += "\nLUCK increased by 0.2"
        print(return_string)

    def __str__(self):
        return f"[HERO] {self.name} \nHP: {self.hp} / {self.max_hp} | DEF: {self.defense} \nATK: {self.attack} | STR: {self.strength} \nSPD: {self.speed} | LUCK: {self.luck} \n{self.xp} \nMANA: {self.mana} \n\nParty: \n{self.party}"

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
        if self.members == []:
            party_print = "You have no party members"
        else:
            for i in range(self.members):
                x = str(print(self.members[i]))
                party_print += f"{x} \n"
        return party_print