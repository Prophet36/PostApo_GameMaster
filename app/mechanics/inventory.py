from app.items.generic import Item, Armor, Weapon
from app.items.stackables import Stackable
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

    def __init__(self, armor, weapon):
        """Initializes instance of the class with provided armor and weapon as default equipped items.

        Provided armor and weapon must be Armor and Weapon derived objects, respectively.

        :param armor: armor to be equipped, as Armor object
        :param weapon: weapon to be equipped, as Weapon derived object
        :raises InventoryError: when provided armor or weapon object is of incorrect type
        """
        if isinstance(armor, Armor) and (isinstance(weapon, MeleeWeapon) or isinstance(weapon, RangedWeapon)):
            self._equipped_armor = armor
            self._equipped_weapon = weapon
        else:
            raise Inventory.InventoryError("Error! Incorrect object type(s) to create inventory with!")
        self._items = list()

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
        :raises InventoryError: when provided object is incorrect
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

    def __str__(self):
        str_representation = "Armor: {}\nWeapon: {}\nItems:".format(self._equipped_armor.name,
                                                                    self._equipped_weapon.name)
        if len(self._items) > 0:
            for idx, item in enumerate(self._items):
                str_representation += "\n{}: {}".format(idx + 1, item.name)
        else:
            str_representation += "\nNone"
        return str_representation


class InventoryItemAdder:
    """This class adds items to specified inventory.

    The class uses Inventory class' InventoryError exception, which is raised when adding incorrect item type or
    specified inventory is incorrect.
    """

    @staticmethod
    def add_item(inv, item_to_add):
        """Adds provided item to specified inventory's list of carried items.

        :param inv: Inventory object to add item in
        :param item_to_add: Item derived object to add to inventory
        :raises InventoryError: when specified inventory or item is incorrect
        """
        if not isinstance(inv, Inventory):
            raise Inventory.InventoryError("Error! Specified inventory is incorrect!")
        if isinstance(item_to_add, Item):
            item_to_add_id = item_to_add.item_id
            if isinstance(item_to_add, Stackable):
                InventoryItemAdder._add_stackable(inv=inv, stackable_to_add=item_to_add, stackable_id=item_to_add_id)
            else:
                InventoryItemAdder._add_item(inv=inv, item_to_add=item_to_add)

        else:
            raise Inventory.InventoryError("Error! Incorrect object type to add to inventory!")

    @staticmethod
    def _add_stackable(inv, stackable_to_add, stackable_id):
        """Adds provided stackable item to specified inventory's list of carried items.

        Stackables are added by first checking if there are already stackables of the same type in inventory in order to
        merge or fill existing stacks, if possible. For example, already having 2 / 5 of one stackable item and adding
        additional 1 / 5 of the same item will result in one stack with 3 / 5, instead of two stacks. In another
        example, having 3 / 5 of some item and adding 4 / 5 will result in filling original stack to 5 / 5 and leaving
        the rest 2 / 5 in the other.

        :param inv: Inventory object to add stackable item to
        :param stackable_to_add: Stackable derived object to add to inventory
        :param stackable_id: ID of the stackable item
        """
        for item in inv.items:
            if item.item_id == stackable_id:
                available_amount = item.max_stack - item.current_amount
                if available_amount >= stackable_to_add.current_amount:
                    item.current_amount += stackable_to_add.current_amount
                    break
                else:
                    item.current_amount = item.max_stack
                    stackable_to_add.current_amount -= available_amount
        else:
            InventoryItemAdder._add_item(inv=inv, item_to_add=stackable_to_add)

    @staticmethod
    def _add_item(inv, item_to_add):
        """Adds provided item to specified inventory by appending to list of carried items.

        :param inv: Inventory object to add item to
        :param item_to_add: Item derived object to add to inventory's list of carried items
        """
        inv.items.append(item_to_add)


class InventoryItemRemover:
    """This class removes items from specified inventory.

    Items are removed by passing its reference. Only items in inventory's list of carried items can be removed.

    The class uses Inventory class' InventoryError exception, which is raised when removing incorrect item or
    specified inventory is incorrect.
    """

    @staticmethod
    def remove_item(inv, item_to_remove):
        """Removes specified item from specified inventory's list of carried items.

        :param inv: Inventory object to remove item from
        :param item_to_remove: reference to Item derived object to remove from inventory
        :raises InventoryError: when specified inventory or item is incorrect
        """
        if not isinstance(inv, Inventory):
            raise Inventory.InventoryError("Error! Specified inventory is incorrect!")
        try:
            inv.items.remove(item_to_remove)
        except ValueError:
            raise Inventory.InventoryError("Error! This item does not exist in inventory!")


