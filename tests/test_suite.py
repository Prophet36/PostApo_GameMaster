import unittest

import tests.test_file_handler
import tests.test_inventory
import tests.test_item_factory
import tests.test_items

loader = unittest.TestLoader()

suite = unittest.TestSuite()
suite.addTests(loader.loadTestsFromModule(tests.test_file_handler))
suite.addTests(loader.loadTestsFromModule(tests.test_item_factory))
suite.addTests(loader.loadTestsFromModule(tests.test_items))
suite.addTests(loader.loadTestsFromModule(tests.test_inventory))


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)