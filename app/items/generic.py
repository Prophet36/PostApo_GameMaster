from abc import ABC, abstractmethod


class Item(ABC):
    """This is abstract base class representing items existing in the game and contains necessary and common parameters
    for all items.
    """

    @abstractmethod
    def __init__(self, item_id, tags, name, desc, value, weight):
        """Initialize object instance with specified parameters.
        :param item_id: ID of the item
        :param tags: tags associated with the item
        :param name: name of the item
        :param desc: quick description of the item
        :param value: bartering value
        :param weight: weight of the item
        """
        self._item_id = item_id
        self._tags = tags
        self._name = name
        self._desc = desc
        self._value = value
        self._weight = weight

    @property
    def item_id(self):
        """Get item's ID.
        :return: item's ID
        """
        return self._item_id

    @property
    def tags(self):
        """Get item's tags.
        :return: item's tags
        """
        return self._tags

    @property
    def name(self):
        """Get item's name.
        :return: item's name
        """
        return self._name

    @property
    def desc(self):
        """Get item's quick description.
        :return: item's description
        """
        return self._desc

    @property
    def value(self):
        """Get item's bartering value.
        :return: item's value
        """
        return self._value

    @property
    def weight(self):
        """Get item's weight.
        :return: item's weight
        """
        return self._weight


class Armor(Item):
    """This class derives from Item abstract base class. It represents armors existing in the game and contains common
    item parameters, while incorporating armor specific parameters.
    """

    def __init__(self, item_id, tags, name, desc, dmg_res, rad_res, evasion, value, weight):
        """Initialize object instance with specified parameters.
        :param item_id: ID of the armor
        :param tags: tags associated with the armor
        :param name: name of the armor
        :param desc: quick description of the armor
        :param dmg_res: damage resistance provided by the armor
        :param rad_res: radiation resistance provided by the armor (measured in percents)
        :param evasion: evasion bonus provided by the armor
        :param value: bartering value
        :param weight: weight of the armor
        """
        super().__init__(item_id, tags, name, desc, value, weight)
        self._dmg_res = dmg_res
        self._rad_res = rad_res
        self._evasion = evasion

    def __str__(self):
        return "ID: {}, tags: {}, name: {}, description: {}, damage resistance: {}, radiation resistance: {}, " \
               "evasion: {}, value: {}, weight: {}" \
               .format(self._item_id, self._tags, self._name, self._desc, self._dmg_res, self._rad_res, self._evasion,
                       self._value, self._weight)

    @property
    def dmg_res(self):
        """Get damage resistance provided by the armor.
        :return: damage resistance
        """
        return self._dmg_res

    @property
    def rad_res(self):
        """Get radiation resistance provided by the armor (measured in percents).
        :return: radiation resistance
        """
        return self._rad_res

    @property
    def evasion(self):
        """Get evasion bonus provided by the armor.
        :return: evasion bonus
        """
        return self._evasion


class Weapon(ABC):
    """This is abstract base class representing weapons existing in the game and contains necessary and common
    parameters and methods for all weapons.
    """

    @abstractmethod
    def __init__(self, damage, armor_pen, accuracy, ap_cost, st_requirement):
        """Initialize object instance with specified parameters.
        :param damage: damage dealt by weapon; formatted as A + XdY, where A is base damage, X is number of Y-sided dice
                       rolls (A is omitted when it would be 0, while X is omitted when it would be 1)
        :param armor_pen: armor penetration
        :param accuracy: bonus (or malus, if negative) to accuracy
        :param ap_cost: action points cost of attack using the weapon
        :param st_requirement: strength required to use the weapon
        """
        self._damage = damage
        self._armor_pen = armor_pen
        self._accuracy = accuracy
        self._ap_cost = ap_cost
        self._st_requirement = st_requirement

    @property
    def damage(self):
        """Get weapon's damage formula.
        :return: damage formula
        """
        return self._damage

    @property
    def armor_pen(self):
        """Get weapon's armor penetration.
        :return: armor penetration
        """
        return self._armor_pen

    @property
    def accuracy(self):
        """Get weapon's bonus (malus) to accuracy.
        :return: bonus (malus) to accuracy
        """
        return self._accuracy

    @property
    def ap_cost(self):
        """Get weapon's attack action points cost.
        :return: action points cost of attack
        """
        return self._ap_cost

    @property
    def st_requirement(self):
        """Get weapon's strength requirement.
        :return: strength requirement
        """
        return self._st_requirement

    def get_dmg_range(self):
        """Get weapon's minimum and maximum damage range.
        :return: damage range as tuple of minimum and maximum damage
        """
        dmg_values = self._damage.split(" + ")
        if len(dmg_values) == 2:
            base_dmg = int(dmg_values[0])
            roll_dmg = dmg_values[1]
        else:
            base_dmg = 0
            roll_dmg = dmg_values[0]
        roll_dmg_values = roll_dmg.split("d")
        if roll_dmg_values[0] == "":
            roll_dmg_values[0] = 1
        roll_dmg_values = [int(x) for x in roll_dmg_values]
        min_dmg = base_dmg + roll_dmg_values[0]
        max_dmg = base_dmg + roll_dmg_values[0] * roll_dmg_values[1]
        return min_dmg, max_dmg
