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
