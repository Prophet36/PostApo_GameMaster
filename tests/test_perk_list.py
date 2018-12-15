import unittest

from app.mechanics.perk_list import PerkList, PerkListPerkAdder, PerkListPerkRemover
from app.mechanics.perk_list import PerkListStatusEffectDurationLowerer
from app.perks.generic import CharacterPerk, StatusEffect


class PerkListTests(unittest.TestCase):

    def setUp(self):
        self.perks = PerkList()

    def test_property_values(self):
        self.assertIsInstance(self.perks.perks, list)
        self.assertEqual(0, len(self.perks.perks))

    def test_obj_as_str_representation(self):
        correct_str_print = "Perks:\nNone"
        self.assertEqual(correct_str_print, self.perks.__str__())


class PerkListPerkAdderTests(unittest.TestCase):

    def setUp(self):
        self.perks = PerkList()

    def test_add_perk(self):
        perk_to_add = CharacterPerk(perk_id="perk", tags="perk, ap_cost, test", name="Perk", desc="Test perk.",
                                    effects="weapon, short, ap_cost, -1", requirements="attribute, agility, 6")
        self.assertEqual(0, len(self.perks.perks))
        PerkListPerkAdder.add_perk(perk_list=self.perks, perk_to_add=perk_to_add)
        self.assertEqual(1, len(self.perks.perks))
        self.assertIs(perk_to_add, self.perks.perks[0])

    def test_add_already_existing_perk_raises_exception(self):
        perk_to_add = CharacterPerk(perk_id="perk", tags="perk, ap_cost, test", name="Perk", desc="Test perk.",
                                    effects="weapon, short, ap_cost, -1", requirements="attribute, agility, 6")
        PerkListPerkAdder.add_perk(perk_list=self.perks, perk_to_add=perk_to_add)
        with self.assertRaisesRegex(PerkList.PerkError, "can't add already existing perk: .*"):
            PerkListPerkAdder.add_perk(perk_list=self.perks, perk_to_add=perk_to_add)

    def test_add_incorrect_obj_as_perk_raises_exception(self):
        with self.assertRaisesRegex(PerkList.PerkError, "incorrect object type to add to perk list"):
            PerkListPerkAdder.add_perk(perk_list=self.perks, perk_to_add="not Perk derived object")

    def test_incorrect_obj_as_perk_list_raises_exception(self):
        with self.assertRaisesRegex(PerkList.PerkError, "incorrect object type for perk list"):
            PerkListPerkAdder.add_perk(perk_list="not PerkList object", perk_to_add="perk to add")

    def test_perk_list_with_multiple_perks_as_str_representation(self):
        perk = CharacterPerk(perk_id="perk", tags="perk, ap_cost, test", name="Perk", desc="Test perk.",
                             effects="weapon, short, ap_cost, -1", requirements="attribute, agility, 6")
        status_effect = StatusEffect(perk_id="status_effect", tags="status effect, evasion, test", name="Status Effect",
                                     desc="Test status effect.", effects="evasion, 1", duration=1)
        PerkListPerkAdder.add_perk(perk_list=self.perks, perk_to_add=perk)
        PerkListPerkAdder.add_perk(perk_list=self.perks, perk_to_add=status_effect)
        correct_str_print = "Perks:\n1: Perk\n2: Status Effect"
        self.assertEqual(correct_str_print, self.perks.__str__())


class PerkListPerkRemoverTests(unittest.TestCase):

    def setUp(self):
        self.perks = PerkList()

    def test_remove_perk(self):
        perk = CharacterPerk(perk_id="perk", tags="perk, ap_cost, test", name="Perk", desc="Test perk.",
                             effects="weapon, short, ap_cost, -1", requirements="attribute, agility, 6")
        PerkListPerkAdder.add_perk(perk_list=self.perks, perk_to_add=perk)
        self.assertEqual(1, len(self.perks.perks))
        perk_to_remove = self.perks.perks[0]
        PerkListPerkRemover.remove_perk(perk_list=self.perks, perk_to_remove=perk_to_remove)
        self.assertEqual(0, len(self.perks.perks))

    def test_remove_incorrect_perk_raises_exception(self):
        with self.assertRaisesRegex(PerkList.PerkError, "no such perk in perk list"):
            PerkListPerkRemover.remove_perk(perk_list=self.perks, perk_to_remove="incorrect perk")

    def test_incorrect_obj_as_perk_list_raises_exception(self):
        with self.assertRaisesRegex(PerkList.PerkError, "incorrect object type for perk list"):
            PerkListPerkRemover.remove_perk(perk_list="not PerkList object", perk_to_remove="perk to remove")


class PerkListStatusEffectDurationLowererTests(unittest.TestCase):

    def setUp(self):
        self.perks = PerkList()
        perk = CharacterPerk(perk_id="perk", tags="perk, ap_cost, test", name="Perk", desc="Test perk.",
                             effects="weapon, short, ap_cost, -1", requirements="attribute, agility, 6")
        status_effect = StatusEffect(perk_id="status_effect", tags="status effect, evasion, test", name="Status Effect",
                                     desc="Test status effect.", effects="evasion, 1", duration=1)
        another_status_effect = StatusEffect(perk_id="another_status_effect", tags="status effect, evasion, test",
                                             name="Status Effect", desc="Test status effect.", effects="evasion, 1",
                                             duration=-1)
        PerkListPerkAdder.add_perk(perk_list=self.perks, perk_to_add=perk)
        PerkListPerkAdder.add_perk(perk_list=self.perks, perk_to_add=status_effect)
        PerkListPerkAdder.add_perk(perk_list=self.perks, perk_to_add=another_status_effect)

    def test_lower_status_effects_duration(self):
        self.assertEqual(1, self.perks.perks[1].duration)
        self.assertEqual(-1, self.perks.perks[2].duration)
        PerkListStatusEffectDurationLowerer.lower_status_effects_duration(perk_list=self.perks)
        self.assertEqual(0, self.perks.perks[1].duration)
        self.assertEqual(-1, self.perks.perks[2].duration)

    def test_incorrect_obj_as_perk_list_raises_exception(self):
        with self.assertRaisesRegex(PerkList.PerkError, "incorrect object type for perk list"):
            PerkListStatusEffectDurationLowerer.lower_status_effects_duration(perk_list="not PerkList object")


if __name__ == "__main__":
    unittest.main()
