import unittest

from app.characters.characters import Human, Critter
from app.items.items import Armor
from app.items.weapons import RangedWeapon, MeleeWeapon
from app.mechanics.combat_calculators import CombatCalculatorError, DamageCalculator, DamageFormulaConverter
from app.mechanics.combat_calculators import AccuracyCalculator, EffectiveAccuracyCalculator
from app.mechanics.combat_calculators import DamageResistanceCalculator, EffectiveDamageCalculator, APCostCalculator
from app.mechanics.inventory import InventoryItemAdder, InventoryItemEquipper, InventoryItemUnequipper
from app.mechanics.perk_inventory import PerkInventoryPerkAdder
from app.perks.perks import CharacterPerk


class DamageFormulaConverterTests(unittest.TestCase):

    def test_get_damage_tuple_with_full_damage_formula_multiple_rolls(self):
        damage_formula = "2 + 4d6"
        correct_damage_tuple = (2, 4, 6)
        damage_tuple = DamageFormulaConverter.get_damage_tuple(damage_formula=damage_formula)
        self.assertEqual(correct_damage_tuple, damage_tuple)

    def test_get_damage_tuple_with_full_damage_formula_single_roll(self):
        damage_formula = "2 + d6"
        correct_damage_tuple = (2, 1, 6)
        damage_tuple = DamageFormulaConverter.get_damage_tuple(damage_formula=damage_formula)
        self.assertEqual(correct_damage_tuple, damage_tuple)

    def test_get_damage_tuple_with_multiple_rolls_only(self):
        damage_formula = "4d6"
        correct_damage_tuple = (0, 4, 6)
        damage_tuple = DamageFormulaConverter.get_damage_tuple(damage_formula=damage_formula)
        self.assertEqual(correct_damage_tuple, damage_tuple)

    def test_get_damage_tuple_with_single_roll_only(self):
        damage_formula = "d6"
        correct_damage_tuple = (0, 1, 6)
        damage_tuple = DamageFormulaConverter.get_damage_tuple(damage_formula=damage_formula)
        self.assertEqual(correct_damage_tuple, damage_tuple)

    def test_damage_range_with_full_damage_formula_multiple_rolls(self):
        damage_formula = "2 + 4d6"
        correct_damage_range = (6, 26)
        damage_range = DamageFormulaConverter.get_damage_range(damage_formula=damage_formula)
        self.assertTupleEqual(correct_damage_range, damage_range)

    def test_damage_range_with_full_damage_formula_single_roll(self):
        damage_formula = "2 + d6"
        correct_damage_range = (3, 8)
        damage_range = DamageFormulaConverter.get_damage_range(damage_formula=damage_formula)
        self.assertTupleEqual(correct_damage_range, damage_range)

    def test_damage_range_with_multiple_rolls_only(self):
        damage_formula = "4d6"
        correct_damage_range = (4, 24)
        damage_range = DamageFormulaConverter.get_damage_range(damage_formula=damage_formula)
        self.assertTupleEqual(correct_damage_range, damage_range)

    def test_damage_range_with_single_roll_only(self):
        damage_formula = "d6"
        correct_damage_range = (1, 6)
        damage_range = DamageFormulaConverter.get_damage_range(damage_formula=damage_formula)
        self.assertTupleEqual(correct_damage_range, damage_range)

    def test_incorrect_str_as_damage_formula_raises_exception(self):
        with self.assertRaisesRegex(CombatCalculatorError, "incorrect string for damage formula"):
            DamageFormulaConverter.get_damage_tuple(damage_formula="two + 4d6")
        with self.assertRaisesRegex(CombatCalculatorError, "incorrect string for damage formula"):
            DamageFormulaConverter.get_damage_range(damage_formula=2)


