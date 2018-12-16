from abc import ABC, abstractmethod


class Item(ABC):
    """This is abstract base class representing items existing in the game and contains necessary and common parameters
    for all items.
    """

    @abstractmethod
    def __init__(self, item_id, tags, name, desc, value, weight):
        """Initializes object instance with specified parameters.

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
        """Gets item's ID.

        :return: item's ID
        """
        return self._item_id

    @property
    def tags(self):
        """Gets item's tags.

        :return: item's tags
        """
        return self._tags

    @property
    def name(self):
        """Gets item's name.

        :return: item's name
        """
        return self._name

    @property
    def desc(self):
        """Gets item's quick description.

        :return: item's description
        """
        return self._desc

    @property
    def value(self):
        """Gets item's bartering value.

        :return: item's value
        """
        return self._value

    @property
    def weight(self):
        """Gets item's weight.

        :return: item's weight
        """
        return self._weight


class Armor(Item):
    """This class derives from Item abstract base class. It represents armors existing in the game and contains common
    item parameters, while incorporating armor specific parameters.
    """

    def __init__(self, item_id, tags, name, desc, dmg_res, rad_res, evasion, value, weight):
        """Initializes object instance with specified parameters.

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
        return ("ID: {}, tags: {}, name: {}, description: {}, damage resistance: {}, radiation resistance: {}, "
                "evasion: {}, value: {}, weight: {}"
                .format(self._item_id, self._tags, self._name, self._desc, self._dmg_res, self._rad_res, self._evasion,
                        self._value, self._weight))

    @property
    def dmg_res(self):
        """Gets damage resistance provided by the armor.

        :return: damage resistance
        """
        return self._dmg_res

    @property
    def rad_res(self):
        """Gets radiation resistance provided by the armor (measured in percents).

        :return: radiation resistance
        """
        return self._rad_res

    @property
    def evasion(self):
        """Gets evasion bonus provided by the armor.

        :return: evasion bonus
        """
        return self._evasion
