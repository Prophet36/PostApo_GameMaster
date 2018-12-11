class FileHandler:
    """This class handles file extraction. Methods of this class are static and should be called by other classes
    whenever data extraction is necessary.
    """

    @staticmethod
    def get_file_contents_as_list(file_name):
        """Extracts data from specified file and returns it as list of lines.

        :param file_name: name of the file to extract data from
        :return: list of lines extracted from file
        """
        with open(file_name) as file:
            data = file.read().splitlines()
        return data