class DamageCalculatorTests(unittest.TestCase):

    def setUp(self):
        self.character = Human(name="Human", tags="human", level=1, strength=5, endurance=5, agility=5,
                               perception=5, intelligence=5)
        self.critter = Critter(name="Critter", tags="critter, dog", level=1, strength=5, endurance=5, agility=5,
                               perception=5, intelligence=5, health_bonus=10, exp_award=10)
        weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short", name="Gun", desc="Test gun.", damage="2 + 4d6",
                              ammo_type="ammo", clip_size=10, armor_pen=0, accuracy=0, ap_cost=10, st_requirement=1,
                              value=10, weight=2.0)
        InventoryItemAdder.add_item(inv=self.character.inventory, item_to_add=weapon)
        InventoryItemEquipper.equip_item(inv=self.character.inventory, item_to_equip=self.character.inventory.items[0])

    def test_base_weapon_damage(self):
        damage = DamageCalculator.get_weapon_damage(character=self.character)
        self.assertEqual("2 + 4d6", damage)

    def test_weapon_damage_with_weapon_type_damage_bonus_perks(self):
        perk = CharacterPerk(perk_id="perk", tags="perk, damage", name="Perk", desc="Test perk.",
                             effects="weapon, short, damage, 2", requirements="agility, 5")
        PerkInventoryPerkAdder.add_perk(perk_inv=self.character.perks, perk_to_add=perk)
        damage = DamageCalculator.get_weapon_damage(character=self.character)
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
            DamageCalculator.get_weapon_damage(character=self.character)

    def test_same_obj_as_character_and_opponent_raises_exception(self):
        with self.assertRaisesRegex(CombatCalculatorError, "character and opponent are the same object"):
            DamageCalculator.get_weapon_damage(character=self.character, opponent=self.character)

    def test_incorrect_obj_as_character_raises_exception(self):
        with self.assertRaisesRegex(CombatCalculatorError, "incorrect object type for character"):
            DamageCalculator.get_weapon_damage(character="not Character derived object")
        with self.assertRaisesRegex(CombatCalculatorError, "incorrect object type for opponent"):
            DamageCalculator.get_weapon_damage(character=self.character, opponent="not Character derived object")


class AccuracyCalculatorTests(unittest.TestCase):

    def setUp(self):
        self.character = Human(name="Human", tags="human", level=1, strength=5, endurance=5, agility=5,
                               perception=5, intelligence=5)
        self.critter = Critter(name="Critter", tags="critter, dog", level=1, strength=5, endurance=5, agility=5,
                               perception=5, intelligence=5, health_bonus=10, exp_award=10)
        weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short", name="Gun", desc="Test gun.", damage="2 + 4d6",
                              ammo_type="ammo", clip_size=10, armor_pen=0, accuracy=0, ap_cost=10, st_requirement=1,
                              value=10, weight=2.0)
        InventoryItemAdder.add_item(inv=self.character.inventory, item_to_add=weapon)
        InventoryItemEquipper.equip_item(inv=self.character.inventory, item_to_equip=self.character.inventory.items[0])

    def test_base_ranged_weapon_accuracy(self):
        accuracy = AccuracyCalculator.get_weapon_accuracy(character=self.character)
        self.assertEqual(6, accuracy)
        self.character.guns = 5
        accuracy = AccuracyCalculator.get_weapon_accuracy(character=self.character)
        self.assertEqual(10, accuracy)

    def test_ranged_weapon_accuracy_with_weapon_type_accuracy_bonus_perks(self):
        perk = CharacterPerk(perk_id="perk", tags="perk, accuracy", name="Perk", desc="Test perk.",
                             effects="weapon, gun, short, accuracy, 1", requirements="agility, 5")
        PerkInventoryPerkAdder.add_perk(perk_inv=self.character.perks, perk_to_add=perk)
        accuracy = AccuracyCalculator.get_weapon_accuracy(character=self.character)
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
        InventoryItemEquipper.equip_item(inv=self.character.inventory, item_to_equip=self.character.inventory.items[0])
        accuracy = AccuracyCalculator.get_weapon_accuracy(character=self.character)
        self.assertEqual(7, accuracy)

    def test_ranged_weapon_accuracy_with_perks_without_qualifying_bonuses_gives_no_bonus_accuracy(self):
        weapon = RangedWeapon(item_id="laser", tags="weapon, energy, short, laser", name="Laser", desc="Test laser.",
                              damage="2 + 4d6", ammo_type="ammo", clip_size=10, armor_pen=0, accuracy=0, ap_cost=10,
                              st_requirement=1, value=10, weight=2.0)
        InventoryItemAdder.add_item(inv=self.character.inventory, item_to_add=weapon)
        InventoryItemEquipper.equip_item(inv=self.character.inventory, item_to_equip=self.character.inventory.items[0])
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
        InventoryItemEquipper.equip_item(inv=self.character.inventory, item_to_equip=self.character.inventory.items[0])
        accuracy = AccuracyCalculator.get_weapon_accuracy(character=self.character)
        self.assertEqual(6, accuracy)
        self.character.melee = 5
        accuracy = AccuracyCalculator.get_weapon_accuracy(character=self.character)
        self.assertEqual(10, accuracy)

    def test_melee_weapon_accuracy_with_weapon_type_accuracy_bonus_perks(self):
        weapon = MeleeWeapon(item_id="melee", tags="weapon, melee, sharp", name="Melee", desc="Test melee.",
                             damage="2 + 4d6", effect="bleed_minor", eff_chance="-6 + d10", armor_pen=0, accuracy=0,
                             ap_cost=10, st_requirement=1, value=5, weight=1.0)
        InventoryItemAdder.add_item(inv=self.character.inventory, item_to_add=weapon)
        InventoryItemEquipper.equip_item(inv=self.character.inventory, item_to_equip=self.character.inventory.items[0])
        perk = CharacterPerk(perk_id="perk", tags="perk, accuracy", name="Perk", desc="Test perk.",
                             effects="weapon, melee, sharp, accuracy, 1", requirements="agility, 5")
        PerkInventoryPerkAdder.add_perk(perk_inv=self.character.perks, perk_to_add=perk)
        accuracy = AccuracyCalculator.get_weapon_accuracy(character=self.character)
        self.assertEqual(7, accuracy)

    def test_melee_weapon_accuracy_with_opponent_type_accuracy_bonus_perks(self):
        weapon = MeleeWeapon(item_id="melee", tags="weapon, melee, sharp", name="Melee", desc="Test melee.",
                             damage="2 + 4d6", effect="bleed_minor", eff_chance="-6 + d10", armor_pen=0, accuracy=0,
                             ap_cost=10, st_requirement=1, value=5, weight=1.0)
        InventoryItemAdder.add_item(inv=self.character.inventory, item_to_add=weapon)
        InventoryItemEquipper.equip_item(inv=self.character.inventory, item_to_equip=self.character.inventory.items[0])
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
        InventoryItemEquipper.equip_item(inv=self.character.inventory, item_to_equip=self.character.inventory.items[0])
        accuracy = AccuracyCalculator.get_weapon_accuracy(character=self.character)
        self.assertEqual(7, accuracy)

    def test_melee_weapon_accuracy_with_perks_without_qualifying_bonuses_gives_no_bonus_accuracy(self):
        weapon = MeleeWeapon(item_id="melee", tags="weapon, melee, blunt", name="Melee", desc="Test melee.",
                             damage="2 + 4d6", effect="bleed_minor", eff_chance="-6 + d10", armor_pen=0, accuracy=0,
                             ap_cost=10, st_requirement=1, value=5, weight=1.0)
        InventoryItemAdder.add_item(inv=self.character.inventory, item_to_add=weapon)
        InventoryItemEquipper.equip_item(inv=self.character.inventory, item_to_equip=self.character.inventory.items[0])
        perk = CharacterPerk(perk_id="perk", tags="perk, accuracy", name="Perk", desc="Test perk.",
                             effects="weapon, melee, sharp, accuracy, 1", requirements="agility, 5")
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
            AccuracyCalculator.get_weapon_accuracy(character=self.character)

    def test_same_obj_as_character_and_opponent_raises_exception(self):
        with self.assertRaisesRegex(CombatCalculatorError, "character and opponent are the same object"):
            AccuracyCalculator.get_weapon_accuracy(character=self.character, opponent=self.character)

    def test_incorrect_obj_as_character_raises_exception(self):
        with self.assertRaisesRegex(CombatCalculatorError, "incorrect object type for character"):
            AccuracyCalculator.get_weapon_accuracy(character="not Character derived object")
        with self.assertRaisesRegex(CombatCalculatorError, "incorrect object type for opponent"):
            AccuracyCalculator.get_weapon_accuracy(character=self.character, opponent="not Character derived object")


