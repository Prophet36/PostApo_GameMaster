import unittest

from app.items.factory import ItemFactory
from app.items.generic import Armor
from app.items.stackables import Ammo, Consumable
from app.items.weapons import MeleeWeapon, RangedWeapon


class ItemFactoryTests(unittest.TestCase):

    def test_invalid_item_data_raises_exception(self):
        with self.assertRaisesRegex(ItemFactory.BuildError, "Item data is unavailable!"):
            ItemFactory(data_file="invalid_file.txt")

    def test_create_armor(self):
        armor = ItemFactory(data_file="test_items_correct.txt").create_item("armor")
        self.assertIsInstance(armor, Armor)
        self.assertEqual("armor", armor.item_id)
        self.assertEqual("armor, test", armor.tags)
        self.assertEqual("Armor", armor.name)
        self.assertEqual("Test armor.", armor.desc)
        self.assertEqual(0, armor.dmg_res)
        self.assertEqual(10, armor.rad_res)
        self.assertEqual(2, armor.evasion)
        self.assertEqual(10, armor.value)
        self.assertEqual(2.5, armor.weight)

    def test_create_melee_weapon(self):
        weapon = ItemFactory(data_file="test_items_correct.txt").create_item("melee")
        self.assertIsInstance(weapon, MeleeWeapon)
        self.assertEqual("melee", weapon.item_id)
        self.assertEqual("weapon, melee, sharp, test", weapon.tags)
        self.assertEqual("Melee", weapon.name)
        self.assertEqual("Test melee.", weapon.desc)
        self.assertEqual("2 + 4d6", weapon.damage)
        self.assertEqual("bleed_minor", weapon.effect)
        self.assertEqual("-6 + d10", weapon.eff_chance)
        self.assertEqual(0, weapon.armor_pen)
        self.assertEqual(0, weapon.accuracy)
        self.assertEqual(10, weapon.ap_cost)
        self.assertEqual(1, weapon.st_requirement)
        self.assertEqual(5, weapon.value)
        self.assertEqual(1.0, weapon.weight)

    def test_create_ranged_weapon(self):
        weapon = ItemFactory(data_file="test_items_correct.txt").create_item("gun")
        self.assertIsInstance(weapon, RangedWeapon)
        self.assertEqual("gun", weapon.item_id)
        self.assertEqual("weapon, gun, short, test", weapon.tags)
        self.assertEqual("Gun", weapon.name)
        self.assertEqual("Test gun.", weapon.desc)
        self.assertEqual("2 + 4d6", weapon.damage)
        self.assertEqual(0, weapon.armor_pen)
        self.assertEqual(0, weapon.accuracy)
        self.assertEqual("ammo", weapon.ammo_type)
        self.assertEqual(10, weapon.clip_size)
        self.assertEqual(0, weapon.current_ammo)
        self.assertEqual(10, weapon.ap_cost)
        self.assertEqual(1, weapon.st_requirement)
        self.assertEqual(10, weapon.value)
        self.assertEqual(2.0, weapon.weight)

    def test_create_ammo(self):
        ammo = ItemFactory(data_file="test_items_correct.txt").create_item("ammo")
        self.assertIsInstance(ammo, Ammo)
        self.assertEqual("ammo", ammo.item_id)
        self.assertEqual("ammo, stackable, test", ammo.tags)
        self.assertEqual("Ammo", ammo.name)
        self.assertEqual("Test ammo.", ammo.desc)
        self.assertEqual(50, ammo.max_stack)
        self.assertEqual(50, ammo.current_amount)
        self.assertEqual(1, ammo.value)
        self.assertEqual(0.01, ammo.weight)

    def test_create_consumable(self):
        consumable = ItemFactory(data_file="test_items_correct.txt").create_item("consumable")
        self.assertIsInstance(consumable, Consumable)
        self.assertEqual("consumable", consumable.item_id)
        self.assertEqual("consumable, stackable, test", consumable.tags)
        self.assertEqual("Consumable", consumable.name)
        self.assertEqual("Test consumable.", consumable.desc)
        self.assertEqual("none", consumable.effect)
        self.assertEqual(5, consumable.max_stack)
        self.assertEqual(5, consumable.current_amount)
        self.assertEqual(10, consumable.value)
        self.assertEqual(0.5, consumable.weight)

    def test_invalid_item_id_raises_exception(self):
        with self.assertRaisesRegex(ItemFactory.BuildError, "Can't create .*. Item does not exist!"):
            ItemFactory(data_file="test_items_correct.txt").create_item("invalid_id")

    def test_incorrect_item_data_raises_exception(self):
        with self.assertRaisesRegex(ItemFactory.BuildError, "Can't create .*. Incorrect item data!"):
            ItemFactory(data_file="test_items_incorrect.txt").create_item("incorrect_armor")

    def test_missing_item_data_raises_exception(self):
        with self.assertRaisesRegex(ItemFactory.BuildError, "Can't create .*. Missing item data!"):
            ItemFactory(data_file="test_items_incorrect.txt").create_item("incorrect_melee")

    def test_missing_item_data_due_to_end_of_file_raises_exception(self):
        with self.assertRaisesRegex(ItemFactory.BuildError, "Can't create .*. Missing item data!"):
            ItemFactory(data_file="test_items_incorrect.txt").create_item("incorrect_gun")


if __name__ == "__main__":
    unittest.main()
