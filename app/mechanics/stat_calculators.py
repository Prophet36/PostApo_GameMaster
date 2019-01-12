from app.mechanics.perk_inventory import PerkInventory


class PerkAttributeCalculator:
    """This class calculates bonuses (maluses) to character attributes given by active perks.

    The class uses PerkInventory class' PerkInventoryError exception, which is raised when specified perk inventory is
    incorrect.
    """

    @staticmethod
    def get_attribute_bonus(perk_inv, attribute):
        """Get bonuses (maluses) to specified attribute given by perks in specified perk inventory.

        :param perk_inv: PerkInventory object to get bonuses (maluses) from
        :param attribute: name of the attribute to check bonuses (maluses) for
        :raises PerkInventoryError: when specified perk inventory is incorrect
        """
        if not isinstance(perk_inv, PerkInventory):
            raise PerkInventory.PerkInventoryError("incorrect object type for perk inventory")
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

    The class uses PerkInventory class' PerkInventoryError exception, which is raised when specified perk inventory is
    incorrect.
    """

    @staticmethod
    def get_skill_bonus(perk_inv, skill):
        """Get bonuses (maluses) to specified skill given by perks in specified perk inventory.

        :param perk_inv: PerkInventory object to get bonuses (maluses) from
        :param skill: name of the skill to check bonuses (maluses) for
        :raises PerkInventoryError: when specified perk inventory is incorrect
        """
        if not isinstance(perk_inv, PerkInventory):
            raise PerkInventory.PerkInventoryError("incorrect object type for perk inventory")
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

    The class uses PerkInventory class' PerkInventoryError exception, which is raised when specified perk inventory is
    incorrect.
    """

    @staticmethod
    def get_stat_bonus(perk_inv, stat):
        """Get bonuses (maluses) to specified derived stat given by perks in specified perk inventory.

        :param perk_inv: PerkInventory object to get bonuses (maluses) from
        :param stat: name of the derived stat to check bonuses (maluses) for
        :raises PerkInventoryError: when specified perk inventory is incorrect
        """
        if not isinstance(perk_inv, PerkInventory):
            raise PerkInventory.PerkInventoryError("incorrect object type for perk inventory")
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