class EffectiveAccuracyCalculatorTests(unittest.TestCase):

    def setUp(self):
        self.character = Human(name="Human", tags="human", level=1, strength=5, endurance=5, agility=5,
                               perception=5, intelligence=5)
        self.opponent = Human(name="Human", tags="human", level=1, strength=5, endurance=5, agility=5,
                              perception=5, intelligence=5)
        weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short", name="Gun", desc="Test gun.", damage="2 + 4d6",
                              ammo_type="ammo", clip_size=10, armor_pen=0, accuracy=2, ap_cost=10, st_requirement=1,
                              value=10, weight=2.0)
        armor = Armor(item_id="armor", tags="armor", name="Armor", desc="Test armor.", dmg_res=0, rad_res=10,
                      evasion=0, value=10, weight=2.5)
        InventoryItemAdder.add_item(inv=self.character.inventory, item_to_add=weapon)
        InventoryItemEquipper.equip_item(inv=self.character.inventory, item_to_equip=self.character.inventory.items[0])
        InventoryItemAdder.add_item(inv=self.opponent.inventory, item_to_add=armor)
        InventoryItemEquipper.equip_item(inv=self.opponent.inventory, item_to_equip=self.opponent.inventory.items[0])
        self.character.guns = 5

    def test_base_accuracy_against_opponent(self):
        accuracy = EffectiveAccuracyCalculator.get_effective_accuracy(character=self.character, opponent=self.opponent)
        self.assertEqual(12, accuracy)

    def test_accuracy_with_weapon_type_accuracy_perk_against_opponent(self):
        perk = CharacterPerk(perk_id="perk", tags="perk, accuracy", name="Perk", desc="Test perk.",
                             effects="weapon, gun, short, accuracy, 1", requirements="agility, 5")
        PerkInventoryPerkAdder.add_perk(perk_inv=self.character.perks, perk_to_add=perk)
        accuracy = EffectiveAccuracyCalculator.get_effective_accuracy(character=self.character, opponent=self.opponent)
        self.assertEqual(13, accuracy)

    def test_accuracy_with_opponent_type_accuracy_perk_against_opponent(self):
        perk = CharacterPerk(perk_id="perk", tags="perk, accuracy", name="Perk", desc="Test perk.",
                             effects="human, accuracy, 2", requirements="agility, 5")
        PerkInventoryPerkAdder.add_perk(perk_inv=self.character.perks, perk_to_add=perk)
        accuracy = EffectiveAccuracyCalculator.get_effective_accuracy(character=self.character, opponent=self.opponent)
        self.assertEqual(14, accuracy)

    def test_accuracy_against_opponent_with_armor_evasion_bonus(self):
        armor = Armor(item_id="armor", tags="armor", name="Armor", desc="Test armor.", dmg_res=0, rad_res=10,
                      evasion=2, value=10, weight=2.5)
        InventoryItemAdder.add_item(inv=self.opponent.inventory, item_to_add=armor)
        InventoryItemEquipper.equip_item(inv=self.opponent.inventory, item_to_equip=self.opponent.inventory.items[0])
        accuracy = EffectiveAccuracyCalculator.get_effective_accuracy(character=self.character, opponent=self.opponent)
        self.assertEqual(10, accuracy)

    def test_accuracy_against_opponent_with_evasion_perk(self):
        perk = CharacterPerk(perk_id="perk", tags="perk, evasion", name="Perk", desc="Test perk.",
                             effects="evasion, 1", requirements="agility, 5")
        PerkInventoryPerkAdder.add_perk(perk_inv=self.opponent.perks, perk_to_add=perk)
        accuracy = EffectiveAccuracyCalculator.get_effective_accuracy(character=self.character, opponent=self.opponent)
        self.assertEqual(11, accuracy)

    def test_accuracy_with_perks_against_opponent_with_perk_and_armor_evasion_bonus(self):
        weapon_type_perk = CharacterPerk(perk_id="perk", tags="perk, accuracy", name="Perk", desc="Test perk.",
                                         effects="weapon, gun, short, accuracy, 1", requirements="agility, 5")
        opponent_type_perk = CharacterPerk(perk_id="another_perk", tags="perk, accuracy", name="Perk",
                                           desc="Test perk.", effects="human, accuracy, 2", requirements="agility, 5")
        opponent_evasion_perk = CharacterPerk(perk_id="perk", tags="perk, evasion", name="Perk", desc="Test perk.",
                                              effects="evasion, 1", requirements="agility, 5")
        PerkInventoryPerkAdder.add_perk(perk_inv=self.character.perks, perk_to_add=weapon_type_perk)
        PerkInventoryPerkAdder.add_perk(perk_inv=self.character.perks, perk_to_add=opponent_type_perk)
        PerkInventoryPerkAdder.add_perk(perk_inv=self.opponent.perks, perk_to_add=opponent_evasion_perk)
        armor = Armor(item_id="armor", tags="armor", name="Armor", desc="Test armor.", dmg_res=0, rad_res=10,
                      evasion=2, value=10, weight=2.5)
        InventoryItemAdder.add_item(inv=self.opponent.inventory, item_to_add=armor)
        InventoryItemEquipper.equip_item(inv=self.opponent.inventory, item_to_equip=self.opponent.inventory.items[0])
        accuracy = EffectiveAccuracyCalculator.get_effective_accuracy(character=self.character, opponent=self.opponent)
        self.assertEqual(12, accuracy)

    def test_minimum_accuracy_against_opponent(self):
        self.character.guns = 0
        armor = Armor(item_id="armor", tags="armor", name="Armor", desc="Test armor.", dmg_res=0, rad_res=10,
                      evasion=20, value=10, weight=2.5)
        InventoryItemAdder.add_item(inv=self.opponent.inventory, item_to_add=armor)
        InventoryItemEquipper.equip_item(inv=self.opponent.inventory, item_to_equip=self.opponent.inventory.items[0])
        accuracy = EffectiveAccuracyCalculator.get_effective_accuracy(character=self.character, opponent=self.opponent)
        self.assertEqual(1, accuracy)

    def test_same_obj_as_character_and_opponent_raises_exception(self):
        with self.assertRaisesRegex(CombatCalculatorError, "character and opponent are the same object"):
            EffectiveAccuracyCalculator.get_effective_accuracy(character=self.character, opponent=self.character)

    def test_incorrect_obj_as_character_raises_exception(self):
        with self.assertRaisesRegex(CombatCalculatorError, "incorrect object type for character"):
            EffectiveAccuracyCalculator.get_effective_accuracy(character="not Character derived object",
                                                               opponent=self.opponent)
        with self.assertRaisesRegex(CombatCalculatorError, "incorrect object type for opponent"):
            EffectiveAccuracyCalculator.get_effective_accuracy(character=self.character,
                                                               opponent="not Character derived object")


