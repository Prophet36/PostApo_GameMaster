from app.perks.generic import Perk, StatusEffect


class PerkList:
    """This class represents list of perks giving various effects for characters in the game.

    The class provides PerkError exception, which is raised when adding objects that are not instances of Perk derived
    classes or accessing nonexistent perks.
    """

    class PerkError(Exception):
        """This exception class exist to unify all errors and exceptions occurring during perk manipulation."""
        pass

    def __init__(self):
        """Initializes instance of the class."""
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


class PerkListPerkAdder:
    """This class adds perks to specified perk list.

    The class uses PerkList class' PerkError exception, which is raised when adding incorrect perk type or specified
    perk list is incorrect.
    """

    @staticmethod
    def add_perk(perk_list, perk_to_add):
        """Adds provided perk to specified perk list.

        :param perk_list: PerkList object to add perk in
        :param perk_to_add: Perk derived object to add to perk list
        :raises PerkError: when specified perk list or perk is incorrect
        """
        if not isinstance(perk_list, PerkList):
            raise PerkList.PerkError("incorrect object type for perk list")
        if isinstance(perk_to_add, Perk):
            PerkListPerkAdder._add_perk(perk_list=perk_list, perk_to_add=perk_to_add)
        else:
            raise PerkList.PerkError("incorrect object type to add to perk list")

    @staticmethod
    def _add_perk(perk_list, perk_to_add):
        """Adds provided perk to specified perk list by appending to list of active perks.

        :param perk_list: PerkList object to add perk to
        :param perk_to_add: Perk derived object to add to perk list
        :raises PerkError: when adding already existing perk
        """
        for perk in perk_list.perks:
            if perk.perk_id == perk_to_add.perk_id:
                raise PerkList.PerkError("can't add already existing perk: {}".format(perk_to_add.name))
        else:
            perk_list.perks.append(perk_to_add)


class PerkListPerkRemover:
    """This class removes perks from specified perk list.

    The class uses PerkList class' PerkError exception, which is raised when removing incorrect perk or specified perk
    list is incorrect.
    """

    @staticmethod
    def remove_perk(perk_list, perk_to_remove):
        """Removes specified perk from specified perk list.

        :param perk_list: PerkList object to remove perk from
        :param perk_to_remove: Perk derived object to remove from perk list
        :raises PerkError: when specified perk list or perk is incorrect
        """
        if not isinstance(perk_list, PerkList):
            raise PerkList.PerkError("incorrect object type for perk list")
        try:
            perk_list.perks.remove(perk_to_remove)
        except ValueError:
            raise PerkList.PerkError("no such perk in perk list")


class PerkListStatusEffectDurationLowerer:
    """This class lowers duration of all status effects in specified perk list.

    The class uses PerkList class' PerkError exception, which is raised when specified perk list is incorrect
    """

    @staticmethod
    def lower_status_effects_duration(perk_list):
        """Lowers duration of status effects in specified perk list.

        :param perk_list: PerkList object to lower duration of status effects in
        :raises PerkError: when specified perk list is incorrect
        """
        if not isinstance(perk_list, PerkList):
            raise PerkList.PerkError("incorrect object type for perk list")
        for perk in perk_list.perks:
            if isinstance(perk, StatusEffect):
                perk.lower_duration()
