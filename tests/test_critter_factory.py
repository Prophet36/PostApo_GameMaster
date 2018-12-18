import unittest

from app.characters.characters import Critter
from app.characters.factory import CritterFactory
from app.items.items import Armor
from app.items.weapons import MeleeWeapon


class CritterFactoryTests(unittest.TestCase):

    def test_invalid_critter_data_raises_exception(self):
        with self.assertRaisesRegex(CritterFactory.CritterBuildError, "critter data is unavailable"):
            CritterFactory(data_file="invalid_file.txt")

    def test_create_critter(self):
        critter = CritterFactory(data_file="test_critters_correct.txt", item_data_file="test_items_correct.txt",
                                 perk_data_file="test_perks_correct.txt").create_critter(critter_id="critter")
        self.assertIsInstance(critter, Critter)
        self.assertEqual("Critter", critter.name)
        self.assertEqual("critter, test", critter.tags)
        self.assertEqual(1, critter.level)
        self.assertEqual(5, critter.strength)
        self.assertEqual(5, critter.endurance)
        self.assertEqual(5, critter.agility)
        self.assertEqual(5, critter.perception)
        self.assertEqual(5, critter.intelligence)
        self.assertEqual(10, critter.health_bonus)
        self.assertEqual(10, critter.experience_award)
        self.assertIsInstance(critter.inventory.equipped_armor, Armor)
        self.assertIsInstance(critter.inventory.equipped_weapon, MeleeWeapon)

    def test_create_critter_with_no_perks(self):
        critter = CritterFactory(data_file="test_critters_correct.txt", item_data_file="test_items_correct.txt",
                                 perk_data_file="test_perks_correct.txt").create_critter(critter_id="another_critter")
        self.assertIsInstance(critter, Critter)
        self.assertEqual("Critter", critter.name)
        self.assertEqual("critter, test", critter.tags)
        self.assertEqual(1, critter.level)
        self.assertEqual(5, critter.strength)
        self.assertEqual(5, critter.endurance)
        self.assertEqual(5, critter.agility)
        self.assertEqual(5, critter.perception)
        self.assertEqual(5, critter.intelligence)
        self.assertEqual(10, critter.health_bonus)
        self.assertEqual(10, critter.experience_award)
        self.assertIsInstance(critter.inventory.equipped_armor, Armor)
        self.assertIsInstance(critter.inventory.equipped_weapon, MeleeWeapon)
        self.assertEqual(0, len(critter.perks.perks))
    
    def test_invalid_critter_id_raises_exception(self):
        with self.assertRaisesRegex(CritterFactory.CritterBuildError, "incorrect critter ID"):
            CritterFactory(data_file="test_critters_correct.txt", item_data_file="test_items_correct.txt",
                           perk_data_file="test_perks_correct.txt").create_critter(critter_id="invalid_id")

    def test_incorrect_critter_data_raises_exception(self):
        with self.assertRaisesRegex(CritterFactory.CritterBuildError, "incorrect parameter data for critter: .*"):
            CritterFactory(data_file="test_critters_incorrect.txt", item_data_file="test_items_correct.txt",
                           perk_data_file="test_perks_correct.txt").create_critter(critter_id="incorrect_critter")

    def test_missing_critter_data_raises_exception(self):
        with self.assertRaisesRegex(CritterFactory.CritterBuildError, "incorrect parameter name: .* for critter: .*"):
            CritterFactory(data_file="test_critters_incorrect.txt", item_data_file="test_items_correct.txt",
                           perk_data_file="test_perks_correct.txt").create_critter(
                critter_id="another_incorrect_critter")

    def test_missing_critter_data_due_to_end_of_file_raises_exception(self):
        with self.assertRaisesRegex(CritterFactory.CritterBuildError, "missing critter data for critter: .*"):
            CritterFactory(data_file="test_critters_incorrect.txt", item_data_file="test_items_correct.txt",
                           perk_data_file="test_perks_correct.txt").create_critter(
                critter_id="yet_another_incorrect_critter")

    def test_incorrect_critter_armor_raises_exception(self):
        with self.assertRaisesRegex(CritterFactory.CritterBuildError, "can't create armor: .* for critter: .*"):
            CritterFactory(data_file="test_critters_incorrect.txt", item_data_file="test_items_correct.txt",
                           perk_data_file="test_perks_correct.txt").create_critter(
                critter_id="critter_with_incorrect_armor")

    def test_incorrect_critter_weapon_raises_exception(self):
        with self.assertRaisesRegex(CritterFactory.CritterBuildError, "can't create weapon: .* for critter: .*"):
            CritterFactory(data_file="test_critters_incorrect.txt", item_data_file="test_items_correct.txt",
                           perk_data_file="test_perks_correct.txt").create_critter(
                critter_id="critter_with_incorrect_weapon")

    def test_incorrect_critter_perk_raises_exception(self):
        with self.assertRaisesRegex(CritterFactory.CritterBuildError, "can't create perk: .* for critter: .*"):
            CritterFactory(data_file="test_critters_incorrect.txt", item_data_file="test_items_correct.txt",
                           perk_data_file="test_perks_correct.txt").create_critter(
                critter_id="critter_with_incorrect_perk")


if __name__ == "__main__":
    unittest.main()
