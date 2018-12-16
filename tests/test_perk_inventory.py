import unittest

from app.mechanics.perk_inventory import PerkInventory, PerkInventoryPerkAdder, PerkInventoryPerkRemover
from app.mechanics.perk_inventory import PerkInventoryStatusEffectDurationLowerer
from app.perks.perks import CharacterPerk, StatusEffect


class PerkListTests(unittest.TestCase):

    def setUp(self):
        self.perk_inventory = PerkInventory()

    def test_property_values(self):
        self.assertIsInstance(self.perk_inventory.perks, list)
        self.assertEqual(0, len(self.perk_inventory.perks))

    def test_obj_as_str_representation(self):
        correct_str_print = "Perks:\nNone"
        self.assertEqual(correct_str_print, self.perk_inventory.__str__())


class PerkListPerkAdderTests(unittest.TestCase):

    def setUp(self):
        self.perk_inventory = PerkInventory()

    def test_add_perk(self):
        perk_to_add = CharacterPerk(perk_id="perk", tags="perk, ap_cost, test", name="Perk", desc="Test perk.",
                                    effects="weapon, short, ap_cost, -1", requirements="attribute, agility, 6")
        self.assertEqual(0, len(self.perk_inventory.perks))
        PerkInventoryPerkAdder.add_perk(perk_inv=self.perk_inventory, perk_to_add=perk_to_add)
        self.assertEqual(1, len(self.perk_inventory.perks))
        self.assertIs(perk_to_add, self.perk_inventory.perks[0])

    def test_add_already_existing_perk_raises_exception(self):
        perk_to_add = CharacterPerk(perk_id="perk", tags="perk, ap_cost, test", name="Perk", desc="Test perk.",
                                    effects="weapon, short, ap_cost, -1", requirements="attribute, agility, 6")
        PerkInventoryPerkAdder.add_perk(perk_inv=self.perk_inventory, perk_to_add=perk_to_add)
        with self.assertRaisesRegex(PerkInventory.PerkInventoryError, "can't add already existing perk: .*"):
            PerkInventoryPerkAdder.add_perk(perk_inv=self.perk_inventory, perk_to_add=perk_to_add)

    def test_add_incorrect_obj_as_perk_raises_exception(self):
        with self.assertRaisesRegex(PerkInventory.PerkInventoryError, "incorrect object type to add to perk list"):
            PerkInventoryPerkAdder.add_perk(perk_inv=self.perk_inventory, perk_to_add="not Perk derived object")

    def test_incorrect_obj_as_perk_list_raises_exception(self):
        with self.assertRaisesRegex(PerkInventory.PerkInventoryError, "incorrect object type for perk list"):
            PerkInventoryPerkAdder.add_perk(perk_inv="not PerkList object", perk_to_add="perk to add")

    def test_perk_list_with_multiple_perks_as_str_representation(self):
        perk = CharacterPerk(perk_id="perk", tags="perk, ap_cost, test", name="Perk", desc="Test perk.",
                             effects="weapon, short, ap_cost, -1", requirements="attribute, agility, 6")
        status_effect = StatusEffect(perk_id="status_effect", tags="status effect, evasion, test", name="Status Effect",
                                     desc="Test status effect.", effects="evasion, 1", duration=1)
        PerkInventoryPerkAdder.add_perk(perk_inv=self.perk_inventory, perk_to_add=perk)
        PerkInventoryPerkAdder.add_perk(perk_inv=self.perk_inventory, perk_to_add=status_effect)
        correct_str_print = "Perks:\n1: Perk\n2: Status Effect"
        self.assertEqual(correct_str_print, self.perk_inventory.__str__())


class PerkListPerkRemoverTests(unittest.TestCase):

    def setUp(self):
        self.perk_inventory = PerkInventory()

    def test_remove_perk(self):
        perk = CharacterPerk(perk_id="perk", tags="perk, ap_cost, test", name="Perk", desc="Test perk.",
                             effects="weapon, short, ap_cost, -1", requirements="attribute, agility, 6")
        PerkInventoryPerkAdder.add_perk(perk_inv=self.perk_inventory, perk_to_add=perk)
        self.assertEqual(1, len(self.perk_inventory.perks))
        perk_to_remove = self.perk_inventory.perks[0]
        PerkInventoryPerkRemover.remove_perk(perk_inv=self.perk_inventory, perk_to_remove=perk_to_remove)
        self.assertEqual(0, len(self.perk_inventory.perks))

    def test_remove_incorrect_perk_raises_exception(self):
        with self.assertRaisesRegex(PerkInventory.PerkInventoryError, "no such perk in perk list"):
            PerkInventoryPerkRemover.remove_perk(perk_inv=self.perk_inventory, perk_to_remove="incorrect perk")

    def test_incorrect_obj_as_perk_list_raises_exception(self):
        with self.assertRaisesRegex(PerkInventory.PerkInventoryError, "incorrect object type for perk list"):
            PerkInventoryPerkRemover.remove_perk(perk_inv="not PerkList object", perk_to_remove="perk to remove")


class PerkListStatusEffectDurationLowererTests(unittest.TestCase):

    def setUp(self):
        self.perk_inventory = PerkInventory()
        perk = CharacterPerk(perk_id="perk", tags="perk, ap_cost, test", name="Perk", desc="Test perk.",
                             effects="weapon, short, ap_cost, -1", requirements="attribute, agility, 6")
        status_effect = StatusEffect(perk_id="status_effect", tags="status effect, evasion, test", name="Status Effect",
                                     desc="Test status effect.", effects="evasion, 1", duration=1)
        another_status_effect = StatusEffect(perk_id="another_status_effect", tags="status effect, evasion, test",
                                             name="Status Effect", desc="Test status effect.", effects="evasion, 1",
                                             duration=-1)
        PerkInventoryPerkAdder.add_perk(perk_inv=self.perk_inventory, perk_to_add=perk)
        PerkInventoryPerkAdder.add_perk(perk_inv=self.perk_inventory, perk_to_add=status_effect)
        PerkInventoryPerkAdder.add_perk(perk_inv=self.perk_inventory, perk_to_add=another_status_effect)

    def test_lower_status_effects_duration(self):
        self.assertEqual(1, self.perk_inventory.perks[1].duration)
        self.assertEqual(-1, self.perk_inventory.perks[2].duration)
        PerkInventoryStatusEffectDurationLowerer.lower_status_effects_duration(perk_inv=self.perk_inventory)
        self.assertEqual(0, self.perk_inventory.perks[1].duration)
        self.assertEqual(-1, self.perk_inventory.perks[2].duration)

    def test_incorrect_obj_as_perk_list_raises_exception(self):
        with self.assertRaisesRegex(PerkInventory.PerkInventoryError, "incorrect object type for perk list"):
            PerkInventoryStatusEffectDurationLowerer.lower_status_effects_duration(perk_inv="not PerkList object")


if __name__ == "__main__":
    unittest.main()
