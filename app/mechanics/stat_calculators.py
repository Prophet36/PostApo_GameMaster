from app.characters.characters import Character
from app.mechanics.perk_inventory import PerkInventory


class StatCalculatorError(Exception):
    """This exception class exist to unify all errors and exceptions occurring during stat calculations."""
    pass


class PerkAttributeCalculator:
    """This class calculates bonuses (maluses) to character attributes given by active perks.

    The class uses StatCalculatorError exception, which is raised when specified perk inventory is incorrect.
    """

    @staticmethod
    def get_attribute_bonus(perk_inv, attribute):
        """Get bonuses (maluses) to specified attribute given by perks in specified perk inventory.

        :param perk_inv: PerkInventory object to get bonuses (maluses) from
        :param attribute: name of the attribute to check bonuses (maluses) for
        :raises StatCalculatorError: when specified perk inventory is incorrect
        """
        if not isinstance(perk_inv, PerkInventory):
            raise StatCalculatorError("incorrect object type for perk inventory")
        attribute_bonus = 0
        for perk in perk_inv.perks:
            if "attribute" in perk.tags:
                attribute_bonus += PerkAttributeCalculator._get_attribute_bonus(perk=perk, attribute=attribute)
        return attribute_bonus

    @staticmethod
    def _get_attribute_bonus(perk, attribute):
        """Get bonuses (maluses) to specified attribute from provided perk.

        :param perk: Perk derived object to get bonuses (maluses) from
        :param attribute: name of the attribute to check bonuses (maluses) for
        """
        attribute_bonus = 0
        for effect in perk.get_effects_list():
            if attribute in effect:
                attribute_bonus += int(effect.split()[-1])
        return attribute_bonus


class PerkSkillCalculator:
    """This class calculates bonuses (maluses) to character skills given by active perks.

    The class uses StatCalculatorError exception, which is raised when specified perk inventory is incorrect.
    """

    @staticmethod
    def get_skill_bonus(perk_inv, skill):
        """Get bonuses (maluses) to specified skill given by perks in specified perk inventory.

        :param perk_inv: PerkInventory object to get bonuses (maluses) from
        :param skill: name of the skill to check bonuses (maluses) for
        :raises StatCalculatorError: when specified perk inventory is incorrect
        """
        if not isinstance(perk_inv, PerkInventory):
            raise StatCalculatorError("incorrect object type for perk inventory")
        skill_bonus = 0
        for perk in perk_inv.perks:
            if "skill" in perk.tags:
                skill_bonus += PerkSkillCalculator._get_skill_bonus(perk=perk, skill=skill)
        return skill_bonus

    @staticmethod
    def _get_skill_bonus(perk, skill):
        """Get bonuses (maluses) to specified skill from provided perk.

        :param perk: Perk derived object to get bonuses (maluses) from
        :param skill: name of the skill to check bonuses (maluses) for
        """
        skill_bonus = 0
        for effect in perk.get_effects_list():
            if skill in effect:
                skill_bonus += int(effect.split()[-1])
        return skill_bonus


class PerkDerivedStatCalculator:
    """This class calculates bonuses (maluses) to character's derived stats given by active perks.

    The class uses StatCalculatorError exception, which is raised when specified perk inventory is incorrect.
    """

    @staticmethod
    def get_stat_bonus(perk_inv, stat):
        """Get bonuses (maluses) to specified derived stat given by perks in specified perk inventory.

        :param perk_inv: PerkInventory object to get bonuses (maluses) from
        :param stat: name of the derived stat to check bonuses (maluses) for
        :raises StatCalculatorError: when specified perk inventory is incorrect
        """
        if not isinstance(perk_inv, PerkInventory):
            raise StatCalculatorError("incorrect object type for perk inventory")
        stat_bonus = 0
        for perk in perk_inv.perks:
            stat_bonus += PerkDerivedStatCalculator._get_stat_bonus(perk=perk, stat=stat)
        return stat_bonus

    @staticmethod
    def _get_stat_bonus(perk, stat):
        """Get bonuses (maluses) to specified derived stat from provided perk.

        :param perk: Perk derived object to get bonuses (maluses) from
        :param stat: name of the derived stat to check bonuses (maluses) for
        """
        stat_bonus = 0
        for effect in perk.get_effects_list():
            if stat in effect:
                stat_bonus += int(effect.split()[-1])
        return stat_bonus


class CharacterAttributeCalculator:
    """This class calculates effective character attributes (base values modified by active perks).

    The class uses StatCalculatorError exception, which is raised when provided character is incorrect or getting
    incorrect character attributes.
    """

    @staticmethod
    def get_strength(character):
        """Get specified character's effective strength attribute.

        :param character: Character derived object to get effective strength for
        :return: effective strength
        """
        return CharacterAttributeCalculator._get_attribute(attribute="strength", character=character)

    @staticmethod
    def get_endurance(character):
        """Get specified character's effective endurance attribute.

        :param character: Character derived object to get effective endurance for
        :return: effective endurance
        """
        return CharacterAttributeCalculator._get_attribute(attribute="endurance", character=character)

    @staticmethod
    def get_agility(character):
        """Get specified character's effective agility attribute.

        :param character: Character derived object to get effective agility for
        :return: effective agility
        """
        return CharacterAttributeCalculator._get_attribute(attribute="agility", character=character)

    @staticmethod
    def get_perception(character):
        """Get specified character's effective perception attribute.

        :param character: Character derived object to get effective perception for
        :return: effective perception
        """
        return CharacterAttributeCalculator._get_attribute(attribute="perception", character=character)

    @staticmethod
    def get_intelligence(character):
        """Get specified character's effective intelligence attribute.

        :param character: Character derived object to get effective intelligence for
        :return: effective intelligence
        """
        return CharacterAttributeCalculator._get_attribute(attribute="intelligence", character=character)

    @staticmethod
    def _get_attribute(attribute, character):
        """Get character's specified base attribute and calculate and add any bonuses (maluses) provided by character's
        active perks.

        :param attribute: name of the attribute to get base value for
        :param character: Character derived object to get base attribute and active perks from
        :raises StatCalculatorError: when specified character or attribute name is incorrect
        :return: effective attribute value
        """
        if not isinstance(character, Character):
            raise StatCalculatorError("incorrect object type for character")
        try:
            attribute_value = getattr(character, attribute)
        except AttributeError:
            raise StatCalculatorError("incorrect character attribute: {}".format(attribute))
        else:
            attribute_value += PerkAttributeCalculator.get_attribute_bonus(perk_inv=character.perks,
                                                                           attribute=attribute)
            return attribute_value
