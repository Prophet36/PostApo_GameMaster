import unittest

from app.items.generic import Item, Armor, Weapon
from app.items.weapons import MeleeWeapon, RangedWeapon


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
        self.assertEqual(10, self.weapon.current_ammo)
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
                            "damage: 0 + d4 (1 - 4), penetration: 0, accuracy: 0, ammo: 9mm (10 / 10), AP: 10, " \
                            "strength required: 1, value: 5, weight: 1.0"
        self.assertEqual(correct_str_print, self.weapon.__str__())


if __name__ == "__main__":
    unittest.main()
