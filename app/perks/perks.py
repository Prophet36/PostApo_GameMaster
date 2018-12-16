from abc import ABC, abstractmethod


class Perk(ABC):
    """This is abstract base class representing perks existing in the game and contains necessary and common parameters
    for all perks.
    """

    @abstractmethod
    def __init__(self, perk_id, tags, name, desc, effects):
        """Initializes object instance with specified parameters.

        :param perk_id: ID of the perk
        :param tags: tags associated with the perk
        :param name: name of the perk
        :param desc: quick description of the perk
        :param effects: effects provided by the perk
        """
        self._perk_id = perk_id
        self._tags = tags
        self._name = name
        self._desc = desc
        self._effects = effects

    @property
    def perk_id(self):
        """Gets perk's ID.

        :return: perk's ID
        """
        return self._perk_id

    @property
    def tags(self):
        """Gets perk's tags.

        :return: perk's tags
        """
        return self._tags

    @property
    def name(self):
        """Gets perk's name.

        :return: perk's name
        """
        return self._name

    @property
    def desc(self):
        """Gets perk's quick description.

        :return: perk's description
        """
        return self._desc

    @property
    def effects(self):
        """Gets perk's effects.

        :return: perk's effects
        """
        return self._effects

    def get_effects_list(self):
        """Gets a list of effects provided by the perk.

        :return: list of perk's effects
        """
        effects_list = list()
        for effect in self._effects.split("; "):
            effects_list.append(effect)
        return effects_list


class CharacterPerk(Perk):
    """This class derives from Perk abstract base class. It represents character perks existing in the game and contains
    common perk parameters, while incorporating character perk specific parameters.
    """

    def __init__(self, perk_id, tags, name, desc, effects, requirements):
        """Initializes object instance with specified parameters.

        :param perk_id: ID of the perk
        :param tags: tags associated with the perk
        :param name: name of the perk
        :param desc: quick description of the perk
        :param effects: effects provided by the perk
        :param requirements: attributes and skills required to obtain the perk
        """
        super().__init__(perk_id, tags, name, desc, effects)
        self._requirements = requirements

    def __str__(self):
        str_print = "ID: {}, tags: {}, name: {}, description: {},\n".format(self._perk_id, self._tags, self._name,
                                                                            self._desc)
        if len(self.get_effects_list()) == 1:
            str_print += "effect: {}, ".format(self._effects)
        else:
            str_print += "effects: {}, ".format(self._effects)
        if len(self.get_requirements_list()) == 1:
            str_print += "requirement: {}".format(self._requirements)
        else:
            str_print += "requirements: {}".format(self._requirements)
        return str_print

    @property
    def requirements(self):
        """Gets perk's requirements.

        :return: perk's requirements
        """
        return self._requirements

    def get_requirements_list(self):
        """Gets a list of attributes and skills required to obtain the perk.

        :return: list of perk's requirements
        """
        requirements_list = list()
        for requirement in self._requirements.split("; "):
            requirements_list.append(requirement)
        return requirements_list


class PlayerTrait(Perk):
    """This class derives from Perk abstract base class. It represents player character's traits existing in the game
    and contains common perk parameters, while incorporating trait specific parameters.
    """

    def __init__(self, perk_id, tags, name, desc, effects, conflicts):
        """Initializes object instance with specified parameters.

        :param perk_id: ID of the trait
        :param tags: tags associated with the trait
        :param name: name of the trait
        :param desc: quick description of the trait
        :param effects: effects provided by the trait
        :param conflicts: other traits that conflict with this trait
        """
        super().__init__(perk_id, tags, name, desc, effects)
        self._conflicts = conflicts

    def __str__(self):
        str_print = "ID: {}, tags: {}, name: {}, description: {},\n".format(self._perk_id, self._tags, self._name,
                                                                            self._desc)
        if len(self.get_effects_list()) == 1:
            str_print += "effect: {}, ".format(self._effects)
        else:
            str_print += "effects: {}, ".format(self._effects)
        if len(self.get_conflicts_list()) == 1:
            str_print += "conflict: {}".format(self.conflicts)
        else:
            str_print += "conflicts: {}".format(self.conflicts)
        return str_print

    @property
    def conflicts(self):
        """Gets trait's conflicts.

        :return: trait's conflicts
        """
        return self._conflicts

    def get_conflicts_list(self):
        """Gets a list of other traits that conflict with this trait.

        :return: list of trait's conflicts
        """
        conflicts_list = list()
        for conflict in self._conflicts.split(", "):
            conflicts_list.append(conflict)
        return conflicts_list


class StatusEffect(Perk):
    """This class derives from Perk abstract base class. It represents active status effects existing in the game and
    contains common perk parameters, while incorporating status effect specific parameters.
    """

    def __init__(self, perk_id, tags, name, desc, effects, duration):
        """Initializes object instance with specified parameters.

        :param perk_id: ID of the status effect
        :param tags: tags associated with the status effect
        :param name: name of the status effect
        :param desc: quick description of the status effect
        :param effects: effects provided by the status effect
        :param duration: how long the status effect is active, measured in turns (negative value means permanent)
        """
        super().__init__(perk_id, tags, name, desc, effects)
        self._duration = duration

    def __str__(self):
        str_print = "ID: {}, tags: {}, name: {}, description: {},\n".format(self._perk_id, self._tags, self._name,
                                                                            self._desc)
        if len(self.get_effects_list()) == 1:
            str_print += "effect: {}, ".format(self._effects)
        else:
            str_print += "effects: {}, ".format(self._effects)
        if self._duration < 0:
            str_print += "duration: permanent"
        elif self._duration == 1:
            str_print += "duration: {} turn".format(self._duration)
        else:
            str_print += "duration: {} turns".format(self._duration)
        return str_print

    @property
    def duration(self):
        """Gets status effect's duration.

        Negative value means permanent duration.

        :return: status effect's duration
        """
        return self._duration

    def lower_duration(self):
        """Lowers current status effect duration by 1, unless duration is already 0 or lower."""
        if self._duration > 0:
            self._duration -= 1