class InventoryItemEquipper:
    """This class equips armor and weapons in specified inventory.

    Items can only be equipped from within specified inventory, and currently equipped item will then swap places with
    specified item to be equipped (from equipped slot to a list of carried items).

    The class uses Inventory class' InventoryError exception, which is raised when equipping incorrect item type,
    equipping item not existing in specified inventory or specified inventory is incorrect.
    """

    @staticmethod
    def equip_item(inv, item_to_equip):
        """Equips specified item in specified inventory.

        Specified inventory must be an instance of Inventory class, and item to equip must be Armor or Weapon derived
        class object (for equipping armor and weapon respectively).

        :param inv: Inventory object to equip item in
        :param item_to_equip: Armor or Weapon derived object to equip
        :raises InventoryError: when specified inventory or item to equip is incorrect
        """
        if not isinstance(inv, Inventory):
            raise Inventory.InventoryError("Error! Specified inventory is incorrect!")
        if isinstance(item_to_equip, Armor):
            InventoryItemEquipper._equip_armor(inv, item_to_equip)
        elif isinstance(item_to_equip, Weapon):
            InventoryItemEquipper._equip_weapon(inv, item_to_equip)
        else:
            raise Inventory.InventoryError("Error! Can't equip this type of item!")

    @staticmethod
    def _equip_armor(inv, armor_to_equip):
        """Equips specified armor in specified inventory.

        Specified armor must be in inventory's list of carried items to be equipped.

        :param inv: Inventory object to equip armor in
        :param armor_to_equip: Armor object to equip
        :raises InventoryError: when specified armor to equip is not in inventory
        """
        if armor_to_equip not in inv.items:
            raise Inventory.InventoryError("Error! This item does not exist in inventory!")
        else:
            idx = inv.items.index(armor_to_equip)
            inv.items[idx], inv.equipped_armor = inv.equipped_armor, inv.items[idx]

    @staticmethod
    def _equip_weapon(inv, weapon_to_equip):
        """Equips specified weapon in specified inventory.

        Specified weapon must be in inventory's list of carried items to be equipped.

        :param inv: Inventory object to equip weapon in
        :param weapon_to_equip: Weapon derived object to equip
        :raises InventoryError: when specified weapon to equip is not in inventory
        """
        if weapon_to_equip not in inv.items:
            raise Inventory.InventoryError("Error! This item does not exist in inventory!")
        else:
            idx = inv.items.index(weapon_to_equip)
            inv.items[idx], inv.equipped_weapon = inv.equipped_weapon, inv.items[idx]


class InventoryItemUnequipper:
    """This class unequips armor and weapons in specified inventory.

    Items that are unequipped are moving to inventory's list of carried items.

    The class uses Inventory class' InventoryError exception, which is raised when specified inventory is incorrect or
    items are already unequipped.
    """

    @staticmethod
    def unequip_armor(inv):
        """Unequips armor in specified inventory and moves it to inventory's list of carried items.

        :param inv: Inventory object to unequip armor in
        :raises InventoryError: when specified inventory is incorrect, or armor is already unequipped
        """
        if not isinstance(inv, Inventory):
            raise Inventory.InventoryError("Error! Specified inventory is incorrect!")
        if inv.equipped_armor is None:
            raise Inventory.InventoryError("Error! Can't unequip that!")
        inv.items.append(inv.equipped_armor)
        inv.equipped_armor = None

    @staticmethod
    def unequip_weapon(inv):
        """Unequips weapon in specified inventory and moves it to inventory's list of carried items.

        :param inv: Inventory object to unequip armor in
        :raises InventoryError: when specified inventory is incorrect, or weapon is already unequipped
        """
        if not isinstance(inv, Inventory):
            raise Inventory.InventoryError("Error! Specified inventory is incorrect!")
        if inv.equipped_weapon is None:
            raise Inventory.InventoryError("Error! Can't unequip that!")
        inv.items.append(inv.equipped_weapon)
        inv.equipped_weapon = None
