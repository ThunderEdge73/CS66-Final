'''
Skill List:
Agi - Fire attack skill, variants: Agilao, Agidyne, Trisagion
Dia - Heal skill, variants: Diarama, Diarahan
Life Bonus - Max HP booster, variants: Life Gain, Life Surge
Rakukaja - Temporary defense booster, variants: Rakukajaon/Marakukaja (multi-target?)
Sukukaja - Speed booster, variants: Sukukajaon/Masukukaja (multi-target)
Mana Bonus - Luck booster, variants: Mana Gain, Mana Surge
Tarukaja - Temporary strength booster, variants: Tarukajaon/Matarukaja (multi-target?)
Luster Candy - Temporary strength, defense, (and speed?) booster

Other potential attack skills:
Bufu - Ice attack skill, variants: Bufula, Bufudyne, Ice Age
Zio - Electric attack skill, variants: Zionga, Ziodyne, Thunder Reign
Zan - Wind attack skill, variants: Zanma, Zandyne, Killing Wind
Hama - Light attack skill, variants: Hamaon, Hamabarion, Divine Judgement
Mudo - Dark attack skill, variants: Mudoon, Mudobarion, Demonic Decree
Megido - Non-elemental attack skill, variants: Megidola, Megidolaon, Morning Star
'''

class SkillNode:
    def __init__(self, name, data):
        self.name = name
        self.type = data['type']
        self.cost = data['cost']
        self.use_cost = data['use_cost']
        self.level = data['level']
        self.effect = data['effect'].split()
        self.req_names = data['requirements'] # String name of the parent
        self.req_nodes = [] # Actual link to the node object (built later)

class SkillTree:
    def __init__(self, skill_data):
        self.nodes = {}
        # 1. create all nodes
        for name, info in skill_data.items():
            self.nodes[name] = SkillNode(name, info)
        
        # 2. link the nodes (build the tree)
        for node in self.nodes.values():
            if node.req_names != []:
                for req in node.req_names:
                    node.req_nodes.append(self.nodes[req])

    def can_unlock(self, skill_name, hero):
        for req in self.nodes[skill_name].req_names:
            if req not in hero.skills_unlocked:
                return "pre-req"
        if self.nodes[skill_name].level > hero.level:
            return "level"
        if self.nodes[skill_name].cost > hero.mana:
            return "mana"
        return True
    
    def check_skills(self, unlocked_skills):
        skills_list = []
        if unlocked_skills == {}:
            skills_list.append("Agi")
        else:
            for skill in self.nodes:
                if self.nodes[skill].req_names != []:
                    for i in range(len(self.nodes[skill].req_names)):
                        if self.nodes[skill].req_names[i] in unlocked_skills and skill not in unlocked_skills:
                            skills_list.append(skill)
                            break
        return skills_list
    
    def available_skills(self, hero):
        return_string = ""
        for skill in self.check_skills(hero.skills_unlocked):
            return_string += f"{skill}: LVL {self.nodes[skill].level}, {self.nodes[skill].cost} Mana, REQS: "
            if self.nodes[skill].req_names == []:
                return_string += "None"
            elif len(self.nodes[skill].req_names) == 1:
                return_string += f"{self.nodes[skill].req_names[0]} | "
            else:
                for req in self.nodes[skill].req_names:
                    if req == self.nodes[skill].req_names[-1]:
                        return_string += f"{req}"
                    else:
                        return_string += f"{req}, "
                return_string += " | "
        return return_string