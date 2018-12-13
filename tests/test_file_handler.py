import unittest

from app.files.file_handler import FileHandler


class FileHandlerTests(unittest.TestCase):

    def test_correct_file_name_returns_data(self):
        data = FileHandler.get_file_contents_as_list("test_items_correct.txt")
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_invalid_file_name_raises_exception(self):
        with self.assertRaisesRegex(FileNotFoundError, ".* No such file or directory: .*"):
            FileHandler.get_file_contents_as_list("invalid_file.txt")


if __name__ == "__main__":
    unittest.main()
