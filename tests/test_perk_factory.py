import unittest

from app.perks.factory import PerkFactory
from app.perks.perks import CharacterPerk, PlayerTrait, StatusEffect


class PerkFactoryTests(unittest.TestCase):

    def test_invalid_perk_data_raises_exception(self):
        with self.assertRaisesRegex(PerkFactory.PerkBuildError, "perk data is unavailable"):
            PerkFactory(data_file="invalid_file.txt")

    def test_create_character_perk(self):
        perk = PerkFactory(data_file="test_perks_correct.txt").create_perk("perk")
        self.assertIsInstance(perk, CharacterPerk)
        self.assertEqual("perk", perk.perk_id)
        self.assertEqual("perk, ap_cost, test", perk.tags)
        self.assertEqual("Perk", perk.name)
        self.assertEqual("Test perk.", perk.desc)
        self.assertEqual("weapon, short, ap_cost, -1", perk.effects)
        self.assertEqual("attribute, agility, 6", perk.requirements)

    def test_create_player_trait(self):
        trait = PerkFactory(data_file="test_perks_correct.txt").create_perk("trait")
        self.assertIsInstance(trait, PlayerTrait)
        self.assertEqual("trait", trait.perk_id)
        self.assertEqual("trait, attribute, test", trait.tags)
        self.assertEqual("Trait", trait.name)
        self.assertEqual("Test trait.", trait.desc)
        self.assertEqual("attribute, strength, -1; attribute, agility, 1", trait.effects)
        self.assertEqual("conflicting_trait", trait.conflicts)

    def test_create_status_effect(self):
        status_effect = PerkFactory(data_file="test_perks_correct.txt").create_perk("status_effect")
        self.assertIsInstance(status_effect, StatusEffect)
        self.assertEqual("status_effect", status_effect.perk_id)
        self.assertEqual("status effect, evasion, test", status_effect.tags)
        self.assertEqual("Status Effect", status_effect.name)
        self.assertEqual("Test status effect.", status_effect.desc)
        self.assertEqual("evasion, 1", status_effect.effects)
        self.assertEqual(1, status_effect.duration)

    def test_invalid_perk_id_raises_exception(self):
        with self.assertRaisesRegex(PerkFactory.PerkBuildError, "incorrect perk ID"):
            PerkFactory(data_file="test_perks_correct.txt").create_perk(perk_id="invalid_id")

    def test_incorrect_perk_type_raises_exception(self):
        with self.assertRaisesRegex(PerkFactory.PerkBuildError, "incorrect perk type for perk: .*"):
            PerkFactory(data_file="test_perks_incorrect.txt").create_perk(perk_id="incorrect_perk")

    def test_incorrect_perk_data_raises_exception(self):
        with self.assertRaisesRegex(PerkFactory.PerkBuildError, "incorrect parameter data for perk: .*"):
            PerkFactory(data_file="test_perks_incorrect.txt").create_perk(perk_id="incorrect_status_effect")

    def test_missing_perk_data_raises_exception(self):
        with self.assertRaisesRegex(PerkFactory.PerkBuildError, "incorrect parameter name: .* for perk: .*"):
            PerkFactory(data_file="test_perks_incorrect.txt").create_perk(perk_id="incorrect_trait")

    def test_missing_perk_data_due_to_end_of_file_raises_exception(self):
        with self.assertRaisesRegex(PerkFactory.PerkBuildError, "missing perk data for perk: .*"):
            PerkFactory(data_file="test_perks_incorrect.txt").create_perk(perk_id="another_incorrect_status_effect")


if __name__ == "__main__":
    unittest.main()
