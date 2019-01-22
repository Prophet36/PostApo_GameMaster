import unittest

from app.characters.characters import Human, Critter
from app.items.weapons import RangedWeapon, MeleeWeapon
from app.mechanics.combat_calculators import CombatCalculatorError, DamageCalculator, DamageFormulaCalculator
from app.mechanics.combat_calculators import AccuracyCalculator
from app.mechanics.inventory import InventoryItemAdder, InventoryItemEquipper, InventoryItemUnequipper
from app.mechanics.perk_inventory import PerkInventoryPerkAdder
from app.perks.perks import CharacterPerk


class TestDamageCalculator(unittest.TestCase):

    def setUp(self):
        self.character = Human(name="Human", tags="character", level=1, strength=5, endurance=5, agility=5,
                               perception=5, intelligence=5)
        self.critter = Critter(name="Critter", tags="critter, dog", level=1, strength=5, endurance=5, agility=5,
                               perception=5, intelligence=5, health_bonus=10, exp_award=10)
        weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short", name="Gun", desc="Test gun.", damage="2 + 4d6",
                              ammo_type="ammo", clip_size=10, armor_pen=0, accuracy=0, ap_cost=10, st_requirement=1,
                              value=10, weight=2.0)
        InventoryItemAdder.add_item(inv=self.character.inventory, item_to_add=weapon)
        InventoryItemEquipper.equip_item(inv=self.character.inventory, item_to_equip=self.character.inventory.items[-1])

    def test_base_weapon_damage(self):
        damage = DamageCalculator.get_weapon_damage(character=self.character, opponent=self.critter)
        self.assertEqual("2 + 4d6", damage)

    def test_weapon_damage_with_weapon_type_damage_bonus_perks(self):
        perk = CharacterPerk(perk_id="perk", tags="perk, damage", name="Perk", desc="Test perk.",
                             effects="weapon, short, damage, 2", requirements="agility, 5")
        PerkInventoryPerkAdder.add_perk(perk_inv=self.character.perks, perk_to_add=perk)
        damage = DamageCalculator.get_weapon_damage(character=self.character, opponent=self.critter)
        self.assertEqual("4 + 4d6", damage)

    def test_weapon_damage_with_opponent_type_damage_bonus_perks(self):
        perk = CharacterPerk(perk_id="perk", tags="perk, damage", name="Perk", desc="Test perk.",
                             effects="critter, dog, damage, 4", requirements="agility, 5")
        PerkInventoryPerkAdder.add_perk(perk_inv=self.character.perks, perk_to_add=perk)
        damage = DamageCalculator.get_weapon_damage(character=self.character, opponent=self.critter)
        self.assertEqual("6 + 4d6", damage)

    def test_weapon_damage_with_perks_without_qualifying_bonuses_gives_no_bonus_damage(self):
        perk = CharacterPerk(perk_id="perk", tags="perk, damage", name="Perk", desc="Test perk.",
                             effects="weapon, long, damage, 2", requirements="agility, 5")
        another_perk = CharacterPerk(perk_id="another_perk", tags="perk, damage", name="Perk", desc="Test perk.",
                                     effects="critter, rat, damage, 4", requirements="agility, 5")
        PerkInventoryPerkAdder.add_perk(perk_inv=self.character.perks, perk_to_add=perk)
        PerkInventoryPerkAdder.add_perk(perk_inv=self.character.perks, perk_to_add=another_perk)
        damage = DamageCalculator.get_weapon_damage(character=self.character, opponent=self.critter)
        self.assertEqual("2 + 4d6", damage)

    def test_no_weapon_equipped_raises_exception(self):
        InventoryItemUnequipper.unequip_weapon(inv=self.character.inventory)
        with self.assertRaisesRegex(CombatCalculatorError, "no weapon equipped on character: .*"):
            DamageCalculator.get_weapon_damage(character=self.character, opponent=self.critter)

    def test_incorrect_obj_as_character_raises_exception(self):
        with self.assertRaisesRegex(CombatCalculatorError, "incorrect object type for character"):
            DamageCalculator.get_weapon_damage(character="not Character derived object", opponent=self.critter)
        with self.assertRaisesRegex(CombatCalculatorError, "incorrect object type for opponent"):
            DamageCalculator.get_weapon_damage(character=self.character, opponent="not Character derived object")

