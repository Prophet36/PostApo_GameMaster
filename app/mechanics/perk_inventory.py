from app.perks.perks import Perk, PlayerTrait, StatusEffect


class PerkInventory:
    """This class represents list of active perks giving various effects for characters in the game.

    The class provides PerkInventoryError exception, which is raised when adding objects that are not instances of Perk
    derived classes or accessing nonexistent perks.
    """

    class PerkInventoryError(Exception):
        """This exception class exist to unify all errors and exceptions occurring during perk inventory manipulation.
        """
        pass

    def __init__(self):
        """Initializes instance of the class with empty list of active perks."""
        self._perks = list()

    def __str__(self):
        str_print = "Perks:"
        if len(self._perks) > 0:
            for idx, perk in enumerate(self._perks):
                str_print += "\n{}: {}".format(idx + 1, perk.name)
        else:
            str_print += "\nNone"
        return str_print

    @property
    def perks(self):
        """Gets a list of active perks, as list of Perk derived object.

        :return: list of Perk derived objects representing active perks
        """
        return self._perks


class PerkInventoryPerkAdder:
    """This class adds perks to specified perk inventory.

    The class uses PerkInventory class' PerkInventoryError exception, which is raised when adding incorrect perk type or
    specified perk inventory is incorrect.
    """

    @staticmethod
    def add_perk(perk_inv, perk_to_add):
        """Adds provided perk to specified perk inventory.

        :param perk_inv: PerkInventory object to add perk in
        :param perk_to_add: Perk derived object to add to perk inventory
        :raises PerkInventoryError: when specified perk inventory or perk is incorrect
        """
        if not isinstance(perk_inv, PerkInventory):
            raise PerkInventory.PerkInventoryError("incorrect object type for perk inventory")
        if isinstance(perk_to_add, Perk):
            PerkInventoryPerkAdder._add_perk(perk_inv=perk_inv, perk_to_add=perk_to_add)
        else:
            raise PerkInventory.PerkInventoryError("incorrect object type to add to perk inventory")

    @staticmethod
    def _add_perk(perk_inv, perk_to_add):
        """Adds provided perk to specified perk inventory by appending to list of active perks.

        :param perk_inv: PerkInventory object to add perk to
        :param perk_to_add: Perk derived object to add to perk inventory
        :raises PerkInventoryError: when adding already existing perk
        """
        if isinstance(perk_to_add, PlayerTrait):
            PerkInventoryPerkAdder._check_conflicting_traits(perk_inv=perk_inv, trait_to_add=perk_to_add)
        for perk in perk_inv.perks:
            if perk.perk_id == perk_to_add.perk_id:
                raise PerkInventory.PerkInventoryError("can't add already existing perk: {}".format(perk_to_add.name))
        else:
            perk_inv.perks.append(perk_to_add)

    @staticmethod
    def _check_conflicting_traits(perk_inv, trait_to_add):
        """Checks for conflicting traits already existing in a list of active perks.

        :param perk_inv: PerkInventory object to check trait conflicts in
        :param trait_to_add: PlayerTrait object to check conflicts for
        :raises PerkInventoryError: when conflicting trait exist in a list of active perks
        """
        conflicting_traits = trait_to_add.get_conflicts_list()
        for perk in perk_inv.perks:
            if perk.perk_id in conflicting_traits:
                raise PerkInventory.PerkInventoryError("can't add conflicting trait: {} for trait: {}"
                                                       .format(trait_to_add.name, perk.name))


class PerkInventoryPerkRemover:
    """This class removes perks from specified perk inventory.

    The class uses PerkInventory class' PerkInventoryError exception, which is raised when removing incorrect perk or
    specified perk inventory is incorrect.
    """

    @staticmethod
    def remove_perk(perk_inv, perk_to_remove):
        """Removes specified perk from specified perk inventory.

        :param perk_inv: PerkInventory object to remove perk from
        :param perk_to_remove: Perk derived object to remove from perk inventory
        :raises PerkInventoryError: when specified perk inventory or perk is incorrect
        """
        if not isinstance(perk_inv, PerkInventory):
            raise PerkInventory.PerkInventoryError("incorrect object type for perk inventory")
        try:
            perk_inv.perks.remove(perk_to_remove)
        except ValueError:
            raise PerkInventory.PerkInventoryError("no such perk in perk inventory")


class PerkInventoryStatusEffectDurationLowerer:
    """This class lowers duration of all status effects in specified perk inventory.

    The class uses PerkInventory class' PerkInventoryError exception, which is raised when specified perk inventory is
    incorrect.
    """

    @staticmethod
    def lower_status_effects_duration(perk_inv):
        """Lowers duration of status effects in specified perk inventory.

        :param perk_inv: PerkInventory object to lower duration of status effects in
        :raises PerkInventoryError: when specified perk inventory is incorrect
        """
        if not isinstance(perk_inv, PerkInventory):
            raise PerkInventory.PerkInventoryError("incorrect object type for perk inventory")
        for perk in perk_inv.perks:
            if isinstance(perk, StatusEffect):
                perk.lower_duration()
