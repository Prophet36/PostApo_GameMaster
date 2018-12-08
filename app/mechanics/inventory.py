from app.items.generic import Item, Armor, Weapon
from app.items.weapons import MeleeWeapon, RangedWeapon


class Inventory:
    """This class represents inventory of items carried and equipped by characters in the game.

    This class contains list of carried items (Item derived objects) as well as currently equipped armor and weapon.

    The class provides InventoryError exception, which is raised when adding objects that are not instances of Item
    derived classes or accessing nonexistent items.
    """

    class InventoryError(Exception):
        """This exception class exist to unify all errors and exceptions occurring during inventory manipulation."""
        pass

    def __init__(self, armor, weapon, items=None):
        """Initializes instance of the class while adding provided armor, weapon and optional items to inventory.

        Provided armor and weapon must be Armor and Weapon derived objects, respectively. Optional items can also be
        provided (as a single, list or tuple of Item derived objects).

        :param armor: armor to be equipped, as Armor object
        :param weapon: weapon to be equipped, as Weapon derived object
        :param items: item(s) to be carried, as single, list or tuple of Item derived objects
        :raises InventoryError: when provided armor or weapon is of incorrect type
        """
        if isinstance(armor, Armor) and (isinstance(weapon, MeleeWeapon) or isinstance(weapon, RangedWeapon)):
            self._equipped_armor = armor
            self._equipped_weapon = weapon
        else:
            raise Inventory.InventoryError("Error! Incorrect object type(s) to create inventory with!")
        self._items = list()
        if items is not None:
            if isinstance(items, list) or isinstance(items, tuple):
                for item in items:
                    self.add_item(item)
            else:
                self.add_item(items)

    @property
    def equipped_armor(self):
        """Gets equipped armor as Armor object.

        :return: Armor object representing equipped armor
        """
        return self._equipped_armor

    @equipped_armor.setter
    def equipped_armor(self, armor_to_equip):
        """Sets equipped armor to provided object or none.

        :param armor_to_equip: Armor object to equip
        :raises InventoryError: when provided object type is incorrect
        """
        if isinstance(armor_to_equip, Armor) or armor_to_equip is None:
            self._equipped_armor = armor_to_equip
        else:
            raise Inventory.InventoryError("Error! Incorrect object type to equip!")

    @property
    def equipped_weapon(self):
        """Gets equipped weapon as Weapon derived object.

        :return: Weapon derived object representing equipped weapon
        """
        return self._equipped_weapon

    @equipped_weapon.setter
    def equipped_weapon(self, weapon_to_equip):
        """Sets equipped weapon to provided object or none.

        :param weapon_to_equip: Weapon derived object to equip
        :raises InventoryError: when provided object type is incorrect
        """
        if isinstance(weapon_to_equip, Weapon) or weapon_to_equip is None:
            self._equipped_weapon = weapon_to_equip
        else:
            raise Inventory.InventoryError("Error! Incorrect object type to equip!")

    @property
    def items(self):
        """Gets a list of carried items, as list of Item derived object.

        :return: list of Item derived objects representing carried items
        """
        return self._items

    def add_item(self, item_to_add):
        """Adds provided item to inventory's list of carried items.

        :param item_to_add: Item derived object to add to inventory
        :raises InventoryError: when provided item is of incorrect type
        """
        if isinstance(item_to_add, Item):
            self._items.append(item_to_add)
        else:
            raise Inventory.InventoryError("Error! Incorrect object type to add to inventory!")

    def remove_item(self, item_to_remove):
        """Removes specified item from inventory's list of carried items.

        Item can be chosen either as a reference to particular Item derived object, or index of list of Item derived
        objects.

        :param item_to_remove: reference to Item derived object or index of list of carried items
        """
        if isinstance(item_to_remove, int):
            self._remove_item_by_index(item_index=item_to_remove)
        else:
            self._remove_item_by_reference(item_reference=item_to_remove)

    def _remove_item_by_index(self, item_index):
        """Removes item from inventory's list of carried items at specified index.

        :param item_index: index of list to remove item from
        :raises InventoryError: when specified index is incorrect
        """
        try:
            self._items.pop(item_index)
        except IndexError:
            raise Inventory.InventoryError("Error! Incorrect inventory index!")

    def _remove_item_by_reference(self, item_reference):
        """Removes specified item from inventory's list of carried items by passed reference.

        Items can only be removed from list of carried items, equipped armor and weapon can't be removed.

        :param item_reference: reference of Item derived object in inventory to remove
        :raises InventoryError: when passed reference is incorrect (either this item is not in inventory, or reference
                                to equipped armor or weapon is passed)
        """
        if item_reference == self._equipped_armor or item_reference == self._equipped_weapon:
            raise Inventory.InventoryError("Error! Can't remove currently equipped item!")
        else:
            try:
                self._items.remove(item_reference)
            except ValueError:
                raise Inventory.InventoryError("Error! This item does not exist in inventory!")

    def __str__(self):
        str_representation = "Armor: {}\nWeapon: {}".format(self._equipped_armor.name, self._equipped_weapon.name)
        if len(self._items) > 0:
            str_representation += "\nItems:"
            for idx, item in enumerate(self._items):
                str_representation += "\n{}: {}".format(idx + 1, item.name)
        return str_representation


