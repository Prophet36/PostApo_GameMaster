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


class CharacterSkillCalculator:
    """This class calculates effective character skills (base values modified by active perks).

    The class uses StatCalculatorError exception, which is raised when provided character is incorrect or getting
    incorrect character skills.
    """

    @staticmethod
    def get_guns(character):
        """Get specified character's effective guns skill.

        :param character: Character derived object to get effective guns skill for
        :return: effective guns skill
        """
        return CharacterSkillCalculator._get_skill(skill="guns", character=character)

    @staticmethod
    def get_energy(character):
        """Get specified character's effective energy weapons skill.

        :param character: Character derived object to get effective energy weapons skill for
        :return: effective energy weapons skill
        """
        return CharacterSkillCalculator._get_skill(skill="energy", character=character)

    @staticmethod
    def get_melee(character):
        """Get specified character's effective melee weapons skill.

        :param character: Character derived object to get effective melee weapons skill for
        :return: effective melee weapons skill
        """
        return CharacterSkillCalculator._get_skill(skill="melee", character=character)

    @staticmethod
    def get_sneak(character):
        """Get specified character's effective sneak skill.

        :param character: Character derived object to get effective sneak skill for
        :return: effective sneak skill
        """
        return CharacterSkillCalculator._get_skill(skill="sneak", character=character)

    @staticmethod
    def get_security(character):
        """Get specified character's effective security skill.

        :param character: Character derived object to get effective security skill for
        :return: effective security skill
        """
        return CharacterSkillCalculator._get_skill(skill="security", character=character)

    @staticmethod
    def get_mechanics(character):
        """Get specified character's effective mechanics skill.

        :param character: Character derived object to get effective mechanics skill for
        :return: effective mechanics skill
        """
        return CharacterSkillCalculator._get_skill(skill="mechanics", character=character)

    @staticmethod
    def get_survival(character):
        """Get specified character's effective survival skill.

        :param character: Character derived object to get effective survival skill for
        :return: effective survival skill
        """
        return CharacterSkillCalculator._get_skill(skill="survival", character=character)

    @staticmethod
    def get_medicine(character):
        """Get specified character's effective medicine skill.

        :param character: Character derived object to get effective medicine skill for
        :return: effective medicine skill
        """
        return CharacterSkillCalculator._get_skill(skill="medicine", character=character)

    @staticmethod
    def _get_skill(skill, character):
        """Get character's specified base skill and calculate and add any bonuses (maluses) provided by character's
        active perks.

        :param skill: name of the skill to get base value for
        :param character: Character derived object to get base skill and active perks from
        :raises StatCalculatorError: when specified character or skill name is incorrect
        :return: effective skill value
        """
        if not isinstance(character, Character):
            raise StatCalculatorError("incorrect object type for character")
        try:
            skill_value = getattr(character, skill)
        except AttributeError:
            raise StatCalculatorError("incorrect character skill: {}".format(skill))
        else:
            skill_value += PerkSkillCalculator.get_skill_bonus(perk_inv=character.perks, skill=skill)
            return skill_value


class CharacterDerivedStatCalculator:
    """This class calculates effective character derived stats (base values derived from attributes and modified by
    active perks).

    The class uses StatCalculatorError exception, which is raised when provided character is incorrect.
    """

    @staticmethod
    def get_carry_weight(character):
        """Get specified character's maximum carry weight (based on strength and active perks).

        :param character: Character derived object to get maximum carry weight for
        :return: maximum carry weight
        """
        CharacterDerivedStatCalculator._check_valid_character(character)
        strength = CharacterAttributeCalculator.get_strength(character)
        carry_weight = 10 + 3 * strength
        carry_weight += PerkDerivedStatCalculator.get_stat_bonus(perk_inv=character.perks, stat="carry_weight")
        return carry_weight

    @staticmethod
    def get_melee_bonus(character):
        """Get specified character's melee damage bonus (based on strength and active perks).

        :param character: Character derived object to get melee damage bonus for
        :return: melee damage bonus
        """
        CharacterDerivedStatCalculator._check_valid_character(character)
        strength = CharacterAttributeCalculator.get_strength(character)
        melee_bonus = 0
        if strength > 5:
            melee_bonus = strength - 5
        melee_bonus += PerkDerivedStatCalculator.get_stat_bonus(perk_inv=character.perks, stat="melee_bonus")
        return melee_bonus

    @staticmethod
    def get_max_health(character):
        """Get specified character's maximum health (based on endurance, level and active perks).

        :param character: Character derived object to get maximum health for
        :return: maximum health
        """
        CharacterDerivedStatCalculator._check_valid_character(character)
        endurance = CharacterAttributeCalculator.get_endurance(character)
        level = character.level
        max_health = (4 * endurance) + (2 * (level - 1))
        max_health += character.health_bonus
        max_health += PerkDerivedStatCalculator.get_stat_bonus(perk_inv=character.perks, stat="health_bonus")
        return max_health

    @staticmethod
    def get_rad_res(character):
        """Get specified character's radiation resistance (based on endurance, active perks and worn armor).

        :param character: Character derived object to get radiation resistance for
        :return: radiation resistance
        """
        CharacterDerivedStatCalculator._check_valid_character(character)
        endurance = CharacterAttributeCalculator.get_endurance(character)
        rad_res = 0
        if endurance > 5:
            rad_res = 5 * (endurance - 5)
        rad_res += PerkDerivedStatCalculator.get_stat_bonus(perk_inv=character.perks, stat="rad_res")
        if character.inventory.equipped_armor is not None:
            rad_res += character.inventory.equipped_armor.rad_res
        return rad_res

    @staticmethod
    def get_evasion(character):
        """Get specified character's evasion (based on agility, active perks and worn armor).

        :param character: Character derived object to get evasion for
        :return: evasion
        """
        CharacterDerivedStatCalculator._check_valid_character(character)
        agility = CharacterAttributeCalculator.get_agility(character)
        evasion = 0
        if agility > 5:
            evasion = agility - 5
        evasion += PerkDerivedStatCalculator.get_stat_bonus(perk_inv=character.perks, stat="evasion")
        if character.inventory.equipped_armor is not None:
            evasion += character.inventory.equipped_armor.evasion
        return evasion

    @staticmethod
    def get_max_ap(character):
        """Get specified character's maximum action points (based on agility and active perks).

        :param character: Character derived object to get maximum action points for
        :return: maximum action points
        """
        CharacterDerivedStatCalculator._check_valid_character(character)
        agility = CharacterAttributeCalculator.get_agility(character)
        action_points = 10 + agility
        action_points += PerkDerivedStatCalculator.get_stat_bonus(perk_inv=character.perks, stat="max_ap")
        return action_points

    @staticmethod
    def get_exp_mult(character):
        """Get specified character's experience gain multiplier (based on intelligence and active perks, measured in
        percents).

        :param character: Character derived object to get experience gain multiplier for
        :return: experience gain multiplier
        """
        CharacterDerivedStatCalculator._check_valid_character(character)
        intelligence = CharacterAttributeCalculator.get_intelligence(character)
        exp_mult = 75
        exp_mult += 5 * intelligence
        exp_mult += PerkDerivedStatCalculator.get_stat_bonus(perk_inv=character.perks, stat="exp_mult")
        return exp_mult

    @staticmethod
    def _check_valid_character(character):
        """Check whether specified character is correct Character derived object.

        :param character: Character derived object
        :raises StatCalculatorError: when specified character is incorrect
        """
        if not isinstance(character, Character):
            raise StatCalculatorError("incorrect object type for character")
