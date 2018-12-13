from app.items.generic import Item, Weapon


class MeleeWeapon(Item, Weapon):
    """This class derives from Item and Weapon abstract base classes. It represents melee weapons existing in the game
    and contains common item and weapon parameters and methods, while incorporating melee weapon specific parameters
    and methods.
    """

    def __init__(self, item_id, tags, name, desc, damage, effect, eff_chance, armor_pen, accuracy, ap_cost,
                 st_requirement, value, weight):
        """Initializes object instance with specified parameters.

        :param item_id: ID of the weapon
        :param tags: tags associated with the weapon
        :param name: name of the weapon
        :param desc: quick description of the weapon
        :param damage: damage dealt by weapon; formatted as A + XdY, where A is base damage, X is number of Y-sided dice
                       rolls (A is omitted when it would be 0, while X is omitted when it would be 1)
        :param effect: potential additional effect applied by the weapon
        :param eff_chance: chance to apply additional effect when target is successfully damaged; formatted as A + dX,
                           where A is base chance, X is X-sided roll dice
        :param armor_pen: armor penetration
        :param accuracy: bonus (or malus, if negative) to accuracy
        :param ap_cost: action points cost of attack using the weapon
        :param st_requirement: strength required to use the weapon
        :param value: bartering value
        :param weight: weight of the weapon
        """
        Item.__init__(self, item_id, tags, name, desc, value, weight)
        Weapon.__init__(self, damage, armor_pen, accuracy, ap_cost, st_requirement)
        self._effect = effect
        self._eff_chance = eff_chance

    def __str__(self):
        dmg_range = self.get_dmg_range()
        effect_chance = self.get_effect_chance()
        str_print = ("ID: {}, tags: {}, name: {}, description: {}, damage: {} ({} - {}), effect: {}, "
                     .format(self._item_id, self._tags, self._name, self._desc, self._damage, dmg_range[0], dmg_range[1],
                             self._effect))
        if effect_chance != 0:
            str_print += "with {} chance ({}%), ".format(self._eff_chance, effect_chance)
        str_print += ("penetration: {}, accuracy: {}, AP: {}, strength required: {}, value: {}, weight: {}"
                      .format(self._armor_pen, self._accuracy, self._ap_cost, self._st_requirement, self._value,
                              self._weight))
        return str_print

    @property
    def effect(self):
        """Gets effect potentially applied by the weapon.

        :return: additional effect
        """
        return self._effect

    @property
    def eff_chance(self):
        """Gets weapon's chance to apply additional effect when target is successfully damaged.

        :return: effect chance
        """
        return self._eff_chance

    def get_effect_chance(self):
        """Gets weapon's chance to apply additional effect measured in percents.

        :return: effect chance in percents
        """
        if self._eff_chance != "0":
            eff_chance_values = self._eff_chance.split(" + ")
            eff_chance_percent = 100 + int(eff_chance_values[0]) * 10
            return eff_chance_percent
        else:
            return 0


class RangedWeapon(Item, Weapon):
    """This class derives from Item and Weapon abstract base classes. It represents melee weapons existing in the game
    and contains common item and weapon parameters and methods, while incorporating ranged weapon specific parameters.
    """

    def __init__(self, item_id, tags, name, desc, damage, ammo_type, clip_size, armor_pen, accuracy, ap_cost,
                 st_requirement, value, weight):
        """Initializes object instance with specified parameters.

        :param item_id: ID of the weapon
        :param tags: tags associated with the weapon
        :param name: name of the weapon
        :param desc: quick description of the weapon
        :param damage: damage dealt by weapon; formatted as A + XdY, where A is base damage, X is number of Y-sided dice
                       rolls (A is omitted when it would be 0, while X is omitted when it would be 1)
        :param ammo_type: ammunition type the weapon uses
        :param clip_size: weapon's clip (magazine) size
        :param armor_pen: armor penetration
        :param accuracy: bonus (or malus, if negative) to accuracy
        :param ap_cost: action points cost of attack using the weapon
        :param st_requirement: strength required to use the weapon
        :param value: bartering value
        :param weight: weight of the weapon
        """
        Item.__init__(self, item_id, tags, name, desc, value, weight)
        Weapon.__init__(self, damage, armor_pen, accuracy, ap_cost, st_requirement)
        self._ammo_type = ammo_type
        self._clip_size = clip_size
        self.current_ammo = 0

    def __str__(self):
        dmg_range = self.get_dmg_range()
        return ("ID: {}, tags: {}, name: {}, description: {}, damage: {} ({} - {}), ammo: {} ({} / {}), "
                "penetration: {}, accuracy: {}, AP: {}, strength required: {}, value: {}, weight: {}"
                .format(self._item_id, self._tags, self._name, self._desc, self._damage, dmg_range[0], dmg_range[1],
                        self._ammo_type, self._current_ammo, self._clip_size, self._armor_pen, self._accuracy,
                        self._ap_cost, self._st_requirement, self._value, self._weight))

    @property
    def ammo_type(self):
        """Gets type of ammunition the weapon uses.

        :return: ammunition type
        """
        return self._ammo_type

    @property
    def clip_size(self):
        """Gets size of weapon's clip (magazine).

        :return: clip (magazine) size
        """
        return self._clip_size

    @property
    def current_ammo(self):
        """Gets current amount of ammunition in weapon's clip (magazine).

        :return: current ammunition in clip (magazine)
        """
        return self._current_ammo

    @current_ammo.setter
    def current_ammo(self, value):
        """Sets current amount of ammunition in weapon's clip (magazine) to provided value.

        :param value: value to set current amount of ammunition to
        :raises ValueError: when value to set current amount of ammunition to is either negative or exceeds clip maximum
        """
        if value < 0:
            raise ValueError("current amount of ammunition can't be negative")
        elif value > self._clip_size:
            raise ValueError("current amount of ammunition can't exceed clip (magazine) size: {}".
                             format(self._clip_size))
        else:
            self._current_ammo = value