class InventoryEquipper:
    """This class equips armor and weapons in specified inventory.

    Items can only be equipped from within specified inventory, and currently equipped item will then swap places with
    specified item to be equipped (from equipped slot to a list of carried items).

    The class uses Inventory class' InventoryError exception, which is raised when equipping incorrect item type,
    equipping item not existing in specified inventory or specified inventory is incorrect.
    """

    @staticmethod
    def equip_item(inventory, item_to_equip):
        """Equips specified item in specified inventory.

        Specified inventory must be an instance of Inventory class, and item to equip must be Armor or Weapon derived
        class object (for equipping armor and weapon respectively).

        :param inventory: Inventory object to equip item in
        :param item_to_equip: Armor or Weapon derived object to equip
        :raises InventoryError: when specified inventory or item to equip is incorrect
        """
        if not isinstance(inventory, Inventory):
            raise Inventory.InventoryError("Error! Specified inventory is incorrect!")
        if isinstance(item_to_equip, Armor):
            InventoryEquipper._equip_armor(inventory, item_to_equip)
        elif isinstance(item_to_equip, Weapon):
            InventoryEquipper._equip_weapon(inventory, item_to_equip)
        else:
            raise Inventory.InventoryError("Error! Can't equip this type of item!")

    @staticmethod
    def _equip_armor(inventory, armor_to_equip):
        """Equips specified armor in specified inventory.

        Specified armor must be in inventory's list of carried items to be equipped.

        :param inventory: Inventory object to equip armor in
        :param armor_to_equip: Armor object to equip
        :raises InventoryError: when specified armor to equip is not in inventory
        """
        if armor_to_equip not in inventory.items:
            raise Inventory.InventoryError("Error! This item does not exist in inventory!")
        else:
            idx = inventory.items.index(armor_to_equip)
            inventory.items[idx], inventory.equipped_armor = inventory.equipped_armor, inventory.items[idx]

    @staticmethod
    def _equip_weapon(inventory, weapon_to_equip):
        """Equips specified weapon in specified inventory.

        Specified weapon must be in inventory's list of carried items to be equipped.

        :param inventory: Inventory object to equip weapon in
        :param weapon_to_equip: Weapon derived object to equip
        :raises InventoryError: when specified weapon to equip is not in inventory
        """
        if weapon_to_equip not in inventory.items:
            raise Inventory.InventoryError("Error! This item does not exist in inventory!")
        else:
            idx = inventory.items.index(weapon_to_equip)
            inventory.items[idx], inventory.equipped_weapon = inventory.equipped_weapon, inventory.items[idx]


class InventoryUnequipper:
    """This class unequips armor and weapons in specified inventory.

    Items that are unequipped are moving to inventory's list of carried items.

    The class uses Inventory class' InventoryError exception, which is raised when specified inventory is incorrect or
    items are already unequipped.
    """

    @staticmethod
    def unequip_armor(inventory):
        """Unequips armor in specified inventory and moves it to inventory's list of carried items.

        :param inventory: Inventory object to unequip armor in
        :raises InventoryError: when specified inventory is incorrect, or armor is already unequipped
        """
        if not isinstance(inventory, Inventory):
            raise Inventory.InventoryError("Error! Specified inventory is incorrect!")
        if inventory.equipped_armor is None:
            raise Inventory.InventoryError("Error! Can't unequip that!")
        inventory.items.append(inventory.equipped_armor)
        inventory.equipped_armor = None

    @staticmethod
    def unequip_weapon(inventory):
        """Unequips weapon in specified inventory and moves it to inventory's list of carried items.

        :param inventory: Inventory object to unequip armor in
        :raises InventoryError: when specified inventory is incorrect, or weapon is already unequipped
        """
        if not isinstance(inventory, Inventory):
            raise Inventory.InventoryError("Error! Specified inventory is incorrect!")
        if inventory.equipped_weapon is None:
            raise Inventory.InventoryError("Error! Can't unequip that!")
        inventory.items.append(inventory.equipped_weapon)
        inventory.equipped_weapon = None