class DamageResistanceCalculatorTests(unittest.TestCase):

    def setUp(self):
        self.character = Human(name="Human", tags="human", level=1, strength=5, endurance=5, agility=5,
                               perception=5, intelligence=5)
        self.critter = Critter(name="Critter", tags="critter, dog", level=1, strength=5, endurance=5, agility=5,
                               perception=5, intelligence=5, health_bonus=10, exp_award=10)
        armor = Armor(item_id="armor", tags="armor", name="Armor", desc="Test armor.", dmg_res=0, rad_res=10,
                      evasion=2, value=10, weight=2.5)
        InventoryItemAdder.add_item(inv=self.character.inventory, item_to_add=armor)
        InventoryItemEquipper.equip_item(inv=self.character.inventory, item_to_equip=self.character.inventory.items[0])

    def test_base_damage_resistance(self):
        dmg_res = DamageResistanceCalculator.get_damage_resistance(character=self.character)
        self.assertEqual(0, dmg_res)

    def test_damage_resistance_with_armor_with_damage_resistance_bonus(self):
        armor = Armor(item_id="armor", tags="armor", name="Armor", desc="Test armor.", dmg_res=5, rad_res=10,
                      evasion=2, value=10, weight=2.5)
        InventoryItemAdder.add_item(inv=self.character.inventory, item_to_add=armor)
        InventoryItemEquipper.equip_item(inv=self.character.inventory, item_to_equip=self.character.inventory.items[0])
        dmg_res = DamageResistanceCalculator.get_damage_resistance(character=self.character)
        self.assertEqual(5, dmg_res)

    def test_damage_resistance_with_damage_resistance_bonus_perks(self):
        perk = CharacterPerk(perk_id="perk", tags="perk, dmg_res", name="Perk", desc="Test perk.",
                             effects="armor, dmg_res, 1", requirements="agility, 5")
        PerkInventoryPerkAdder.add_perk(perk_inv=self.character.perks, perk_to_add=perk)
        dmg_res = DamageResistanceCalculator.get_damage_resistance(character=self.character)
        self.assertEqual(1, dmg_res)

    def test_damage_resistance_with_opponent_type_damage_resistance_bonus_perks(self):
        perk = CharacterPerk(perk_id="perk", tags="perk, dmg_res", name="Perk", desc="Test perk.",
                             effects="critter, dog, dmg_res, 2", requirements="agility, 5")
        PerkInventoryPerkAdder.add_perk(perk_inv=self.character.perks, perk_to_add=perk)
        dmg_res = DamageResistanceCalculator.get_damage_resistance(character=self.character, opponent=self.critter)
        self.assertEqual(2, dmg_res)

    def test_damage_resistance_with_perks_without_qualifying_bonuses_gives_no_bonus_damage_resistance(self):
        perk = CharacterPerk(perk_id="perk", tags="perk, dmg_res", name="Perk", desc="Test perk.",
                             effects="critter, rat, dmg_res, 2", requirements="agility, 5")
        PerkInventoryPerkAdder.add_perk(perk_inv=self.character.perks, perk_to_add=perk)
        dmg_res = DamageResistanceCalculator.get_damage_resistance(character=self.character, opponent=self.critter)
        self.assertEqual(0, dmg_res)

    def test_no_armor_equipped_raises_exception(self):
        InventoryItemUnequipper.unequip_armor(inv=self.character.inventory)
        with self.assertRaisesRegex(CombatCalculatorError, "no armor equipped on character: .*"):
            DamageResistanceCalculator.get_damage_resistance(character=self.character)

    def test_same_obj_as_character_and_opponent_raises_exception(self):
        with self.assertRaisesRegex(CombatCalculatorError, "character and opponent are the same object"):
            DamageResistanceCalculator.get_damage_resistance(character=self.character, opponent=self.character)

    def test_incorrect_obj_as_character_raises_exception(self):
        with self.assertRaisesRegex(CombatCalculatorError, "incorrect object type for character"):
            DamageResistanceCalculator.get_damage_resistance(character="not Character derived object")
        with self.assertRaisesRegex(CombatCalculatorError, "incorrect object type for opponent"):
            DamageResistanceCalculator.get_damage_resistance(character=self.character,
                                                             opponent="not Character derived object")


