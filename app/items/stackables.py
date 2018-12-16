from abc import ABC, abstractmethod

from app.items.items import Item


class Stackable(ABC):
    """This is abstract base class representing stackable items existing in the game and contains necessary and common
    parameters for all stackable items.
    """

    @abstractmethod
    def __init__(self, max_stack, current_amount):
        """Initializes object instance with specified parameters.

        :param max_stack: stack maximum; how many can fit in one inventory slot
        :param current_amount: current amount in stack
        """
        self._max_stack = max_stack
        self.current_amount = current_amount

    @property
    def max_stack(self):
        """Gets stack maximum.

        :return: maximum stack
        """
        return self._max_stack

    @property
    def current_amount(self):
        """Gets current amount in stack.

        :return: current amount
        """
        return self._current_amount

    @current_amount.setter
    def current_amount(self, value):
        """Sets current amount to provided value.

        :param value: value to set current stack amount to
        :raises ValueError: when value to set current stack to is either negative or exceeds stack maximum
        """
        if value < 0:
            raise ValueError("current amount can't be negative")
        elif value > self._max_stack:
            raise ValueError("current amount can't exceed stack maximum: {}".format(self._max_stack))
        else:
            self._current_amount = value


class Ammo(Item, Stackable):
    """This class derives from Item and Stackable abstract base classes. It represents ammunition existing in the game
    and contains common item and stackable item parameters, while incorporating ammunition specific parameters.
    """

    def __init__(self, item_id, tags, name, desc, max_stack, current_amount, value, weight):
        """Initializes object instance with specified parameters.

        :param item_id: ID of the ammo
        :param tags: tags associated with the ammo
        :param name: name of the ammo
        :param desc: quick description of the ammo
        :param max_stack: stack maximum; how many can fit in one inventory slot
        :param current_amount: current amount in stack
        :param value: bartering value
        :param weight: weight of the ammo
        """
        Item.__init__(self, item_id, tags, name, desc, value, weight)
        Stackable.__init__(self, max_stack, current_amount)

    def __str__(self):
        total_value = self._current_amount * self._value
        total_weight = self._current_amount * self._weight
        return ("ID: {}, tags: {}, name: {}, description: {},\namount: {} / {}, value: {} ({}), weight: {} ({})"
                .format(self._item_id, self._tags, self._name, self._desc, self._current_amount, self._max_stack,
                        self._value, total_value, self._weight, total_weight))


class Consumable(Item, Stackable):
    """This class derives from Item and Stackable abstract base classes. It represents consumables existing in the game
    and contains common item and stackable item parameters, while incorporating consumable specific parameters and
    methods.
    """

    def __init__(self, item_id, tags, name, desc, effect, max_stack, current_amount, value, weight):
        """Initializes object instance with specified parameters.

        :param item_id: ID of the consumable
        :param tags: tags associated with the consumable
        :param name: name of the consumable
        :param desc: quick description of the consumable
        :param effect: effect applied when consumed
        :param max_stack: stack maximum; how many can fit in one inventory slot
        :param current_amount: current amount in stack
        :param value: bartering value
        :param weight: weight of the consumable
        """
        Item.__init__(self, item_id, tags, name, desc, value, weight)
        Stackable.__init__(self, max_stack, current_amount)
        self._effect = effect

    @property
    def effect(self):
        """Gets effect applied when consumed.

        :return: effect applied
        """
        return self._effect

    def __str__(self):
        total_value = self._current_amount * self._value
        total_weight = self._current_amount * self._weight
        return ("ID: {}, tags: {}, name: {}, description: {},\neffect: {}, amount: {} / {}, value: {} ({}), weight: "
                "{} ({})"
                .format(self._item_id, self._tags, self._name, self._desc, self._effect, self._current_amount,
                        self._max_stack, self._value, total_value, self._weight, total_weight))
