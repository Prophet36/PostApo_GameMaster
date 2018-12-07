import unittest

from app.items.generic import Armor
from app.items.weapons import RangedWeapon
from app.mechanics.inventory import Inventory


class InventoryTests(unittest.TestCase):

    def setUp(self):
        self.armor = Armor(item_id="armor", tags="armor, test", name="Armor", desc="Test armor.", dmg_res=0, rad_res=10,
                           evasion=2, value=10, weight=2.5)
        self.weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short, test", name="Gun", desc="Test gun.",
                                   damage="2 + 4d6", ammo_type="ammo", clip_size=10, armor_pen=0, accuracy=0,
                                   ap_cost=10, st_requirement=1, value=10, weight=2.0)
        self.inventory = Inventory(armor=self.armor, weapon=self.weapon)

    def test_property_values(self):
        self.assertIsInstance(self.inventory.items, list)
        self.assertEqual(0, len(self.inventory.items))
        self.assertIs(self.armor, self.inventory.equipped_armor)
        self.assertIs(self.weapon, self.inventory.equipped_weapon)

    def test_create_inventory_instance_with_incorrect_obj_types_for_equipped_items_raises_exception(self):
        with self.assertRaisesRegex(Inventory.InventoryError, "Error! Incorrect object .* to create inventory with!"):
            Inventory(armor="not Armor class object", weapon=self.weapon)
        with self.assertRaisesRegex(Inventory.InventoryError, "Error! Incorrect object .* to create inventory with!"):
            Inventory(armor=self.armor, weapon="not Weapon derived class object")

    def test_create_inventory_instance_with_additional_item(self):
        item_to_add = RangedWeapon(item_id="gun", tags="weapon, gun, short, test", name="Pistol", desc="Test pistol.",
                                   damage="2 + 4d6", ammo_type="ammo", clip_size=10, armor_pen=0, accuracy=0,
                                   ap_cost=10, st_requirement=1, value=10, weight=2.0)
        inventory_with_items = Inventory(armor=self.armor, weapon=self.weapon,
                                         items=item_to_add)
        self.assertEqual(1, len(inventory_with_items.items))
        self.assertIs(item_to_add, inventory_with_items.items[0])

    def test_create_inventory_instance_with_incorrect_obj_type_for_additional_item_raises_exception(self):
        with self.assertRaisesRegex(Inventory.InventoryError, "Error! Incorrect object type to add to inventory!"):
            Inventory(armor=self.armor, weapon=self.weapon, items="not Item derived class object")

    def test_create_inventory_instance_with_multiple_additional_items(self):
        item_to_add_1 = RangedWeapon(item_id="gun", tags="weapon, gun, short, test", name="Pistol", desc="Test pistol.",
                                     damage="2 + 4d6", ammo_type="ammo", clip_size=10, armor_pen=0, accuracy=0,
                                     ap_cost=10, st_requirement=1, value=10, weight=2.0)
        item_to_add_2 = RangedWeapon(item_id="gun", tags="weapon, energy, laser, short, test", name="Laser",
                                     desc="Test laser.", damage="2 + 4d6", ammo_type="ammo", clip_size=10, armor_pen=0,
                                     accuracy=0, ap_cost=10, st_requirement=1, value=10, weight=2.0)
        inventory_with_items = Inventory(armor=self.armor, weapon=self.weapon,
                                         items=[item_to_add_1, item_to_add_2])
        self.assertEqual(2, len(inventory_with_items.items))
        self.assertIs(item_to_add_1, inventory_with_items.items[0])
        self.assertIs(item_to_add_2, inventory_with_items.items[1])

    def test_create_inventory_instance_with_incorrect_obj_type_for_multiple_additional_items_raises_exception(self):
        with self.assertRaisesRegex(Inventory.InventoryError, "Error! Incorrect object type to add to inventory!"):
            Inventory(armor=self.armor, weapon=self.weapon, items=["not Item derived class object",
                                                                   "another not Item derived class object"])

    def test_add_item(self):
        item_to_add = RangedWeapon(item_id="gun", tags="weapon, gun, short, test", name="Pistol", desc="Test pistol.",
                                   damage="2 + 4d6", armor_pen=0, accuracy=0, ammo_type="ammo", clip_size=10,
                                   ap_cost=10, st_requirement=1, value=10, weight=2.0)
        self.assertEqual(0, len(self.inventory.items))
        self.inventory.add_item(item_to_add)
        self.assertEqual(1, len(self.inventory.items))
        self.assertIs(item_to_add, self.inventory.items[0])

    def test_add_item_as_incorrect_obj_type_raises_exception(self):
        item_to_add = "not Item derived class object"
        with self.assertRaisesRegex(Inventory.InventoryError, "Error! Incorrect object type to add to inventory!"):
            self.inventory.add_item(item_to_add)

    def test_remove_item_by_reference(self):
        item_to_add = RangedWeapon(item_id="gun", tags="weapon, gun, short, test", name="Pistol", desc="Test pistol.",
                                   damage="2 + 4d6", armor_pen=0, accuracy=0, ammo_type="ammo", clip_size=10,
                                   ap_cost=10, st_requirement=1, value=10, weight=2.0)
        self.inventory.add_item(item_to_add)
        self.assertEqual(1, len(self.inventory.items))
        item_to_remove = self.inventory.items[0]
        self.inventory.remove_item(item_to_remove)
        self.assertEqual(0, len(self.inventory.items))

    def test_remove_item_by_index(self):
        item_to_add = RangedWeapon(item_id="gun", tags="weapon, gun, short, test", name="Gun", desc="Test gun.",
                                   damage="2 + 4d6", armor_pen=0, accuracy=0, ammo_type="ammo", clip_size=10,
                                   ap_cost=10, st_requirement=1, value=10, weight=2.0)
        self.inventory.add_item(item_to_add)
        self.assertEqual(1, len(self.inventory.items))
        self.inventory.remove_item(0)
        self.assertEqual(0, len(self.inventory.items))

    def test_remove_item_by_incorrect_reference_raises_exception(self):
        with self.assertRaisesRegex(Inventory.InventoryError, "Error! This item does not exist in inventory!"):
            self.inventory.remove_item("incorrect_obj_reference")

    def test_remove_item_by_incorrect_index_raises_exception(self):
        with self.assertRaisesRegex(Inventory.InventoryError, "Error! Incorrect inventory index!"):
            self.inventory.remove_item(0)

    def test_remove_item_by_referencing_equipped_item_raises_exception(self):
        with self.assertRaisesRegex(Inventory.InventoryError, "Error! Can't remove currently equipped item!"):
            item_to_remove = self.inventory.equipped_armor
            self.inventory.remove_item(item_to_remove)
        with self.assertRaisesRegex(Inventory.InventoryError, "Error! Can't remove currently equipped item!"):
            item_to_remove = self.inventory.equipped_weapon
            self.inventory.remove_item(item_to_remove)

    def test_obj_as_str_representation(self):
        item_to_add_1 = RangedWeapon(item_id="gun", tags="weapon, gun, short, test", name="Pistol", desc="Test pistol.",
                                     damage="2 + 4d6", ammo_type="ammo", clip_size=10, armor_pen=0, accuracy=0,
                                     ap_cost=10, st_requirement=1, value=10, weight=2.0)
        item_to_add_2 = RangedWeapon(item_id="gun", tags="weapon, energy, laser, short, test", name="Laser",
                                     desc="Test laser.", damage="2 + 4d6", ammo_type="ammo", clip_size=10, armor_pen=0,
                                     accuracy=0, ap_cost=10, st_requirement=1, value=10, weight=2.0)
        self.inventory.add_item(item_to_add_1)
        self.inventory.add_item(item_to_add_2)
        correct_str_print = "Armor: Armor\nWeapon: Gun\nItems:\n1: Pistol\n2: Laser"
        self.assertEqual(correct_str_print, self.inventory.__str__())


if __name__ == "__main__":
    unittest.main()