class EffectiveDamageCalculatorTests(unittest.TestCase):

    def setUp(self):
        self.character = Human(name="Human", tags="human", level=1, strength=5, endurance=5, agility=5,
                               perception=5, intelligence=5)
        self.opponent = Human(name="Human", tags="human", level=1, strength=5, endurance=5, agility=5,
                              perception=5, intelligence=5)
        weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short", name="Gun", desc="Test gun.", damage="2 + 4d6",
                              ammo_type="ammo", clip_size=10, armor_pen=0, accuracy=2, ap_cost=10, st_requirement=1,
                              value=10, weight=2.0)
        armor = Armor(item_id="armor", tags="armor", name="Armor", desc="Test armor.", dmg_res=0, rad_res=10,
                      evasion=0, value=10, weight=2.5)
        InventoryItemAdder.add_item(inv=self.character.inventory, item_to_add=weapon)
        InventoryItemEquipper.equip_item(inv=self.character.inventory, item_to_equip=self.character.inventory.items[0])
        InventoryItemAdder.add_item(inv=self.opponent.inventory, item_to_add=armor)
        InventoryItemEquipper.equip_item(inv=self.opponent.inventory, item_to_equip=self.opponent.inventory.items[0])

    def test_base_damage_against_opponent(self):
        damage_roll = 10
        damage = EffectiveDamageCalculator.get_effective_damage(character=self.character, opponent=self.opponent,
                                                                damage_roll=damage_roll)
        self.assertEqual(12, damage)

    def test_damage_with_weapon_type_damage_perk_against_opponent(self):
        perk = CharacterPerk(perk_id="perk", tags="perk, damage", name="Perk", desc="Test perk.",
                             effects="weapon, short, damage, 2", requirements="agility, 5")
        PerkInventoryPerkAdder.add_perk(perk_inv=self.character.perks, perk_to_add=perk)
        damage_roll = 10
        damage = EffectiveDamageCalculator.get_effective_damage(character=self.character, opponent=self.opponent,
                                                                damage_roll=damage_roll)
        self.assertEqual(14, damage)

    def test_damage_with_opponent_type_damage_perk_against_opponent(self):
        perk = CharacterPerk(perk_id="perk", tags="perk, damage", name="Perk", desc="Test perk.",
                             effects="human, damage, 4", requirements="agility, 5")
        PerkInventoryPerkAdder.add_perk(perk_inv=self.character.perks, perk_to_add=perk)
        damage_roll = 10
        damage = EffectiveDamageCalculator.get_effective_damage(character=self.character, opponent=self.opponent,
                                                                damage_roll=damage_roll)
        self.assertEqual(16, damage)

    def test_damage_against_opponent_with_armor_dmg_res_bonus(self):
        armor = Armor(item_id="armor", tags="armor", name="Armor", desc="Test armor.", dmg_res=4, rad_res=10,
                      evasion=0, value=10, weight=2.5)
        InventoryItemAdder.add_item(inv=self.opponent.inventory, item_to_add=armor)
        InventoryItemEquipper.equip_item(inv=self.opponent.inventory, item_to_equip=self.opponent.inventory.items[0])
        damage_roll = 10
        damage = EffectiveDamageCalculator.get_effective_damage(character=self.character, opponent=self.opponent,
                                                                damage_roll=damage_roll)
        self.assertEqual(8, damage)

    def test_damage_against_opponent_with_dmg_res_perk(self):
        perk = CharacterPerk(perk_id="perk", tags="perk, dmg_res", name="Perk", desc="Test perk.",
                             effects="armor, dmg_res, 2", requirements="agility, 5")
        PerkInventoryPerkAdder.add_perk(perk_inv=self.opponent.perks, perk_to_add=perk)
        damage_roll = 10
        damage = EffectiveDamageCalculator.get_effective_damage(character=self.character, opponent=self.opponent,
                                                                damage_roll=damage_roll)
        self.assertEqual(10, damage)

    def test_damage_with_perks_against_opponent_with_perk_and_armor_dmg_res_bonus(self):
        weapon_type_perk = CharacterPerk(perk_id="perk", tags="perk, damage", name="Perk", desc="Test perk.",
                                         effects="weapon, gun, short, damage, 2", requirements="agility, 5")
        opponent_type_perk = CharacterPerk(perk_id="another_perk", tags="perk, damage", name="Perk",
                                           desc="Test perk.", effects="human, damage, 4", requirements="agility, 5")
        opponent_dmg_res_perk = CharacterPerk(perk_id="perk", tags="perk, dmg_res", name="Perk", desc="Test perk.",
                                              effects="armor, dmg_res, 2", requirements="agility, 5")
        PerkInventoryPerkAdder.add_perk(perk_inv=self.character.perks, perk_to_add=weapon_type_perk)
        PerkInventoryPerkAdder.add_perk(perk_inv=self.character.perks, perk_to_add=opponent_type_perk)
        PerkInventoryPerkAdder.add_perk(perk_inv=self.opponent.perks, perk_to_add=opponent_dmg_res_perk)
        armor = Armor(item_id="armor", tags="armor", name="Armor", desc="Test armor.", dmg_res=4, rad_res=10,
                      evasion=0, value=10, weight=2.5)
        InventoryItemAdder.add_item(inv=self.opponent.inventory, item_to_add=armor)
        InventoryItemEquipper.equip_item(inv=self.opponent.inventory, item_to_equip=self.opponent.inventory.items[0])
        damage_roll = 10
        damage = EffectiveDamageCalculator.get_effective_damage(character=self.character, opponent=self.opponent,
                                                                damage_roll=damage_roll)
        self.assertEqual(12, damage)

    def test_damage_with_penetration_against_opponent(self):
        weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short", name="Gun", desc="Test gun.", damage="2 + 4d6",
                              ammo_type="ammo", clip_size=10, armor_pen=5, accuracy=2, ap_cost=10, st_requirement=1,
                              value=10, weight=2.0)
        InventoryItemAdder.add_item(inv=self.character.inventory, item_to_add=weapon)
        InventoryItemEquipper.equip_item(inv=self.character.inventory, item_to_equip=self.character.inventory.items[0])
        damage_roll = 10
        damage = EffectiveDamageCalculator.get_effective_damage(character=self.character, opponent=self.opponent,
                                                                damage_roll=damage_roll)
        self.assertEqual(12, damage)

    def test_damage_with_penetration_against_opponent_with_armor_dmg_res_bonus(self):
        weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short", name="Gun", desc="Test gun.", damage="2 + 4d6",
                              ammo_type="ammo", clip_size=10, armor_pen=5, accuracy=2, ap_cost=10, st_requirement=1,
                              value=10, weight=2.0)
        armor = Armor(item_id="armor", tags="armor", name="Armor", desc="Test armor.", dmg_res=15, rad_res=10,
                      evasion=0, value=10, weight=2.5)
        InventoryItemAdder.add_item(inv=self.character.inventory, item_to_add=weapon)
        InventoryItemEquipper.equip_item(inv=self.character.inventory, item_to_equip=self.character.inventory.items[0])
        InventoryItemAdder.add_item(inv=self.opponent.inventory, item_to_add=armor)
        InventoryItemEquipper.equip_item(inv=self.opponent.inventory, item_to_equip=self.opponent.inventory.items[0])
        damage_roll = 10
        damage = EffectiveDamageCalculator.get_effective_damage(character=self.character, opponent=self.opponent,
                                                                damage_roll=damage_roll)
        self.assertEqual(2, damage)

    def test_damage_with_over_penetration_against_opponent_with_armor_dmg_res_bonus(self):
        weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short", name="Gun", desc="Test gun.", damage="2 + 4d6",
                              ammo_type="ammo", clip_size=10, armor_pen=15, accuracy=2, ap_cost=10, st_requirement=1,
                              value=10, weight=2.0)
        armor = Armor(item_id="armor", tags="armor", name="Armor", desc="Test armor.", dmg_res=5, rad_res=10,
                      evasion=0, value=10, weight=2.5)
        InventoryItemAdder.add_item(inv=self.character.inventory, item_to_add=weapon)
        InventoryItemEquipper.equip_item(inv=self.character.inventory, item_to_equip=self.character.inventory.items[0])
        InventoryItemAdder.add_item(inv=self.opponent.inventory, item_to_add=armor)
        InventoryItemEquipper.equip_item(inv=self.opponent.inventory, item_to_equip=self.opponent.inventory.items[0])
        damage_roll = 10
        damage = EffectiveDamageCalculator.get_effective_damage(character=self.character, opponent=self.opponent,
                                                                damage_roll=damage_roll)
        self.assertEqual(12, damage)

    def test_minimum_damage_against_opponent(self):
        armor = Armor(item_id="armor", tags="armor", name="Armor", desc="Test armor.", dmg_res=40, rad_res=10,
                      evasion=0, value=10, weight=2.5)
        InventoryItemAdder.add_item(inv=self.opponent.inventory, item_to_add=armor)
        InventoryItemEquipper.equip_item(inv=self.opponent.inventory, item_to_equip=self.opponent.inventory.items[0])
        damage_roll = 10
        damage = EffectiveDamageCalculator.get_effective_damage(character=self.character, opponent=self.opponent,
                                                                damage_roll=damage_roll)
        self.assertEqual(0, damage)

    def test_minimum_damage_with_penetration_against_opponent(self):
        weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short", name="Gun", desc="Test gun.", damage="2 + 4d6",
                              ammo_type="ammo", clip_size=10, armor_pen=5, accuracy=2, ap_cost=10, st_requirement=1,
                              value=10, weight=2.0)
        armor = Armor(item_id="armor", tags="armor", name="Armor", desc="Test armor.", dmg_res=50, rad_res=10,
                      evasion=0, value=10, weight=2.5)
        InventoryItemAdder.add_item(inv=self.character.inventory, item_to_add=weapon)
        InventoryItemEquipper.equip_item(inv=self.character.inventory, item_to_equip=self.character.inventory.items[0])
        InventoryItemAdder.add_item(inv=self.opponent.inventory, item_to_add=armor)
        InventoryItemEquipper.equip_item(inv=self.opponent.inventory, item_to_equip=self.opponent.inventory.items[0])
        damage_roll = 10
        damage = EffectiveDamageCalculator.get_effective_damage(character=self.character, opponent=self.opponent,
                                                                damage_roll=damage_roll)
        self.assertEqual(0, damage)

    def test_same_obj_as_character_and_opponent_raises_exception(self):
        with self.assertRaisesRegex(CombatCalculatorError, "character and opponent are the same object"):
            EffectiveDamageCalculator.get_effective_damage(character=self.character, opponent=self.character,
                                                           damage_roll=10)

    def test_incorrect_obj_as_character_raises_exception(self):
        with self.assertRaisesRegex(CombatCalculatorError, "incorrect object type for character"):
            EffectiveDamageCalculator.get_effective_damage(character="not Character derived object",
                                                           opponent=self.opponent, damage_roll=10)
        with self.assertRaisesRegex(CombatCalculatorError, "incorrect object type for opponent"):
            EffectiveDamageCalculator.get_effective_damage(character=self.character,
                                                           opponent="not Character derived object", damage_roll=10)


