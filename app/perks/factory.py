from app.files.file_handler import FileHandler
from app.perks.perks import CharacterPerk, PlayerTrait, StatusEffect


class PerkFactory:
    """This class is responsible for generating perks with their respective parameters based on obtained data.

    The class obtains data on instantiation. Obtained data is a specially formatted text, which contains list of all
    perks (including status effects) with their parameter values. The class parses this data in order to create new
    instances of Perk derived objects, based on perk type.

    The class provides PerkBuildError exception, which is raised whenever object instance can't be properly created due
    to errors existing in obtained data (missing parameter values, incorrect data formatting, etc).
    """

    class PerkBuildError(Exception):
        """This exception class exist to unify all errors and exceptions occurring during perk creation."""
        pass

    def __init__(self, data_file="perks.txt"):
        """Initializes instance of the class and obtains perk data from specified file. Sets data tracking parameters to
        their default value.

        Data is obtained as a list of lines by FileHandler class. Data tracking parameters are used throughout perk
        creation process to track positions of extracted perk's ID and its parameters.

        :param data_file: name of the file to obtain data from (defaults to perks.txt)
        :raises PerkBuildError: when specified file is not available for data extraction
        """
        try:
            self._data = FileHandler.get_file_contents_as_list(data_file)
        except FileNotFoundError:
            raise PerkFactory.PerkBuildError("perk data is unavailable")
        else:
            self._line_number_containing_perk_id = None
            self._line_number_containing_last_data = None
            self._perk_id_to_find = None

    def create_perk(self, perk_id):
        """Searches for specified perk based on its ID and returns instance of Perk derived class with parameters
        extracted from previously obtained data.

        :param perk_id: ID of the perk to find and create
        :raises PerkBuildError: when specified perk ID is not found
        :return: Perk derived object
        """
        for idx, line in enumerate(self._data):
            if "id:" in line and line.split()[-1] == perk_id:
                self._line_number_containing_perk_id = idx
                self._perk_id_to_find = perk_id
                return self._create_found_perk()
        else:
            raise PerkFactory.PerkBuildError("incorrect perk ID")

    def _create_found_perk(self):
        """Extracts previously found perk's tags in order to call appropriate method to create instance of respective
        Perk derived class.

        :return: Perk derived object
        :raises PerkBuildError: when type of perk is incorrect (either due to missing or incorrect tags)
        """
        tags = self._get_perk_tags()
        self._line_number_containing_last_data = self._line_number_containing_perk_id
        if "perk" in tags:
            return self._create_perk()
        elif "trait" in tags:
            return self._create_trait()
        elif "status effect" in tags:
            return self._create_status_effect()
        else:
            raise PerkFactory.PerkBuildError("incorrect perk type for perk: {}".format(self._perk_id_to_find))

    def _get_perk_tags(self):
        """Extracts and returns previously found perk's tags.

        :return: tags associated with found perk
        """
        return self._data[self._line_number_containing_perk_id + 1]

    def _create_perk(self):
        """Extracts parameter values and creates instance of CharacterPerk class with those parameters.

        :raises PerkBuildError: when extracted data can't be converted due to incorrect parameter value in obtained data
        :return: CharacterPerk object
        """
        perk_id = self._get_parameter_value_from_data(parameter_name="id")
        tags = self._get_parameter_value_from_data(parameter_name="tags")
        name = self._get_parameter_value_from_data(parameter_name="name")
        desc = self._get_parameter_value_from_data(parameter_name="description")
        effects = self._get_parameter_value_from_data(parameter_name="effects")
        requirements = self._get_parameter_value_from_data(parameter_name="requirements")
        return CharacterPerk(perk_id, tags, name, desc, effects, requirements)

    def _create_trait(self):
        """Extracts parameter values and creates instance of PlayerTrait class with those parameters.

        :raises PerkBuildError: when extracted data can't be converted due to incorrect parameter value in obtained data
        :return: PlayerTrait object
        """
        perk_id = self._get_parameter_value_from_data(parameter_name="id")
        tags = self._get_parameter_value_from_data(parameter_name="tags")
        name = self._get_parameter_value_from_data(parameter_name="name")
        desc = self._get_parameter_value_from_data(parameter_name="description")
        effects = self._get_parameter_value_from_data(parameter_name="effects")
        conflicts = self._get_parameter_value_from_data(parameter_name="conflicts")
        return PlayerTrait(perk_id, tags, name, desc, effects, conflicts)

    def _create_status_effect(self):
        """Extracts parameter values and creates instance of StatusEffect class with those parameters.

        :raises PerkBuildError: when extracted data can't be converted due to incorrect parameter value in obtained data
        :return: StatusEffect object
        """
        try:
            perk_id = self._get_parameter_value_from_data(parameter_name="id")
            tags = self._get_parameter_value_from_data(parameter_name="tags")
            name = self._get_parameter_value_from_data(parameter_name="name")
            desc = self._get_parameter_value_from_data(parameter_name="description")
            effects = self._get_parameter_value_from_data(parameter_name="effects")
            duration = int(self._get_parameter_value_from_data(parameter_name="duration"))
        except ValueError:
            raise PerkFactory.PerkBuildError("incorrect parameter data for perk: {}".format(self._perk_id_to_find))
        else:
            return StatusEffect(perk_id, tags, name, desc, effects, duration)

    def _get_parameter_value_from_data(self, parameter_name):
        """Extracts specified parameter value from obtained data.

        :param parameter_name: name of the parameter in obtained data to extract value from
        :raises PerkBuildError: when name of the parameter is incorrect or data is missing (list index out of range)
        :return: parameter value
        """
        try:
            parameter_data = self._data[self._line_number_containing_last_data]
        except IndexError:
            raise PerkFactory.PerkBuildError("missing perk data for perk: {}".format(self._perk_id_to_find))
        else:
            if (parameter_name + ":") in parameter_data:
                parameter_value = " ".join(self._data[self._line_number_containing_last_data].split()[1:])
                self._line_number_containing_last_data += 1
                return parameter_value
            else:
                raise PerkFactory.PerkBuildError("incorrect parameter name: {} for perk: {}"
                                                 .format(parameter_name, self._perk_id_to_find))
