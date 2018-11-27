import unittest

from app.items.generic import Item, Armor, Weapon
from app.items.weapons import MeleeWeapon, RangedWeapon
from app.items.stackables import Stackable, Ammo, Consumable


class ItemTests(unittest.TestCase):

    def test_create_item_instance_raises_exception(self):
        with self.assertRaisesRegex(TypeError, "Can't instantiate abstract class .* with abstract methods .*"):
            Item(item_id="item", tags="item, default", name="Item", desc="Default item.", value=0, weight=0.0)


class ArmorTests(unittest.TestCase):

    def setUp(self):
        self.armor = Armor(item_id="armor", tags="armor, default", name="Armor", desc="Default armor.", dmg_res=0,
                           rad_res=10, evasion=2, value=10, weight=2.5)

    def test_property_values(self):
        self.assertEqual("armor", self.armor.item_id)
        self.assertEqual("armor, default", self.armor.tags)
        self.assertEqual("Armor", self.armor.name)
        self.assertEqual("Default armor.", self.armor.desc)
        self.assertEqual(0, self.armor.dmg_res)
        self.assertEqual(10, self.armor.rad_res)
        self.assertEqual(2, self.armor.evasion)
        self.assertEqual(10, self.armor.value)
        self.assertEqual(2.5, self.armor.weight)

    def test_obj_as_str_representation(self):
        correct_str_print = "ID: armor, tags: armor, default, name: Armor, description: Default armor., " \
                            "damage resistance: 0, radiation resistance: 10, evasion: 2, value: 10, weight: 2.5"
        self.assertEqual(correct_str_print, self.armor.__str__())


class WeaponTests(unittest.TestCase):

    def test_create_weapon_instance_raises_exception(self):
        with self.assertRaisesRegex(TypeError, "Can't instantiate abstract class .* with abstract methods .*"):
            Weapon(damage="0 + d4", armor_pen=0, accuracy=0, ap_cost=10, st_requirement=1)


class MeleeWeaponTests(unittest.TestCase):

    def setUp(self):
        self.weapon = MeleeWeapon(item_id="melee", tags="weapon, melee, sharp", name="Melee", desc="Default weapon.",
                                  damage="0 + d4", effect="bleed_minor", eff_chance="-6 + d10", armor_pen=0, accuracy=0,
                                  ap_cost=10, st_requirement=1, value=5, weight=1.0)

    def test_property_values(self):
        self.assertEqual("melee", self.weapon.item_id)
        self.assertEqual("weapon, melee, sharp", self.weapon.tags)
        self.assertEqual("Melee", self.weapon.name)
        self.assertEqual("Default weapon.", self.weapon.desc)
        self.assertEqual("0 + d4", self.weapon.damage)
        self.assertEqual("bleed_minor", self.weapon.effect)
        self.assertEqual("-6 + d10", self.weapon.eff_chance)
        self.assertEqual(0, self.weapon.armor_pen)
        self.assertEqual(0, self.weapon.accuracy)
        self.assertEqual(10, self.weapon.ap_cost)
        self.assertEqual(1, self.weapon.st_requirement)
        self.assertEqual(5, self.weapon.value)
        self.assertEqual(1.0, self.weapon.weight)

    def test_damage_range_with_full_damage_formula_multiple_rolls(self):
        weapon = MeleeWeapon(item_id="melee", tags="weapon, melee, sharp", name="Melee", desc="Default weapon.",
                             damage="4 + 2d6", effect="bleed_minor", eff_chance="-6 + d10", armor_pen=0, accuracy=0,
                             ap_cost=10, st_requirement=1, value=5, weight=1.0)
        damage_range = weapon.get_dmg_range()
        self.assertTupleEqual((6, 16), damage_range)

    def test_damage_range_with_full_damage_formula_single_roll(self):
        weapon = MeleeWeapon(item_id="melee", tags="weapon, melee, sharp", name="Melee", desc="Default weapon.",
                             damage="4 + d6", effect="bleed_minor", eff_chance="-6 + d10", armor_pen=0, accuracy=0,
                             ap_cost=10, st_requirement=1, value=5, weight=1.0)
        damage_range = weapon.get_dmg_range()
        self.assertTupleEqual((5, 10), damage_range)

    def test_damage_range_with_multiple_rolls_only(self):
        weapon = MeleeWeapon(item_id="melee", tags="weapon, melee, sharp", name="Melee", desc="Default weapon.",
                             damage="4d6", effect="bleed_minor", eff_chance="-6 + d10", armor_pen=0, accuracy=0,
                             ap_cost=10, st_requirement=1, value=5, weight=1.0)
        damage_range = weapon.get_dmg_range()
        self.assertTupleEqual((4, 24), damage_range)

    def test_damage_range_with_single_roll_only(self):
        weapon = MeleeWeapon(item_id="melee", tags="weapon, melee, sharp", name="Melee", desc="Default weapon.",
                             damage="d6", effect="bleed_minor", eff_chance="-6 + d10", armor_pen=0, accuracy=0,
                             ap_cost=10, st_requirement=1, value=5, weight=1.0)
        damage_range = weapon.get_dmg_range()
        self.assertTupleEqual((1, 6), damage_range)

    def test_effect_chance_in_percents(self):
        self.assertEqual(40, self.weapon.get_effect_chance(),)

    def test_obj_as_str_representation(self):
        correct_str_print = "ID: melee, tags: weapon, melee, sharp, name: Melee, description: Default weapon., " \
                            "damage: 0 + d4 (1 - 4), effect: bleed_minor with -6 + d10 chance (40%), " \
                            "penetration: 0, accuracy: 0, AP: 10, strength required: 1, value: 5, weight: 1.0"
        self.assertEqual(self.weapon.__str__(), correct_str_print)