class APCostCalculatorTests(unittest.TestCase):

    def setUp(self):
        self.character = Human(name="Human", tags="human", level=1, strength=5, endurance=5, agility=5,
                               perception=5, intelligence=5)
        self.critter = Critter(name="Critter", tags="critter, dog", level=1, strength=5, endurance=5, agility=5,
                               perception=5, intelligence=5, health_bonus=10, exp_award=10)
        weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short", name="Gun", desc="Test gun.", damage="2 + 4d6",
                              ammo_type="ammo", clip_size=10, armor_pen=0, accuracy=0, ap_cost=10, st_requirement=1,
                              value=10, weight=2.0)
        InventoryItemAdder.add_item(inv=self.character.inventory, item_to_add=weapon)
        InventoryItemEquipper.equip_item(inv=self.character.inventory, item_to_equip=self.character.inventory.items[0])

    def test_base_ap_cost(self):
        ap_cost = APCostCalculator.get_ap_cost(character=self.character)
        self.assertEqual(10, ap_cost)

    def test_ap_cost_with_weapon_type_ap_cost_bonus_perks(self):
        perk = CharacterPerk(perk_id="perk", tags="perk, ap_cost", name="Perk", desc="Test perk.",
                             effects="weapon, short, ap_cost, -2", requirements="agility, 5")
        PerkInventoryPerkAdder.add_perk(perk_inv=self.character.perks, perk_to_add=perk)
        ap_cost = APCostCalculator.get_ap_cost(character=self.character)
        self.assertEqual(8, ap_cost)

    def test_ap_cost_with_perks_without_qualifying_bonuses_gives_no_bonus_ap_cost(self):
        perk = CharacterPerk(perk_id="perk", tags="perk, ap_cost", name="Perk", desc="Test perk.",
                             effects="weapon, long, ap_cost, -2", requirements="agility, 5")
        another_perk = CharacterPerk(perk_id="another_perk", tags="perk, damage", name="Perk", desc="Test perk.",
                                     effects="weapon, short, damage, 2", requirements="agility, 5")
        PerkInventoryPerkAdder.add_perk(perk_inv=self.character.perks, perk_to_add=perk)
        PerkInventoryPerkAdder.add_perk(perk_inv=self.character.perks, perk_to_add=another_perk)
        ap_cost = APCostCalculator.get_ap_cost(character=self.character)
        self.assertEqual(10, ap_cost)

    def test_no_weapon_equipped_raises_exception(self):
        InventoryItemUnequipper.unequip_weapon(inv=self.character.inventory)
        with self.assertRaisesRegex(CombatCalculatorError, "no weapon equipped on character: .*"):
            APCostCalculator.get_ap_cost(character=self.character)

    def test_incorrect_obj_as_character_raises_exception(self):
        with self.assertRaisesRegex(CombatCalculatorError, "incorrect object type for character"):
            APCostCalculator.get_ap_cost(character="not Character derived object")


if __name__ == "__main__":
    unittest.main()