class TestDamageFormulaCalculator(unittest.TestCase):

    def test_get_damage_tuple_with_full_damage_formula_multiple_rolls(self):
        damage_formula = "2 + 4d6"
        correct_damage_tuple = (2, 4, 6)
        damage_tuple = DamageFormulaCalculator.get_damage_tuple(damage_formula=damage_formula)
        self.assertEqual(correct_damage_tuple, damage_tuple)

    def test_get_damage_tuple_with_full_damage_formula_single_roll(self):
        damage_formula = "2 + d6"
        correct_damage_tuple = (2, 1, 6)
        damage_tuple = DamageFormulaCalculator.get_damage_tuple(damage_formula=damage_formula)
        self.assertEqual(correct_damage_tuple, damage_tuple)

    def test_get_damage_tuple_with_multiple_rolls_only(self):
        damage_formula = "4d6"
        correct_damage_tuple = (0, 4, 6)
        damage_tuple = DamageFormulaCalculator.get_damage_tuple(damage_formula=damage_formula)
        self.assertEqual(correct_damage_tuple, damage_tuple)

    def test_get_damage_tuple_with_single_roll_only(self):
        damage_formula = "d6"
        correct_damage_tuple = (0, 1, 6)
        damage_tuple = DamageFormulaCalculator.get_damage_tuple(damage_formula=damage_formula)
        self.assertEqual(correct_damage_tuple, damage_tuple)

    def test_damage_range_with_full_damage_formula_multiple_rolls(self):
        damage_formula = "2 + 4d6"
        correct_damage_range = (6, 26)
        damage_range = DamageFormulaCalculator.get_damage_range(damage_formula=damage_formula)
        self.assertTupleEqual(correct_damage_range, damage_range)

    def test_damage_range_with_full_damage_formula_single_roll(self):
        damage_formula = "2 + d6"
        correct_damage_range = (3, 8)
        damage_range = DamageFormulaCalculator.get_damage_range(damage_formula=damage_formula)
        self.assertTupleEqual(correct_damage_range, damage_range)

    def test_damage_range_with_multiple_rolls_only(self):
        damage_formula = "4d6"
        correct_damage_range = (4, 24)
        damage_range = DamageFormulaCalculator.get_damage_range(damage_formula=damage_formula)
        self.assertTupleEqual(correct_damage_range, damage_range)

    def test_damage_range_with_single_roll_only(self):
        damage_formula = "d6"
        correct_damage_range = (1, 6)
        damage_range = DamageFormulaCalculator.get_damage_range(damage_formula=damage_formula)
        self.assertTupleEqual(correct_damage_range, damage_range)

    def test_incorrect_str_as_damage_formula_raises_exception(self):
        with self.assertRaisesRegex(CombatCalculatorError, "incorrect string for damage formula"):
            DamageFormulaCalculator.get_damage_tuple(damage_formula="two + 4d6")
        with self.assertRaisesRegex(CombatCalculatorError, "incorrect string for damage formula"):
            DamageFormulaCalculator.get_damage_range(damage_formula=2)