class RangedWeaponTests(unittest.TestCase):

    def setUp(self):
        self.weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short", name="Gun", desc="Default gun.",
                                   damage="0 + d4", armor_pen=0, accuracy=0, ammo_type="9mm", clip_size=10, ap_cost=10,
                                   st_requirement=1, value=5, weight=1.0)

    def test_property_values(self):
        self.assertEqual("gun", self.weapon.item_id)
        self.assertEqual("weapon, gun, short", self.weapon.tags)
        self.assertEqual("Gun", self.weapon.name)
        self.assertEqual("Default gun.", self.weapon.desc)
        self.assertEqual("0 + d4", self.weapon.damage)
        self.assertEqual(0, self.weapon.armor_pen)
        self.assertEqual(0, self.weapon.accuracy)
        self.assertEqual("9mm", self.weapon.ammo_type)
        self.assertEqual(10, self.weapon.clip_size)
        self.assertEqual(0, self.weapon.current_ammo)
        self.assertEqual(10, self.weapon.ap_cost)
        self.assertEqual(1, self.weapon.st_requirement)
        self.assertEqual(5, self.weapon.value)
        self.assertEqual(1.0, self.weapon.weight)

    def test_damage_range_with_full_damage_formula_multiple_rolls(self):
        weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short", name="Gun", desc="Default gun.",
                              damage="4 + 2d6", armor_pen=0, accuracy=0, ammo_type="9mm", clip_size=10, ap_cost=10,
                              st_requirement=1, value=5, weight=1.0)
        damage_range = weapon.get_dmg_range()
        self.assertTupleEqual((6, 16), damage_range)

    def test_damage_range_with_full_damage_formula_single_roll(self):
        weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short", name="Gun", desc="Default gun.",
                              damage="4 + d6", armor_pen=0, accuracy=0, ammo_type="9mm", clip_size=10, ap_cost=10,
                              st_requirement=1, value=5, weight=1.0)
        damage_range = weapon.get_dmg_range()
        self.assertTupleEqual((5, 10), damage_range)

    def test_damage_range_with_multiple_rolls_only(self):
        weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short", name="Gun", desc="Default gun.", damage="4d6",
                              armor_pen=0, accuracy=0, ammo_type="9mm", clip_size=10, ap_cost=10, st_requirement=1,
                              value=5, weight=1.0)
        damage_range = weapon.get_dmg_range()
        self.assertTupleEqual((4, 24), damage_range)

    def test_damage_range_with_single_roll_only(self):
        weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short", name="Gun", desc="Default gun.", damage="d6",
                              armor_pen=0, accuracy=0, ammo_type="9mm", clip_size=10, ap_cost=10, st_requirement=1,
                              value=5, weight=1.0)
        damage_range = weapon.get_dmg_range()
        self.assertTupleEqual((1, 6), damage_range)

    def test_obj_as_str_representation(self):
        correct_str_print = "ID: gun, tags: weapon, gun, short, name: Gun, description: Default gun., " \
                            "damage: 0 + d4 (1 - 4), penetration: 0, accuracy: 0, ammo: 9mm (0 / 10), AP: 10, " \
                            "strength required: 1, value: 5, weight: 1.0"
        self.assertEqual(correct_str_print, self.weapon.__str__())


