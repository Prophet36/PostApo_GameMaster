import unittest

loader = unittest.TestLoader()

suite = unittest.TestSuite()
suite.addTests(loader.loadTestsFromName("tests.test_characters"))
suite.addTests(loader.loadTestsFromName("tests.test_combat_calculators"))
suite.addTests(loader.loadTestsFromName("tests.test_critter_factory"))
suite.addTests(loader.loadTestsFromName("tests.test_file_handler"))
suite.addTests(loader.loadTestsFromName("tests.test_inventory"))
suite.addTests(loader.loadTestsFromName("tests.test_item_factory"))
suite.addTests(loader.loadTestsFromName("tests.test_items"))
suite.addTests(loader.loadTestsFromName("tests.test_perk_factory"))
suite.addTests(loader.loadTestsFromName("tests.test_perk_inventory"))
suite.addTests(loader.loadTestsFromName("tests.test_perks"))
suite.addTests(loader.loadTestsFromName("tests.test_stat_calculators"))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