class TestAccuracyCalculator(unittest.TestCase):

    def setUp(self):
        self.character = Human(name="Human", tags="character", level=1, strength=5, endurance=5, agility=5,
                               perception=5, intelligence=5)
        self.critter = Critter(name="Critter", tags="critter, dog", level=1, strength=5, endurance=5, agility=5,
                               perception=5, intelligence=5, health_bonus=10, exp_award=10)
        weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short", name="Gun", desc="Test gun.", damage="2 + 4d6",
                              ammo_type="ammo", clip_size=10, armor_pen=0, accuracy=0, ap_cost=10, st_requirement=1,
                              value=10, weight=2.0)
        InventoryItemAdder.add_item(inv=self.character.inventory, item_to_add=weapon)
        InventoryItemEquipper.equip_item(inv=self.character.inventory, item_to_equip=self.character.inventory.items[-1])

    def test_base_ranged_weapon_accuracy(self):
        accuracy = AccuracyCalculator.get_weapon_accuracy(character=self.character, opponent=self.critter)
        self.assertEqual(6, accuracy)
        self.character.guns = 5
        accuracy = AccuracyCalculator.get_weapon_accuracy(character=self.character, opponent=self.critter)
        self.assertEqual(10, accuracy)

    def test_ranged_weapon_accuracy_with_weapon_type_accuracy_bonus_perks(self):
        perk = CharacterPerk(perk_id="perk", tags="perk, accuracy", name="Perk", desc="Test perk.",
                             effects="weapon, gun, short, accuracy, 1", requirements="agility, 5")
        PerkInventoryPerkAdder.add_perk(perk_inv=self.character.perks, perk_to_add=perk)
        accuracy = AccuracyCalculator.get_weapon_accuracy(character=self.character, opponent=self.critter)
        self.assertEqual(7, accuracy)

    def test_ranged_weapon_accuracy_with_opponent_type_accuracy_bonus_perks(self):
        perk = CharacterPerk(perk_id="perk", tags="perk, accuracy", name="Perk", desc="Test perk.",
                             effects="critter, dog, accuracy, 2", requirements="agility, 5")
        PerkInventoryPerkAdder.add_perk(perk_inv=self.character.perks, perk_to_add=perk)
        accuracy = AccuracyCalculator.get_weapon_accuracy(character=self.character, opponent=self.critter)
        self.assertEqual(8, accuracy)

    def test_ranged_weapon_accuracy_with_weapon_with_accuracy_bonus(self):
        weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short", name="Gun", desc="Test gun.", damage="2 + 4d6",
                              ammo_type="ammo", clip_size=10, armor_pen=0, accuracy=1, ap_cost=10, st_requirement=1,
                              value=10, weight=2.0)
        InventoryItemAdder.add_item(inv=self.character.inventory, item_to_add=weapon)
        InventoryItemEquipper.equip_item(inv=self.character.inventory, item_to_equip=self.character.inventory.items[-1])
        accuracy = AccuracyCalculator.get_weapon_accuracy(character=self.character, opponent=self.critter)
        self.assertEqual(7, accuracy)

    def test_ranged_weapon_accuracy_with_perks_without_qualifying_bonuses_gives_no_bonus_accuracy(self):
        weapon = RangedWeapon(item_id="laser", tags="weapon, energy, short, laser", name="Laser", desc="Test laser.",
                              damage="2 + 4d6", ammo_type="ammo", clip_size=10, armor_pen=0, accuracy=0, ap_cost=10,
                              st_requirement=1, value=10, weight=2.0)
        InventoryItemAdder.add_item(inv=self.character.inventory, item_to_add=weapon)
        InventoryItemEquipper.equip_item(inv=self.character.inventory, item_to_equip=self.character.inventory.items[-1])
        perk = CharacterPerk(perk_id="perk", tags="perk, accuracy", name="Perk", desc="Test perk.",
                             effects="weapon, gun, short, accuracy, 1", requirements="agility, 5")
        another_perk = CharacterPerk(perk_id="another_perk", tags="perk, accuracy", name="Perk", desc="Test perk.",
                                     effects="critter, rat, accuracy, 2", requirements="agility, 5")
        PerkInventoryPerkAdder.add_perk(perk_inv=self.character.perks, perk_to_add=perk)
        PerkInventoryPerkAdder.add_perk(perk_inv=self.character.perks, perk_to_add=another_perk)
        accuracy = AccuracyCalculator.get_weapon_accuracy(character=self.character, opponent=self.critter)
        self.assertEqual(6, accuracy)
        self.character.energy = 5
        accuracy = AccuracyCalculator.get_weapon_accuracy(character=self.character, opponent=self.critter)
        self.assertEqual(10, accuracy)

    def test_base_melee_weapon_accuracy(self):
        weapon = MeleeWeapon(item_id="melee", tags="weapon, melee, sharp", name="Melee", desc="Test melee.",
                             damage="2 + 4d6", effect="bleed_minor", eff_chance="-6 + d10", armor_pen=0, accuracy=0,
                             ap_cost=10, st_requirement=1, value=5, weight=1.0)
        InventoryItemAdder.add_item(inv=self.character.inventory, item_to_add=weapon)
        InventoryItemEquipper.equip_item(inv=self.character.inventory, item_to_equip=self.character.inventory.items[-1])
        accuracy = AccuracyCalculator.get_weapon_accuracy(character=self.character, opponent=self.critter)
        self.assertEqual(6, accuracy)
        self.character.melee = 5
        accuracy = AccuracyCalculator.get_weapon_accuracy(character=self.character, opponent=self.critter)
        self.assertEqual(10, accuracy)

    def test_melee_weapon_accuracy_with_weapon_type_accuracy_bonus_perks(self):
        weapon = MeleeWeapon(item_id="melee", tags="weapon, melee, sharp", name="Melee", desc="Test melee.",
                             damage="2 + 4d6", effect="bleed_minor", eff_chance="-6 + d10", armor_pen=0, accuracy=0,
                             ap_cost=10, st_requirement=1, value=5, weight=1.0)
        InventoryItemAdder.add_item(inv=self.character.inventory, item_to_add=weapon)
        InventoryItemEquipper.equip_item(inv=self.character.inventory, item_to_equip=self.character.inventory.items[-1])
        perk = CharacterPerk(perk_id="perk", tags="perk, accuracy", name="Perk", desc="Test perk.",
                             effects="weapon, melee, sharp, accuracy, 1", requirements="agility, 5")
        PerkInventoryPerkAdder.add_perk(perk_inv=self.character.perks, perk_to_add=perk)
        accuracy = AccuracyCalculator.get_weapon_accuracy(character=self.character, opponent=self.critter)
        self.assertEqual(7, accuracy)

    def test_melee_weapon_accuracy_with_opponent_type_accuracy_bonus_perks(self):
        weapon = MeleeWeapon(item_id="melee", tags="weapon, melee, sharp", name="Melee", desc="Test melee.",
                             damage="2 + 4d6", effect="bleed_minor", eff_chance="-6 + d10", armor_pen=0, accuracy=0,
                             ap_cost=10, st_requirement=1, value=5, weight=1.0)
        InventoryItemAdder.add_item(inv=self.character.inventory, item_to_add=weapon)
        InventoryItemEquipper.equip_item(inv=self.character.inventory, item_to_equip=self.character.inventory.items[-1])
        perk = CharacterPerk(perk_id="perk", tags="perk, accuracy", name="Perk", desc="Test perk.",
                             effects="critter, dog, accuracy, 2", requirements="agility, 5")
        PerkInventoryPerkAdder.add_perk(perk_inv=self.character.perks, perk_to_add=perk)
        accuracy = AccuracyCalculator.get_weapon_accuracy(character=self.character, opponent=self.critter)
        self.assertEqual(8, accuracy)

    def test_melee_weapon_accuracy_with_weapon_with_accuracy_bonus(self):
        weapon = MeleeWeapon(item_id="melee", tags="weapon, melee, sharp", name="Melee", desc="Test melee.",
                             damage="2 + 4d6", effect="bleed_minor", eff_chance="-6 + d10", armor_pen=0, accuracy=1,
                             ap_cost=10, st_requirement=1, value=5, weight=1.0)
        InventoryItemAdder.add_item(inv=self.character.inventory, item_to_add=weapon)
        InventoryItemEquipper.equip_item(inv=self.character.inventory, item_to_equip=self.character.inventory.items[-1])
        accuracy = AccuracyCalculator.get_weapon_accuracy(character=self.character, opponent=self.critter)
        self.assertEqual(7, accuracy)

    def test_melee_weapon_accuracy_with_perks_without_qualifying_bonuses_gives_no_bonus_accuracy(self):
        weapon = MeleeWeapon(item_id="melee", tags="weapon, melee, sharp", name="Melee", desc="Test melee.",
                             damage="2 + 4d6", effect="bleed_minor", eff_chance="-6 + d10", armor_pen=0, accuracy=0,
                             ap_cost=10, st_requirement=1, value=5, weight=1.0)
        InventoryItemAdder.add_item(inv=self.character.inventory, item_to_add=weapon)
        InventoryItemEquipper.equip_item(inv=self.character.inventory, item_to_equip=self.character.inventory.items[-1])
        perk = CharacterPerk(perk_id="perk", tags="perk, accuracy", name="Perk", desc="Test perk.",
                             effects="weapon, melee, blunt, accuracy, 1", requirements="agility, 5")
        another_perk = CharacterPerk(perk_id="another_perk", tags="perk, accuracy", name="Perk", desc="Test perk.",
                                     effects="critter, rat, accuracy, 2", requirements="agility, 5")
        PerkInventoryPerkAdder.add_perk(perk_inv=self.character.perks, perk_to_add=perk)
        PerkInventoryPerkAdder.add_perk(perk_inv=self.character.perks, perk_to_add=another_perk)
        accuracy = AccuracyCalculator.get_weapon_accuracy(character=self.character, opponent=self.critter)
        self.assertEqual(6, accuracy)
        self.character.melee = 5
        accuracy = AccuracyCalculator.get_weapon_accuracy(character=self.character, opponent=self.critter)
        self.assertEqual(10, accuracy)

    def test_no_weapon_equipped_raises_exception(self):
        InventoryItemUnequipper.unequip_weapon(inv=self.character.inventory)
        with self.assertRaisesRegex(CombatCalculatorError, "no weapon equipped on character: .*"):
            AccuracyCalculator.get_weapon_accuracy(character=self.character, opponent=self.critter)

    def test_incorrect_obj_as_character_raises_exception(self):
        with self.assertRaisesRegex(CombatCalculatorError, "incorrect object type for character"):
            AccuracyCalculator.get_weapon_accuracy(character="not Character derived object", opponent=self.critter)
        with self.assertRaisesRegex(CombatCalculatorError, "incorrect object type for opponent"):
            AccuracyCalculator.get_weapon_accuracy(character=self.character, opponent="not Character derived object")


if __name__ == "__main__":
    unittest.main()
