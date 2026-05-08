import random

class DecisionTree():
    def __init__(self, root):
        self.root = root
    # Takes in a representation of the current combat in dictionary format
    # Returns a dictionary of enemy effects
    def getEnemyAction(self, combatState): # O(n^2)
        # where n is the number of levels in the tree
        current_node = self.root
        while isinstance(current_node, Choice):
            current_node = current_node.getChoice(combatState)
        return current_node.takeAction()

class EnemyAction():
    def __init__(self, effect):
        # effect should be a dictionary with:
        # "target": string that describes target
        # "effect": effect key
        # "targets_allies": whether or not it affects allied enemies
        self.effect = effect
    # Returns the current action that this node represents
    def takeAction(self):
        return self.effect
    def __str__(self):
        return str(self.effect)

# Empty class defined for easier type checking
class Choice():
    pass

class DecisionNode(Choice):
    def __init__(self, decision_type, nodes):
        # Should be a lambda function that receives the combat state and returns an index
        self.decider_type = decision_type
        self.nodes = nodes
    # Accepts a representation of the current function
    # Returns the node that should be considered next
    def getChoice(self, combatState):  # O(n)
        if parse_decision(self.decider_type, combatState) >= len(self.nodes):
            return EnemyAction({})
        return self.nodes[parse_decision(self.decider_type, combatState)]

class RandomDecision(Choice):
    def __init__(self, nodes, choice_weights = None):
        self.nodes = nodes  # List of nodes
        if choice_weights is None:
            self.choices = [1] * len(nodes)
        else:
            self.choices = choice_weights

    def getChoice(self, _):  # O(n) where n is the length of the list
        weight_sum = sum(self.choices)
        chosen = random.randint(1, weight_sum)
        print(chosen)
        current_sum = 0
        for i in range(len(self.choices)):
            current_sum += self.choices[i]
            if current_sum >= chosen:
                return self.nodes[i]

# Helper function
# Best and worst case is O(1)
def get_hp_percent(entity):
    return entity.hp / entity.max_hp

# Decision function is O(1)
def parse_decision(decision_type, state):
    if decision_type == "first_turn":
        return 0 if state["turn"] == 1 else 1
    if decision_type == "low_hp":
        return 0 if get_hp_percent(state["enemy"]) < 0.5 else 1
    if decision_type == "hero_weak":
        return 0 if get_hp_percent(state["hero"]) < 0.5 else 1
    return 0

def get_node_from_entry(dict):
    if dict.get("choices") is None and dict.get("target") is None:
        return EnemyAction({})
    if dict.get("target") is not None:
        return EnemyAction({
            "effect": dict["type"],
            "target": dict.get("target"),
        })
    elif dict["type"] == "random":
        all_subnodes = []
        for choice in dict["choices"]:
            all_subnodes.append(get_node_from_entry(choice))
        return RandomDecision(all_subnodes, dict.get("weights"))
    else:
        all_subnodes = []
        for choice in dict["choices"]:
            all_subnodes.append(get_node_from_entry(choice))
        return DecisionNode(dict["type"], all_subnodes)

def parse_enemy_ai(enemy_data):
    root = enemy_data["ai"]
    return DecisionTree(get_node_from_entry(root))
