import unittest

from app.characters.characters import Human
from app.mechanics.perk_inventory import PerkInventory, PerkInventoryPerkAdder
from app.mechanics.stat_calculators import PerkAttributeCalculator
from app.perks.perks import PlayerTrait


class TestPerkAttributeCalculator(unittest.TestCase):

    def setUp(self):
        self.human = Human(name="Human", tags="human, test", level=1, strength=5, endurance=5, agility=5, perception=5,
                           intelligence=5)
        trait = PlayerTrait(perk_id="trait", tags="trait, attribute, test", name="Trait", desc="Test trait.",
                            effects="attribute, strength, -1; attribute, agility, 1", conflicts="conflicting_trait")
        PerkInventoryPerkAdder.add_perk(perk_inv=self.human.perks, perk_to_add=trait)

    def test_get_attribute_bonus(self):
        attribute_bonus = PerkAttributeCalculator.get_attribute_bonus(perk_inv=self.human.perks, attribute="agility")
        self.assertEqual(1, attribute_bonus)

    def test_get_attribute_malus(self):
        attribute_malus = PerkAttributeCalculator.get_attribute_bonus(perk_inv=self.human.perks, attribute="strength")
        self.assertEqual(-1, attribute_malus)

    def test_get_attribute_bonus_from_multiple_perks(self):
        another_trait = PlayerTrait(perk_id="another_trait", tags="trait, attribute, test", name="Trait",
                                    desc="Test trait.", effects="attribute, strength, 1; attribute, agility, 1",
                                    conflicts="conflicting_trait")
        PerkInventoryPerkAdder.add_perk(perk_inv=self.human.perks, perk_to_add=another_trait)
        strength_bonus = PerkAttributeCalculator.get_attribute_bonus(perk_inv=self.human.perks, attribute="strength")
        agility_bonus = PerkAttributeCalculator.get_attribute_bonus(perk_inv=self.human.perks, attribute="agility")
        self.assertEqual(0, strength_bonus)
        self.assertEqual(2, agility_bonus)

    def test_get_incorrect_attribute_bonus_returns_zero(self):
        attribute_bonus = PerkAttributeCalculator.get_attribute_bonus(perk_inv=self.human.perks, attribute="endurance")
        self.assertEqual(0, attribute_bonus)

    def test_incorrect_obj_as_perk_inventory_raises_exception(self):
        with self.assertRaisesRegex(PerkInventory.PerkInventoryError, "incorrect object type for perk inventory"):
            PerkInventoryPerkAdder.add_perk(perk_inv="not PerkList object", perk_to_add="perk to add")


if __name__ == "__main__":
    unittest.main()
