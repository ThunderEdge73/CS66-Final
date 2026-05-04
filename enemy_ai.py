import random
from utils import load_game_data
from entities import Enemy

class DecisionTree():
    def __init__(self, root):
        self.root = root

    def getEnemyAction(self, combatState):
        current_node = self.root
        while isinstance(current_node, Choice):
            current_node = current_node.getChoice(combatState)
        return current_node.takeAction(combatState)


class EnemyAction():
    def __init__(self, action_lambda):
        # action_lambda should return a dictionary with:
        # "targets": list of targets
        # "effects": dictionary of effects
        self.action = action_lambda

    def takeAction(self, combatState):
        return self.action(combatState)


class Choice():
    def __init__(self):
        pass

    def getChoice(self, combatState):
        pass


class DecisionNode(Choice):
    def __init__(self, decision_lambda, nodes):
        # Should be a lambda function that receives the combat state and returns an index
        self.decider = decision_lambda
        self.nodes = nodes

    def getChoice(self, combatState):  # Big O depends on the decider function
        return self.nodes[self.decider(combatState)]


class RandomDecision(Choice):
    def __init__(self, nodes, choice_weights = None):
        self.nodes = nodes  # List of nodes
        if choice_weights is None:
            self.choices = [1] * len(nodes)
        elif choice_weights is int:
            self.choices = [1] * choice_weights
        else:
            self.choices = choice_weights

    def getChoice(self, combatState):  # O(n) where n is the length of the list
        weight_sum = sum(self.choices)
        chosen = random.randint(1, weight_sum)
        current_sum = 0
        for i in range(len(self.choices)):
            current_sum += self.choices[i]
            if current_sum <= chosen:
                return self.nodes[i]


def get_max_hp(entity):
    return entity.hp / entity.max_hp


def get_enemy(state):
    return state["enemy"]


node_keys = {
    "random": lambda nodes: RandomDecision(nodes),
}

action_keys = {
    "attack": EnemyAction(lambda combatState:
        {"damage": get_enemy(combatState).attack})
}

def get_node_from_entry(dict):
    if node_keys.get(dict["type"]):
        children = []
        for c in dict["choices"]:
            children.append(get_node_from_entry(c))
        return node_keys[dict["type"]](children)
    else: # assume it lives in action_keys
        return action_keys[dict["type"]]

def parse_enemy_ai(enemy):
    enemy_data = load_game_data("game_data.json")["assets"]["enemies"]
    target_data = None
    for data in enemy_data:
        if data["name"] == enemy:
            target_data = data
    root = target_data["ai"]
    return DecisionTree(get_node_from_entry(root))

e_data = load_game_data("game_data.json")["assets"]["enemies"]

enemy = Enemy("Anomaly", e_data[1])

tree = parse_enemy_ai(enemy.name)

print(tree.getEnemyAction({"enemy": enemy}))