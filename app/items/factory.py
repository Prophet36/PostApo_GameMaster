from app.files.file_handler import FileHandler
from app.items.generic import Armor
from app.items.stackables import Ammo, Consumable
from app.items.weapons import MeleeWeapon, RangedWeapon


class ItemFactory:
    """This class is responsible for generating items with their respective parameters based on obtained data.

    The class obtains data on instantiation. Obtained data is a specially formatted text. This text contains list of all
    items (weapons, consumables, etc) with their parameter values for the class to parse in order to create new
    instances of Item derived objects, based on item type.

    The class provides BuildError exception, which is raised whenever object instance can't be properly created due to
    errors existing in obtained data (missing parameter values, incorrect data formatting, etc).
    """

    class BuildError(Exception):
        """This exception class exist to unify all errors and exceptions occurring during item creation."""
        pass

    def __init__(self, data_file="items.txt"):
        """Initializes instance of the class and obtains item data from specified file. Sets data tracking parameters to
        their default None value.

        Data is obtained as a list of lines by FileHandler class. Data tracking parameters are used throughout item
        creation process to track positions of extracted item's ID and its parameters.

        :param data_file: name of the file to obtain data from (defaults to items.txt)
        :raises BuildError: when specified file is not available for data extraction
        """
        try:
            self._data = FileHandler.get_file_contents_as_list(data_file)
        except FileNotFoundError:
            raise ItemFactory.BuildError("Error! Item data is unavailable!")
        else:
            self._line_number_containing_item_id = None
            self._line_number_containing_last_data = None
            self._item_id_to_find = None

    def create_item(self, item_id):
        """Searches for specified item based on its ID and returns instance of Item derived class with parameters
        extracted from previously obtained data.

        :param item_id: ID of the item to find and create
        :return: instance of Item derived class
        :raises BuildError: when specified item ID is not found
        """
        for idx, line in enumerate(self._data):
            if "id:" in line and item_id in line:
                self._line_number_containing_item_id = idx
                self._item_id_to_find = item_id
                return self._create_found_item()
        else:
            raise ItemFactory.BuildError("Error! Can't create {}. Item does not exist!".format(item_id))

    def _create_found_item(self):
        """Extracts previously found item's tags in order to call specific method to create instance of respective Item
        derived class.

        :return: respective instance of Item derived class
        :raises BuildError: when type of item is incorrect (either due to missing or incorrect tags)
        """
        tags = self._get_item_tags()
        self._line_number_containing_last_data = self._line_number_containing_item_id
        if "armor" in tags:
            return self._create_armor()
        elif "melee" in tags:
            return self._create_melee_weapon()
        elif "gun" in tags or "energy" in tags:
            return self._create_ranged_weapon()
        elif "ammo" in tags:
            return self._create_ammo()
        elif "consumable" in tags:
            return self._create_consumable()
        else:
            raise ItemFactory.BuildError("Error! Can't create {}. Incorrect item type!".format(self._item_id_to_find))

    def _get_item_tags(self):
        """Extracts and returns previously found item's tags.

        :return: tags associated with found item
        """
        return self._data[self._line_number_containing_item_id + 1]

    def _create_armor(self):
        """Extracts parameter values and creates instance of Armor class with those parameters.

        :return: instance of Armor class
        :raises BuildError: when extracted data can't be converted due to incorrect parameter value in obtained data
        """
        try:
            item_id = self._get_parameter_value_from_data(parameter_name="id")
            tags = self._get_parameter_value_from_data(parameter_name="tags")
            name = self._get_parameter_value_from_data(parameter_name="name")
            desc = self._get_parameter_value_from_data(parameter_name="description")
            dmg_res = int(self._get_parameter_value_from_data(parameter_name="damage_resistance"))
            rad_res = int(self._get_parameter_value_from_data(parameter_name="radiation_resistance"))
            evasion = int(self._get_parameter_value_from_data(parameter_name="evasion"))
            value = int(self._get_parameter_value_from_data(parameter_name="value"))
            weight = float(self._get_parameter_value_from_data(parameter_name="weight"))
        except ValueError:
            raise ItemFactory.BuildError("Error! Can't create {}. Incorrect item data!".format(self._item_id_to_find))
        else:
            return Armor(item_id, tags, name, desc, dmg_res, rad_res, evasion, value, weight)

    def _create_melee_weapon(self):
        """Extracts parameter values and creates instance of MeleeWeapon class with those parameters.

        :return: instance of MeleeWeapon class
        :raises BuildError: when extracted data can't be converted due to incorrect parameter value in obtained data
        """
        try:
            item_id = self._get_parameter_value_from_data(parameter_name="id")
            tags = self._get_parameter_value_from_data(parameter_name="tags")
            name = self._get_parameter_value_from_data(parameter_name="name")
            desc = self._get_parameter_value_from_data(parameter_name="description")
            damage = self._get_parameter_value_from_data(parameter_name="damage")
            effect = self._get_parameter_value_from_data(parameter_name="effect")
            eff_chance = self._get_parameter_value_from_data(parameter_name="effect_chance")
            armor_pen = int(self._get_parameter_value_from_data(parameter_name="armor_penetration"))
            accuracy = int(self._get_parameter_value_from_data(parameter_name="accuracy"))
            ap_cost = int(self._get_parameter_value_from_data(parameter_name="action_points_cost"))
            st_requirement = int(self._get_parameter_value_from_data(parameter_name="strength_requirement"))
            value = int(self._get_parameter_value_from_data(parameter_name="value"))
            weight = float(self._get_parameter_value_from_data(parameter_name="weight"))
        except ValueError:
            raise ItemFactory.BuildError("Error! Can't create {}. Incorrect item data!".format(self._item_id_to_find))
        else:
            return MeleeWeapon(item_id, tags, name, desc, damage, effect, eff_chance, armor_pen, accuracy, ap_cost,
                               st_requirement, value, weight)

    def _create_ranged_weapon(self):
        """Extracts parameter values and creates instance of RangedWeapon class with those parameters.

        :return: instance of RangedWeapon class
        :raises BuildError: when extracted data can't be converted due to incorrect parameter value in obtained data
        """
        try:
            item_id = self._get_parameter_value_from_data(parameter_name="id")
            tags = self._get_parameter_value_from_data(parameter_name="tags")
            name = self._get_parameter_value_from_data(parameter_name="name")
            desc = self._get_parameter_value_from_data(parameter_name="description")
            damage = self._get_parameter_value_from_data(parameter_name="damage")
            ammo_type = self._get_parameter_value_from_data(parameter_name="ammo_type")
            clip_size = int(self._get_parameter_value_from_data(parameter_name="clip_size"))
            armor_pen = int(self._get_parameter_value_from_data(parameter_name="armor_penetration"))
            accuracy = int(self._get_parameter_value_from_data(parameter_name="accuracy"))
            ap_cost = int(self._get_parameter_value_from_data(parameter_name="action_points_cost"))
            st_requirement = int(self._get_parameter_value_from_data(parameter_name="strength_requirement"))
            value = int(self._get_parameter_value_from_data(parameter_name="value"))
            weight = float(self._get_parameter_value_from_data(parameter_name="weight"))
        except ValueError:
            raise ItemFactory.BuildError("Error! Can't create {}. Incorrect item data!".format(self._item_id_to_find))
        else:
            return RangedWeapon(item_id, tags, name, desc, damage, ammo_type, clip_size, armor_pen, accuracy, ap_cost,
                                st_requirement, value, weight)

    def _create_ammo(self):
        """Extracts parameter values and creates instance of Ammo class with those parameters.

        :return: instance of Ammo class
        :raises BuildError: when extracted data can't be converted due to incorrect parameter value in obtained data
        """
        try:
            item_id = self._get_parameter_value_from_data(parameter_name="id")
            tags = self._get_parameter_value_from_data(parameter_name="tags")
            name = self._get_parameter_value_from_data(parameter_name="name")
            desc = self._get_parameter_value_from_data(parameter_name="description")
            max_stack = int(self._get_parameter_value_from_data(parameter_name="max_stack"))
            current_amount = max_stack
            value = int(self._get_parameter_value_from_data(parameter_name="value"))
            weight = float(self._get_parameter_value_from_data(parameter_name="weight"))
        except ValueError:
            raise ItemFactory.BuildError("Error! Can't create {}. Incorrect item data!".format(self._item_id_to_find))
        else:
            return Ammo(item_id, tags, name, desc, max_stack, current_amount, value, weight)

    def _create_consumable(self):
        """Extracts parameter values and creates instance of Consumable class with those parameters.

        :return: instance of Consumable class
        :raises BuildError: when extracted data can't be converted due to incorrect parameter value in obtained data
        """
        try:
            item_id = self._get_parameter_value_from_data(parameter_name="id")
            tags = self._get_parameter_value_from_data(parameter_name="tags")
            name = self._get_parameter_value_from_data(parameter_name="name")
            desc = self._get_parameter_value_from_data(parameter_name="description")
            effect = self._get_parameter_value_from_data(parameter_name="effect")
            max_stack = int(self._get_parameter_value_from_data(parameter_name="max_stack"))
            current_amount = max_stack
            value = int(self._get_parameter_value_from_data(parameter_name="value"))
            weight = float(self._get_parameter_value_from_data(parameter_name="weight"))
        except ValueError:
            raise ItemFactory.BuildError("Error! Can't create {}. Incorrect item data!".format(self._item_id_to_find))
        else:
            return Consumable(item_id, tags, name, desc, effect, max_stack, current_amount, value, weight)

    def _get_parameter_value_from_data(self, parameter_name):
        """Extracts specified parameter value from obtained data.

        Exception is thrown when name of the parameter is incorrect (either due to missing or incorrect parameter in
        obtained data and incorrect order of parameters).

        :param parameter_name: name of the parameter in obtained data to extract value from
        :return: parameter value
        :raises BuildError: when name of the parameter is incorrect or data is missing (list index out of range)
        """
        try:
            parameter_data = self._data[self._line_number_containing_last_data]
        except IndexError:
            raise ItemFactory.BuildError("Error! Can't create {}. Not enough item data!".format(self._item_id_to_find))
        else:
            if (parameter_name + ":") in parameter_data:
                parameter_value = " ".join(self._data[self._line_number_containing_last_data].split()[1:])
                self._line_number_containing_last_data += 1
                return parameter_value
            else:
                raise ItemFactory.BuildError("Error! Can't create {}. Missing item data!".
                                             format(self._item_id_to_find))
