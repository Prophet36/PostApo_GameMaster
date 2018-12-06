import unittest

import tests.test_file_handler
import tests.test_item_factory
import tests.test_items

loader = unittest.TestLoader()

items_suite = unittest.TestSuite()
items_suite.addTests(loader.loadTestsFromModule(tests.test_file_handler))
items_suite.addTests(loader.loadTestsFromModule(tests.test_item_factory))
items_suite.addTests(loader.loadTestsFromModule(tests.test_items))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(items_suite)