class StackableTests(unittest.TestCase):

    def test_create_stackable_instance_raises_exception(self):
        with self.assertRaisesRegex(TypeError, "Can't instantiate abstract class .* with abstract methods .*"):
            Stackable(max_stack=10, current_amount=5)


class AmmoTests(unittest.TestCase):

    def setUp(self):
        self.ammo = Ammo(item_id="ammo", tags="stackable, ammo, default", name="Ammo", desc="Default ammo.",
                         max_stack=50, current_amount=30, value=1, weight=0.01)

    def test_property_values(self):
        self.assertEqual("ammo", self.ammo.item_id)
        self.assertEqual("stackable, ammo, default", self.ammo.tags)
        self.assertEqual("Ammo", self.ammo.name)
        self.assertEqual("Default ammo.", self.ammo.desc)
        self.assertEqual(50, self.ammo.max_stack)
        self.assertEqual(30, self.ammo.current_amount)
        self.assertEqual(1, self.ammo.value)
        self.assertEqual(0.01, self.ammo.weight)

    def test_set_current_amount(self):
        self.ammo.current_amount = 35
        self.assertEqual(35, self.ammo.current_amount)

    def test_set_current_amount_above_max_stack_raises_exception(self):
        with self.assertRaisesRegex(ValueError, "Current amount can't exceed stack maximum .*"):
            self.ammo.current_amount = 70

    def test_set_amount_below_zero_raises_exception(self):
        with self.assertRaisesRegex(ValueError, "Current amount can't be negative!"):
            self.ammo.current_amount = - 5

    def test_obj_as_str_representation(self):
        correct_str_print = "ID: ammo, tags: stackable, ammo, default, name: Ammo, description: Default ammo., " \
                            "amount: 30 / 50, value: 1 (30), weight: 0.01 (0.3)"
        self.assertEqual(correct_str_print, self.ammo.__str__())


class ConsumableTests(unittest.TestCase):

    def setUp(self):
        self.consumable = Consumable(item_id="consumable", tags="stackable, consumable, default", name="Consumable",
                                     desc="Default consumable.", effect="healing", max_stack=5, current_amount=2,
                                     value=10, weight=0.5)

    def test_property_values(self):
        self.assertEqual("consumable", self.consumable.item_id)
        self.assertEqual("stackable, consumable, default", self.consumable.tags)
        self.assertEqual("Consumable", self.consumable.name)
        self.assertEqual("Default consumable.", self.consumable.desc)
        self.assertEqual("healing", self.consumable.effect)
        self.assertEqual(5, self.consumable.max_stack)
        self.assertEqual(2, self.consumable.current_amount)
        self.assertEqual(10, self.consumable.value)
        self.assertEqual(0.5, self.consumable.weight)

    def test_set_current_amount(self):
        self.consumable.current_amount = 4
        self.assertEqual(4, self.consumable.current_amount)

    def test_set_current_amount_above_max_stack_raises_exception(self):
        with self.assertRaisesRegex(ValueError, "Current amount can't exceed stack maximum .*"):
            self.consumable.current_amount = 10

    def test_set_amount_below_zero_raises_exception(self):
        with self.assertRaisesRegex(ValueError, "Current amount can't be negative!"):
            self.consumable.current_amount = - 5

    def test_obj_as_str_representation(self):
        correct_str_print = "ID: consumable, tags: stackable, consumable, default, name: Consumable, " \
                            "description: Default consumable., effect: healing, amount: 2 / 5, value: 10 (20), " \
                            "weight: 0.5 (1.0)"
        self.assertEqual(correct_str_print, self.consumable.__str__())


if __name__ == "__main__":
    unittest.main()
