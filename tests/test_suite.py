import unittest

import tests.test_characters
import tests.test_critter_factory
import tests.test_file_handler
import tests.test_inventory
import tests.test_item_factory
import tests.test_items
import tests.test_perk_factory
import tests.test_perk_inventory
import tests.test_perks
import tests.test_stat_calculators

loader = unittest.TestLoader()

suite = unittest.TestSuite()
suite.addTests(loader.loadTestsFromModule(tests.test_characters))
suite.addTests(loader.loadTestsFromModule(tests.test_critter_factory))
suite.addTests(loader.loadTestsFromModule(tests.test_file_handler))
suite.addTests(loader.loadTestsFromModule(tests.test_inventory))
suite.addTests(loader.loadTestsFromModule(tests.test_item_factory))
suite.addTests(loader.loadTestsFromModule(tests.test_items))
suite.addTests(loader.loadTestsFromModule(tests.test_perk_factory))
suite.addTests(loader.loadTestsFromModule(tests.test_perk_inventory))
suite.addTests(loader.loadTestsFromModule(tests.test_perks))
suite.addTests(loader.loadTestsFromModule(tests.test_stat_calculators))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
