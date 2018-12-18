from app.files.file_handler import FileHandler
from app.characters.characters import Critter
from app.items.factory import ItemFactory
from app.perks.factory import PerkFactory
from app.mechanics.inventory import Inventory, InventoryItemAdder, InventoryItemEquipper
from app.mechanics.perk_inventory import PerkInventory, PerkInventoryPerkAdder


class CritterFactory:
    """This class is responsible for generating critters with their respective parameters, items and perks based on
    obtained data.

    The class obtains data on instantiation. Obtained data is a specially formatted text, which contains list of all
    critters with their parameter values. The class parses this data in order to create new instances of Critter
    objects.

    The class provides CritterBuildError exception, which is raised whenever object instance can't be properly created
    due to errors existing in obtained data (missing parameter values, incorrect data formatting, etc).
    """

    class CritterBuildError(Exception):
        """This exception class exist to unify all errors and exceptions occurring during critter creation."""
        pass

    def __init__(self, data_file="critters.txt", item_data_file="items.txt", perk_data_file="perks.txt"):
        """Initializes instance of the class and obtains critter data from specified file. Sets data tracking parameters
        to their default value.

        Data is obtained as a list of lines by FileHandler class. Data tracking parameters are used throughout critter
        creation process to track positions of extracted critter's ID and its parameters.

        Stores names of item and perk data files, which are used when creating items and perks for critters.

        :param data_file: name of the file to obtain data from (defaults to critters.txt)
        :param item_data_file: name of the file containing item data (defaults to items.txt)
        :param perk_data_file: name of the file containing perk data (defaults to perks.txt)
        :raises CritterBuildError: when specified file is not available for data extraction
        """
        try:
            self._data = FileHandler.get_file_contents_as_list(data_file)
        except FileNotFoundError:
            raise CritterFactory.CritterBuildError("critter data is unavailable")
        else:
            self._line_number_containing_critter_id = None
            self._line_number_containing_last_data = None
            self._critter_id_to_find = None
            self._item_data_file = item_data_file
            self._perk_data_file = perk_data_file

    def create_critter(self, critter_id):
        """Searches for specified critter based on its ID and returns instance of Critter class with parameters
        extracted from previously obtained data.

        :param critter_id: ID of the critter to find and create
        :raises CritterBuildError: when specified critter ID is not found
        :return: Critter object
        """
        for idx, line in enumerate(self._data):
            if "id:" in line and line.split()[-1] == critter_id:
                self._line_number_containing_critter_id = idx
                self._line_number_containing_last_data = self._line_number_containing_critter_id + 1
                self._critter_id_to_find = critter_id
                return self._create_critter()
        else:
            raise CritterFactory.CritterBuildError("incorrect critter ID")

    def _create_critter(self):
        """Extracts parameter values and creates instance of Critter class with those parameters, items and perks.

        :raises CritterBuildError: when extracted data can't be converted due to incorrect parameter value in obtained
                                   data
        :return: Critter object
        """
        try:
            tags = self._get_parameter_value_from_data(parameter_name="tags")
            name = self._get_parameter_value_from_data(parameter_name="name")
            level = int(self._get_parameter_value_from_data(parameter_name="level"))
            strength = int(self._get_parameter_value_from_data(parameter_name="strength"))
            endurance = int(self._get_parameter_value_from_data(parameter_name="endurance"))
            agility = int(self._get_parameter_value_from_data(parameter_name="agility"))
            perception = int(self._get_parameter_value_from_data(parameter_name="perception"))
            intelligence = int(self._get_parameter_value_from_data(parameter_name="intelligence"))
            health_bonus = int(self._get_parameter_value_from_data(parameter_name="health_bonus"))
            exp_award = int(self._get_parameter_value_from_data(parameter_name="exp_award"))
        except ValueError:
            raise CritterFactory.CritterBuildError("incorrect parameter data for critter: {}"
                                                   .format(self._critter_id_to_find))
        else:
            critter = Critter(name, tags, level, strength, endurance, agility, perception, intelligence, health_bonus,
                              exp_award)
            self._create_critter_armor(critter)
            self._create_critter_weapon(critter)
            self._create_critter_perks(critter)
            return critter

    def _create_critter_armor(self, critter):
        """Creates and equips critter armor based on extracted armor ID.

        :param critter: Critter object to add and equip armor
        :raises CritterBuildError: when armor can't be created or equipped
        """
        armor_id = self._get_parameter_value_from_data(parameter_name="armor")
        try:
            armor = ItemFactory(data_file=self._item_data_file).create_item(item_id=armor_id)
            InventoryItemAdder.add_item(inv=critter.inventory, item_to_add=armor)
            InventoryItemEquipper.equip_item(inv=critter.inventory, item_to_equip=critter.inventory.items[0])
        except (ItemFactory.ItemBuildError, Inventory.InventoryError):
            raise CritterFactory.CritterBuildError("can't create armor: {} for critter: {}"
                                                   .format(armor_id, critter.name))

    def _create_critter_weapon(self, critter):
        """Creates and equips critter weapon based on extracted weapon ID.

        :param critter: Critter object to add and equip weapon
        :raises CritterBuildError: when weapon can't be created or equipped
        """
        weapon_id = self._get_parameter_value_from_data(parameter_name="weapon")
        try:
            weapon = ItemFactory(data_file=self._item_data_file).create_item(item_id=weapon_id)
            InventoryItemAdder.add_item(inv=critter.inventory, item_to_add=weapon)
            InventoryItemEquipper.equip_item(inv=critter.inventory, item_to_equip=critter.inventory.items[0])
        except (ItemFactory.ItemBuildError, Inventory.InventoryError):
            raise CritterFactory.CritterBuildError("can't create weapon: {} for critter: {}"
                                                   .format(weapon_id, critter.name))

    def _create_critter_perks(self, critter):
        """Creates and adds critter perks based on extracted perk IDs.

        :param critter: Critter object to add perks for
        :raises CritterBuildError: when perks can't be created or added
        """
        perks = self._get_parameter_value_from_data(parameter_name="perks")
        if perks != "none":
            perks = perks.split(", ")
            for perk_id in perks:
                try:
                    perk = PerkFactory(data_file=self._perk_data_file).create_perk(perk_id=perk_id)
                    PerkInventoryPerkAdder.add_perk(perk_inv=critter.perks, perk_to_add=perk)
                except (PerkFactory.PerkBuildError, PerkInventory.PerkInventoryError):
                    raise CritterFactory.CritterBuildError("can't create perk: {} for critter: {}"
                                                           .format(perk_id, critter.name))

    def _get_parameter_value_from_data(self, parameter_name):
        """Extracts specified parameter value from obtained data.

        :param parameter_name: name of the parameter in obtained data to extract value from
        :raises CritterBuildError: when name of the parameter is incorrect or data is missing (list index out of range)
        :return: parameter value
        """
        try:
            parameter_data = self._data[self._line_number_containing_last_data]
        except IndexError:
            raise CritterFactory.CritterBuildError("missing critter data for critter: {}"
                                                   .format(self._critter_id_to_find))
        else:
            if (parameter_name + ":") in parameter_data:
                parameter_value = " ".join(self._data[self._line_number_containing_last_data].split()[1:])
                self._line_number_containing_last_data += 1
                return parameter_value
            else:
                raise CritterFactory.CritterBuildError("incorrect parameter name: {} for critter: {}"
                                                       .format(parameter_name, self._critter_id_to_find))
