from abc import ABC, abstractmethod

from app.config.game_config import get_health_bonus_human, get_health_bonus_player
from app.mechanics.inventory import Inventory
from app.mechanics.perk_inventory import PerkInventory


class Character(ABC):
    """This is abstract base class representing characters existing in the game and contains necessary and common
    parameters for all characters.
    """

    @abstractmethod
    def __init__(self, name, tags, level, strength, endurance, agility, perception, intelligence):
        """Initializes object instance with specified parameters.

        :param name: character's name
        :param tags: tags associated with the character
        :param level: character's level
        :param strength: strength attribute
        :param endurance: endurance attribute
        :param agility: agility attribute
        :param perception: perception attribute
        :param intelligence: intelligence attribute
        """
        self._name = name
        self._tags = tags
        self._strength = strength
        self._endurance = endurance
        self._agility = agility
        self._perception = perception
        self._intelligence = intelligence
        self._level = level
        self._health = 0
        self._health_bonus = 0
        self._action_points = 0
        self._inventory = Inventory()
        self._perks = PerkInventory()

    @property
    def name(self):
        """Gets character's name.

        :return: character's name
        """
        return self._name

    @property
    def tags(self):
        """Gets character's tags.

        :return: character's tags
        """
        return self._tags

    @property
    def level(self):
        """Gets character's level.

        :return: character's level
        """
        return self._level

    @property
    def strength(self):
        """Gets character's strength attribute.

        :return: character's strength
        """
        return self._strength

    @property
    def endurance(self):
        """Gets character's endurance attribute.

        :return: character's endurance
        """
        return self._endurance

    @property
    def agility(self):
        """Gets character' agility attribute.

        :return: character's agility
        """
        return self._agility

    @property
    def perception(self):
        """Gets character's perception attribute.

        :return: character's perception
        """
        return self._perception

    @property
    def intelligence(self):
        """Gets character's intelligence attribute.

        :return: character's intelligence
        """
        return self._intelligence

    @property
    def health(self):
        """Gets character's current health.

        :return: character's current health
        """
        return self._health

    @property
    def health_bonus(self):
        """Gets character's bonus to max health.

        :return: character's bonus to max health
        """
        return self._health_bonus

    @property
    def action_points(self):
        """Gets character's current action points.

        :return: character's current action points
        """
        return self._action_points

    @property
    def inventory(self):
        """Gets character's inventory.

        :return: Inventory object representing character's inventory
        """
        return self._inventory

    @property
    def perks(self):
        """Gets character's perks.

        :return: PerkInventory object representing character's perks
        """
        return self._perks


class Human(Character):
    """This class derives from Character abstract base class. It represents human characters existing in the game and
    contains common character parameters, while incorporating human character specific parameters.
    """

    def __init__(self, name, tags, level, strength, endurance, agility, perception, intelligence):
        """Initializes object instance with specified parameters.

        :param name: character's name
        :param tags: tags associated with the character
        :param level: character's level
        :param strength: strength attribute
        :param endurance: endurance attribute
        :param agility: agility attribute
        :param perception: perception attribute
        :param intelligence: intelligence attribute
        """
        super().__init__(name, tags, level, strength, endurance, agility, perception, intelligence)
        self._guns = 1
        self._energy = 1
        self._melee = 1
        self._sneak = 1
        self._security = 1
        self._mechanics = 1
        self._survival = 1
        self._medicine = 1
        self._health_bonus = get_health_bonus_human()

    def __str__(self):
        return ("name: {}, tags: {}, level: {},\nstrength: {}, endurance: {}, agility: {}, perception: {}, "
                "intelligence: {},\nguns: {}, energy weapons: {}, melee weapons: {},\nsneak: {}, security: {}, "
                "mechanics: {}, survival: {}, medicine: {}"
                .format(self._name, self._tags, self._level, self._strength, self._endurance, self._agility,
                        self._perception, self._intelligence, self._guns, self._energy, self._melee, self._sneak,
                        self._security, self._mechanics, self._survival, self._medicine))

    @property
    def guns(self):
        """Gets character's guns skill proficiency.

        :return: character's guns skill
        """
        return self._guns

    @property
    def energy(self):
        """Gets character's energy weapons skill proficiency.

        :return: character's energy weapons skill
        """
        return self._energy

    @property
    def melee(self):
        """Gets character's melee weapons skill proficiency.

        :return: character's melee weapons skill
        """
        return self._melee

    @property
    def sneak(self):
        """Gets character's sneak skill proficiency.

        :return: character's sneak skill
        """
        return self._sneak

    @property
    def security(self):
        """Gets character's security (lockpicking, hacking) skill proficiency.

        :return: character's security skill
        """
        return self._security

    @property
    def mechanics(self):
        """Gets character's mechanics (mechanical knowledge, repairing) skill proficiency.

        :return: character's mechanics skill
        """
        return self._mechanics

    @property
    def survival(self):
        """Gets character's survival skill proficiency.

        :return: character's survival skill
        """
        return self._survival

    @property
    def medicine(self):
        """Gets character's medicine skill proficiency.

        :return: character's medicine skill
        """
        return self._medicine


class Player(Human):
    """This class derives from Human class. It represents player controlled characters existing in the game and contains
    common human character parameters, while incorporating player controlled character specific parameters.
    """

    def __init__(self, name, tags, level, strength, endurance, agility, perception, intelligence, experience):
        """Initializes object instance with specified parameters.

        :param name: player's name
        :param tags: tags associated with the player
        :param level: player's level
        :param strength: strength attribute
        :param endurance: endurance attribute
        :param agility: agility attribute
        :param perception: perception attribute
        :param intelligence: intelligence attribute
        :param experience: player's experience points
        """
        super().__init__(name, tags, level, strength, endurance, agility, perception, intelligence)
        self._health_bonus = get_health_bonus_player()
        self._experience = experience

    def __str__(self):
        return ("name: {}, tags: {}, level: {}, experience: {},\nstrength: {}, endurance: {}, agility: {}, "
                "perception: {}, intelligence: {},\nguns: {}, energy weapons: {}, melee weapons: {},\nsneak: {}, "
                "security: {}, mechanics: {}, survival: {}, medicine: {}"
                .format(self._name, self._tags, self._level, self._experience, self._strength, self._endurance,
                        self._agility, self._perception, self._intelligence, self._guns, self._energy, self._melee,
                        self._sneak, self._security, self._mechanics, self._survival, self._medicine))

    @property
    def experience(self):
        """Gets player's experience points.
                
        :return: player's experience
        """
        return self._experience


class Critter(Character):
    """This class derives from Character abstract base class. It represents critters (animals, mutants, etc) existing in
    the game and contains common character parameters, while incorporating critter specific parameters.
    """

    def __init__(self, name, tags, level, strength, endurance, agility, perception, intelligence, health_bonus,
                 exp_award):
        """Initializes object instance with specified parameters.

        :param name: critter's name
        :param tags: tags associated with the critter
        :param level: critter's level
        :param strength: strength attribute
        :param endurance: endurance attribute
        :param agility: agility attribute
        :param perception: perception attribute
        :param intelligence: intelligence attribute
        :param health_bonus: critter's bonus to max health
        :param exp_award: experience award provided upon killing the critter
        """
        super().__init__(name, tags, level, strength, endurance, agility, perception, intelligence)
        self._health_bonus = health_bonus
        self._experience_award = exp_award

    def __str__(self):
        return ("name: {}, tags: {}, level: {},\nstrength: {}, endurance: {}, agility: {}, perception: {}, "
                "intelligence: {},\nexperience award: {}"
                .format(self._name, self._tags, self._level, self._strength, self._endurance, self._agility,
                        self._perception, self._intelligence, self._experience_award))

    @property
    def experience_award(self):
        """Gets experience award provided upon killing the critter.

        :return: critter's experience award
        """
        return self._experience_award
