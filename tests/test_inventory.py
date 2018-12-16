import unittest

from app.items.items import Armor
from app.items.stackables import Ammo
from app.items.weapons import MeleeWeapon, RangedWeapon
from app.mechanics.inventory import Inventory, InventoryItemAdder, InventoryItemRemover
from app.mechanics.inventory import InventoryItemEquipper, InventoryItemUnequipper
from app.mechanics.inventory import InventoryWeaponReloader, InventoryWeaponUnloader
from app.mechanics.inventory import InventoryItemMover


class InventoryTests(unittest.TestCase):

    def setUp(self):
        self.inventory = Inventory()

    def test_property_values(self):
        self.assertIsInstance(self.inventory.items, list)
        self.assertEqual(0, len(self.inventory.items))
        self.assertIsNone(self.inventory.equipped_armor)
        self.assertIsNone(self.inventory.equipped_weapon)

    def test_create_inventory_with_equipped_items(self):
        armor = Armor(item_id="armor", tags="armor, test", name="Armor", desc="Test armor.", dmg_res=0, rad_res=10,
                      evasion=2, value=10, weight=2.5)
        weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short, test", name="Gun", desc="Test gun.",
                              damage="2 + 4d6", ammo_type="ammo", clip_size=10, armor_pen=0, accuracy=0, ap_cost=10,
                              st_requirement=1, value=10, weight=2.0)
        inventory = Inventory(armor=armor, weapon=weapon)
        self.assertIs(armor, inventory.equipped_armor)
        self.assertIs(weapon, inventory.equipped_weapon)

    def test_create_inventory_with_incorrect_obj_types_for_equipped_items_raises_exception(self):
        armor = Armor(item_id="armor", tags="armor, test", name="Armor", desc="Test armor.", dmg_res=0, rad_res=10,
                      evasion=2, value=10, weight=2.5)
        weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short, test", name="Gun", desc="Test gun.",
                              damage="2 + 4d6", ammo_type="ammo", clip_size=10, armor_pen=0, accuracy=0, ap_cost=10,
                              st_requirement=1, value=10, weight=2.0)
        with self.assertRaisesRegex(Inventory.InventoryError, "incorrect object .* to create inventory with"):
            Inventory(armor="not Armor object", weapon=weapon)
        with self.assertRaisesRegex(Inventory.InventoryError, "incorrect object .* to create inventory with"):
            Inventory(armor=armor, weapon="not Weapon derived object")

    def test_obj_as_str_representation(self):
        correct_str_print = "Armor: None\nWeapon: None\nItems:\nNone"
        self.assertEqual(correct_str_print, self.inventory.__str__())

    def test_inventory_with_equipped_items_as_str_representation_(self):
        armor = Armor(item_id="armor", tags="armor, test", name="Armor", desc="Test armor.", dmg_res=0, rad_res=10,
                      evasion=2, value=10, weight=2.5)
        weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short, test", name="Gun", desc="Test gun.",
                              damage="2 + 4d6", ammo_type="ammo", clip_size=10, armor_pen=0, accuracy=0, ap_cost=10,
                              st_requirement=1, value=10, weight=2.0)
        inventory = Inventory(armor=armor, weapon=weapon)
        correct_str_print = "Armor: Armor\nWeapon: Gun\nItems:\nNone"
        self.assertEqual(correct_str_print, inventory.__str__())


class InventoryItemAdderTests(unittest.TestCase):

    def setUp(self):
        armor = Armor(item_id="armor", tags="armor, test", name="Armor", desc="Test armor.", dmg_res=0, rad_res=10,
                      evasion=2, value=10, weight=2.5)
        weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short, test", name="Gun", desc="Test gun.",
                              damage="2 + 4d6", ammo_type="ammo", clip_size=10, armor_pen=0, accuracy=0, ap_cost=10,
                              st_requirement=1, value=10, weight=2.0)
        self.inventory = Inventory(armor=armor, weapon=weapon)

    def test_add_item(self):
        item_to_add = RangedWeapon(item_id="gun", tags="weapon, gun, short, test", name="Pistol", desc="Test pistol.",
                                   damage="2 + 4d6", armor_pen=0, accuracy=0, ammo_type="ammo", clip_size=10,
                                   ap_cost=10, st_requirement=1, value=10, weight=2.0)
        self.assertEqual(0, len(self.inventory.items))
        InventoryItemAdder.add_item(inv=self.inventory, item_to_add=item_to_add)
        self.assertEqual(1, len(self.inventory.items))
        self.assertIs(item_to_add, self.inventory.items[0])

    def test_add_same_type_stackables_merges_stacks_into_sum_of_both_stacks(self):
        stackable_to_add = Ammo(item_id="ammo", tags="ammo, stackable, test", name="Ammo", desc="Test ammo.",
                                max_stack=50, current_amount=30, value=1, weight=0.01)
        additional_stackable_to_add = Ammo(item_id="ammo", tags="ammo, stackable, test", name="Ammo", desc="Test ammo.",
                                           max_stack=50, current_amount=10, value=1, weight=0.01)
        InventoryItemAdder.add_item(inv=self.inventory, item_to_add=stackable_to_add)
        self.assertEqual(1, len(self.inventory.items))
        self.assertEqual(30, self.inventory.items[0].current_amount)
        InventoryItemAdder.add_item(inv=self.inventory, item_to_add=additional_stackable_to_add)
        self.assertEqual(1, len(self.inventory.items))
        self.assertEqual(40, self.inventory.items[0].current_amount)

    def test_add_same_type_stackables_fills_one_stack_leaving_rest_in_other(self):
        stackable_to_add = Ammo(item_id="ammo", tags="ammo, stackable, test", name="Ammo", desc="Test ammo.",
                                max_stack=50, current_amount=30, value=1, weight=0.01)
        additional_stackable_to_add = Ammo(item_id="ammo", tags="ammo, stackable, test", name="Ammo", desc="Test ammo.",
                                           max_stack=50, current_amount=40, value=1, weight=0.01)
        InventoryItemAdder.add_item(inv=self.inventory, item_to_add=stackable_to_add)
        self.assertEqual(1, len(self.inventory.items))
        self.assertEqual(30, self.inventory.items[0].current_amount)
        InventoryItemAdder.add_item(inv=self.inventory, item_to_add=additional_stackable_to_add)
        self.assertEqual(2, len(self.inventory.items))
        self.assertEqual(50, self.inventory.items[0].current_amount)
        self.assertEqual(20, self.inventory.items[1].current_amount)

    def test_add_different_type_stackables(self):
        stackable_to_add = Ammo(item_id="ammo", tags="ammo, stackable, test", name="Ammo", desc="Test ammo.",
                                max_stack=50, current_amount=30, value=1, weight=0.01)
        additional_stackable_to_add = Ammo(item_id="other_ammo", tags="ammo, stackable, test", name="Other Ammo",
                                           desc="Test ammo.", max_stack=50, current_amount=10, value=1, weight=0.01)
        InventoryItemAdder.add_item(inv=self.inventory, item_to_add=stackable_to_add)
        self.assertEqual(1, len(self.inventory.items))
        self.assertEqual(30, self.inventory.items[0].current_amount)
        InventoryItemAdder.add_item(inv=self.inventory, item_to_add=additional_stackable_to_add)
        self.assertEqual(2, len(self.inventory.items))
        self.assertEqual(30, self.inventory.items[0].current_amount)
        self.assertEqual(10, self.inventory.items[1].current_amount)

    def test_add_incorrect_obj_as_item_raises_exception(self):
        with self.assertRaisesRegex(Inventory.InventoryError, "incorrect object type to add to inventory"):
            InventoryItemAdder.add_item(inv=self.inventory, item_to_add="not Item derived object")

    def test_incorrect_obj_as_inventory_raises_exception(self):
        with self.assertRaisesRegex(Inventory.InventoryError, "incorrect object type for inventory"):
            InventoryItemAdder.add_item(inv="not Inventory object", item_to_add="item to add")

    def test_inventory_with_multiple_items_as_str_representation(self):
        ammo = Ammo(item_id="ammo", tags="ammo, stackable, test", name="Ammo", desc="Test ammo.", max_stack=50,
                    current_amount=30, value=1, weight=0.01)
        weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short, test", name="Pistol", desc="Test pistol.",
                              damage="2 + 4d6", armor_pen=0, accuracy=0, ammo_type="ammo", clip_size=10, ap_cost=10,
                              st_requirement=1, value=10, weight=2.0)
        InventoryItemAdder.add_item(inv=self.inventory, item_to_add=ammo)
        InventoryItemAdder.add_item(inv=self.inventory, item_to_add=weapon)
        correct_str_print = "Armor: Armor\nWeapon: Gun\nItems:\n1: Ammo\n2: Pistol"
        self.assertEqual(correct_str_print, self.inventory.__str__())


class InventoryItemRemoverTests(unittest.TestCase):

    def setUp(self):
        armor = Armor(item_id="armor", tags="armor, test", name="Armor", desc="Test armor.", dmg_res=0, rad_res=10,
                      evasion=2, value=10, weight=2.5)
        weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short, test", name="Gun", desc="Test gun.",
                              damage="2 + 4d6", ammo_type="ammo", clip_size=10, armor_pen=0, accuracy=0, ap_cost=10,
                              st_requirement=1, value=10, weight=2.0)
        self.inventory = Inventory(armor=armor, weapon=weapon)

    def test_remove_item(self):
        weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short, test", name="Gun", desc="Test gun.",
                              damage="2 + 4d6", armor_pen=0, accuracy=0, ammo_type="ammo", clip_size=10, ap_cost=10,
                              st_requirement=1, value=10, weight=2.0)
        InventoryItemAdder.add_item(inv=self.inventory, item_to_add=weapon)
        self.assertEqual(1, len(self.inventory.items))
        item_to_remove = self.inventory.items[0]
        InventoryItemRemover.remove_item(inv=self.inventory, item_to_remove=item_to_remove)
        self.assertEqual(0, len(self.inventory.items))

    def test_remove_incorrect_item_raises_exception(self):
        with self.assertRaisesRegex(Inventory.InventoryError, "no such item in inventory"):
            InventoryItemRemover.remove_item(inv=self.inventory, item_to_remove="incorrect item")

    def test_incorrect_obj_as_inventory_raises_exception(self):
        with self.assertRaisesRegex(Inventory.InventoryError, "incorrect object type for inventory"):
            InventoryItemRemover.remove_item(inv="not Inventory object", item_to_remove="item to remove")


class InventoryItemEquipperTests(unittest.TestCase):

    def setUp(self):
        self.armor = Armor(item_id="armor", tags="armor, test", name="Armor", desc="Test armor.", dmg_res=0, rad_res=10,
                           evasion=2, value=10, weight=2.5)
        self.weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short, test", name="Gun", desc="Test gun.",
                                   damage="2 + 4d6", ammo_type="ammo", clip_size=10, armor_pen=0, accuracy=0,
                                   ap_cost=10, st_requirement=1, value=10, weight=2.0)
        self.equippable_armor = Armor(item_id="armor", tags="armor, test", name="Armor", desc="Test armor.", dmg_res=0,
                                      rad_res=10, evasion=2, value=10, weight=2.5)
        self.equippable_weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short, test", name="Gun",
                                              desc="Test gun.", damage="2 + 4d6", ammo_type="ammo", clip_size=10,
                                              armor_pen=0, accuracy=0, ap_cost=10, st_requirement=1, value=10,
                                              weight=2.0)
        self.not_equippable_item = Ammo(item_id="ammo", tags="ammo, stackable, test", name="Ammo", desc="Test ammo.",
                                        max_stack=50, current_amount=50, value=1, weight=0.01)
        self.inventory = Inventory(armor=self.armor, weapon=self.weapon)
        InventoryItemAdder.add_item(inv=self.inventory, item_to_add=self.equippable_armor)
        InventoryItemAdder.add_item(inv=self.inventory, item_to_add=self.equippable_weapon)
        InventoryItemAdder.add_item(inv=self.inventory, item_to_add=self.not_equippable_item)

    def test_equip_new_armor(self):
        item_to_equip = self.inventory.items[0]
        self.assertIs(self.armor, self.inventory.equipped_armor)
        self.assertIs(self.equippable_armor, self.inventory.items[0])
        InventoryItemEquipper.equip_item(inv=self.inventory, item_to_equip=item_to_equip)
        self.assertIs(self.equippable_armor, self.inventory.equipped_armor)
        self.assertIs(self.armor, self.inventory.items[0])

    def test_equip_new_weapon(self):
        item_to_equip = self.inventory.items[1]
        self.assertIs(self.weapon, self.inventory.equipped_weapon)
        self.assertIs(self.equippable_weapon, self.inventory.items[1])
        InventoryItemEquipper.equip_item(inv=self.inventory, item_to_equip=item_to_equip)
        self.assertIs(self.equippable_weapon, self.inventory.equipped_weapon)
        self.assertIs(self.weapon, self.inventory.items[1])

    def test_equip_incorrect_item_type_raises_exception(self):
        item_to_equip = self.inventory.items[2]
        with self.assertRaisesRegex(Inventory.InventoryError, "incorrect object type to equip"):
            InventoryItemEquipper.equip_item(inv=self.inventory, item_to_equip=item_to_equip)

    def test_equip_item_from_outside_current_inventory_raises_exception(self):
        item_to_equip = Armor(item_id="armor", tags="armor, test", name="Armor", desc="Test armor.", dmg_res=0,
                              rad_res=10, evasion=2, value=10, weight=2.5)
        with self.assertRaisesRegex(Inventory.InventoryError, "no such item in inventory"):
            InventoryItemEquipper.equip_item(inv=self.inventory, item_to_equip=item_to_equip)

    def test_incorrect_obj_as_inventory_raises_exception(self):
        with self.assertRaisesRegex(Inventory.InventoryError, "incorrect object type for inventory"):
            InventoryItemEquipper.equip_item(inv="not Inventory object", item_to_equip=self.inventory.items[0])


class InventoryItemUnequipperTests(unittest.TestCase):

    def setUp(self):
        self.armor = Armor(item_id="armor", tags="armor, test", name="Armor", desc="Test armor.", dmg_res=0, rad_res=10,
                           evasion=2, value=10, weight=2.5)
        self.weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short, test", name="Gun", desc="Test gun.",
                                   damage="2 + 4d6", ammo_type="ammo", clip_size=10, armor_pen=0, accuracy=0,
                                   ap_cost=10, st_requirement=1, value=10, weight=2.0)
        self.inventory = Inventory(armor=self.armor, weapon=self.weapon)

    def test_unequip_armor(self):
        self.assertIs(self.armor, self.inventory.equipped_armor)
        InventoryItemUnequipper.unequip_armor(inv=self.inventory)
        self.assertIs(self.armor, self.inventory.items[0])

    def test_unequip_weapon(self):
        self.assertIs(self.weapon, self.inventory.equipped_weapon)
        InventoryItemUnequipper.unequip_weapon(inv=self.inventory)
        self.assertIs(self.weapon, self.inventory.items[0])

    def test_unequip_already_unequipped_armor_raises_exception(self):
        InventoryItemUnequipper.unequip_armor(inv=self.inventory)
        with self.assertRaisesRegex(Inventory.InventoryError, "can't unequip default armor"):
            InventoryItemUnequipper.unequip_armor(inv=self.inventory)

    def test_unequip_already_unequipped_weapon_raises_exception(self):
        InventoryItemUnequipper.unequip_weapon(inv=self.inventory)
        with self.assertRaisesRegex(Inventory.InventoryError, "can't unequip default weapon"):
            InventoryItemUnequipper.unequip_weapon(inv=self.inventory)

    def test_incorrect_obj_as_inventory_raises_exception(self):
        with self.assertRaisesRegex(Inventory.InventoryError, "incorrect object type for inventory"):
            InventoryItemUnequipper.unequip_armor(inv="not Inventory object")
        with self.assertRaisesRegex(Inventory.InventoryError, "incorrect object type for inventory"):
            InventoryItemUnequipper.unequip_weapon(inv="not Inventory object")


class InventoryWeaponReloaderTests(unittest.TestCase):
    def setUp(self):
        armor = Armor(item_id="armor", tags="armor, test", name="Armor", desc="Test armor.", dmg_res=0, rad_res=10,
                      evasion=2, value=10, weight=2.5)
        weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short, test", name="Gun", desc="Test gun.",
                              damage="2 + 4d6", ammo_type="ammo", clip_size=10, armor_pen=0, accuracy=0, ap_cost=10,
                              st_requirement=1, value=10, weight=2.0)
        self.inventory = Inventory(armor=armor, weapon=weapon)

    def test_fully_reload_equipped_weapon(self):
        ammo = Ammo(item_id="ammo", tags="ammo, stackable, test", name="Ammo", desc="Test ammo.", max_stack=50,
                    current_amount=50, value=1, weight=0.01)
        InventoryItemAdder.add_item(inv=self.inventory, item_to_add=ammo)
        self.assertEqual(0, self.inventory.equipped_weapon.current_ammo)
        self.assertEqual(50, self.inventory.items[0].current_amount)
        InventoryWeaponReloader.reload_weapon(inv=self.inventory, weapon_to_reload=self.inventory.equipped_weapon)
        self.assertEqual(10, self.inventory.equipped_weapon.current_ammo)
        self.assertEqual(40, self.inventory.items[0].current_amount)

    def test_partially_reload_equipped_weapon(self):
        ammo = Ammo(item_id="ammo", tags="ammo, stackable, test", name="Ammo", desc="Test ammo.", max_stack=50,
                    current_amount=5, value=1, weight=0.01)
        InventoryItemAdder.add_item(inv=self.inventory, item_to_add=ammo)
        self.assertEqual(0, self.inventory.equipped_weapon.current_ammo)
        self.assertEqual(5, self.inventory.items[0].current_amount)
        InventoryWeaponReloader.reload_weapon(inv=self.inventory, weapon_to_reload=self.inventory.equipped_weapon)
        self.assertEqual(5, self.inventory.equipped_weapon.current_ammo)
        self.assertEqual(0, len(self.inventory.items))

    def test_fully_reload_not_equipped_weapon(self):
        weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short, test", name="Gun", desc="Test gun.",
                              damage="2 + 4d6", ammo_type="ammo", clip_size=10, armor_pen=0, accuracy=0, ap_cost=10,
                              st_requirement=1, value=10, weight=2.0)
        ammo = Ammo(item_id="ammo", tags="ammo, stackable, test", name="Ammo", desc="Test ammo.", max_stack=50,
                    current_amount=50, value=1, weight=0.01)
        InventoryItemAdder.add_item(inv=self.inventory, item_to_add=weapon)
        InventoryItemAdder.add_item(inv=self.inventory, item_to_add=ammo)
        self.assertEqual(0, self.inventory.items[0].current_ammo)
        self.assertEqual(50, self.inventory.items[1].current_amount)
        InventoryWeaponReloader.reload_weapon(inv=self.inventory, weapon_to_reload=self.inventory.items[0])
        self.assertEqual(10, self.inventory.items[0].current_ammo)
        self.assertEqual(40, self.inventory.items[1].current_amount)

    def test_partially_reload_not_equipped_weapon(self):
        weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short, test", name="Gun", desc="Test gun.",
                              damage="2 + 4d6", ammo_type="ammo", clip_size=10, armor_pen=0, accuracy=0, ap_cost=10,
                              st_requirement=1, value=10, weight=2.0)
        ammo = Ammo(item_id="ammo", tags="ammo, stackable, test", name="Ammo", desc="Test ammo.", max_stack=50,
                    current_amount=5, value=1, weight=0.01)
        InventoryItemAdder.add_item(inv=self.inventory, item_to_add=weapon)
        InventoryItemAdder.add_item(inv=self.inventory, item_to_add=ammo)
        self.assertEqual(0, self.inventory.items[0].current_ammo)
        self.assertEqual(5, self.inventory.items[1].current_amount)
        InventoryWeaponReloader.reload_weapon(inv=self.inventory, weapon_to_reload=self.inventory.items[0])
        self.assertEqual(5, self.inventory.items[0].current_ammo)
        self.assertEqual(1, len(self.inventory.items))

    def test_reload_partially_loaded_weapon(self):
        ammo = Ammo(item_id="ammo", tags="ammo, stackable, test", name="Ammo", desc="Test ammo.", max_stack=50,
                    current_amount=5, value=1, weight=0.01)
        InventoryItemAdder.add_item(inv=self.inventory, item_to_add=ammo)
        InventoryWeaponReloader.reload_weapon(inv=self.inventory, weapon_to_reload=self.inventory.equipped_weapon)
        self.assertEqual(5, self.inventory.equipped_weapon.current_ammo)
        additional_ammo = Ammo(item_id="ammo", tags="ammo, stackable, test", name="Ammo", desc="Test ammo.",
                               max_stack=50, current_amount=50, value=1, weight=0.01)
        InventoryItemAdder.add_item(inv=self.inventory, item_to_add=additional_ammo)
        InventoryWeaponReloader.reload_weapon(inv=self.inventory, weapon_to_reload=self.inventory.equipped_weapon)
        self.assertEqual(10, self.inventory.equipped_weapon.current_ammo)
        self.assertEqual(45, self.inventory.items[0].current_amount)

    def test_reload_weapon_with_multiple_ammo_stacks(self):
        ammo = Ammo(item_id="ammo", tags="ammo, stackable, test", name="Ammo", desc="Test ammo.", max_stack=50,
                    current_amount=50, value=1, weight=0.01)
        additional_ammo = Ammo(item_id="ammo", tags="ammo, stackable, test", name="Ammo", desc="Test ammo.",
                               max_stack=50, current_amount=5, value=1, weight=0.01)
        InventoryItemAdder.add_item(inv=self.inventory, item_to_add=ammo)
        InventoryItemAdder.add_item(inv=self.inventory, item_to_add=additional_ammo)
        self.assertEqual(0, self.inventory.equipped_weapon.current_ammo)
        self.assertEqual(50, self.inventory.items[0].current_amount)
        self.assertEqual(5, self.inventory.items[1].current_amount)
        InventoryWeaponReloader.reload_weapon(inv=self.inventory, weapon_to_reload=self.inventory.equipped_weapon)
        self.assertEqual(10, self.inventory.equipped_weapon.current_ammo)
        self.assertEqual(45, self.inventory.items[0].current_amount)
        self.assertEqual(1, len(self.inventory.items))

    def test_reload_fully_loaded_weapon_raises_exception(self):
        ammo = Ammo(item_id="ammo", tags="ammo, stackable, test", name="Ammo", desc="Test ammo.", max_stack=50,
                    current_amount=50, value=1, weight=0.01)
        InventoryItemAdder.add_item(inv=self.inventory, item_to_add=ammo)
        InventoryWeaponReloader.reload_weapon(inv=self.inventory, weapon_to_reload=self.inventory.equipped_weapon)
        with self.assertRaisesRegex(Inventory.InventoryError, "weapon is already fully loaded"):
            InventoryWeaponReloader.reload_weapon(inv=self.inventory, weapon_to_reload=self.inventory.equipped_weapon)

    def test_reload_weapon_with_no_ammo_available_raises_exception(self):
        with self.assertRaisesRegex(Inventory.InventoryError, "no available ammo: .* to reload weapon: .*"):
            InventoryWeaponReloader.reload_weapon(inv=self.inventory, weapon_to_reload=self.inventory.equipped_weapon)

    def test_reload_weapon_from_outside_current_inventory_raises_exception(self):
        weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short, test", name="Gun", desc="Test gun.",
                              damage="2 + 4d6", ammo_type="ammo", clip_size=10, armor_pen=0, accuracy=0, ap_cost=10,
                              st_requirement=1, value=10, weight=2.0)
        with self.assertRaisesRegex(Inventory.InventoryError, "no such weapon in inventory"):
            InventoryWeaponReloader.reload_weapon(inv=self.inventory, weapon_to_reload=weapon)

    def test_reload_incorrect_weapon_type_raises_exception(self):
        with self.assertRaisesRegex(Inventory.InventoryError, "incorrect object type to reload"):
            InventoryWeaponReloader.reload_weapon(inv=self.inventory, weapon_to_reload="weapon to reload")

    def test_reload_weapon_with_incorrect_ammo_type_raises_exception(self):
        incorrect_ammo = RangedWeapon(item_id="ammo", tags="weapon, gun, short, test", name="Ammo",
                                      desc="Test ammo.", damage="2 + 4d6", ammo_type="ammo", clip_size=10,
                                      armor_pen=0, accuracy=0, ap_cost=10, st_requirement=1, value=10, weight=2.0)
        InventoryItemAdder.add_item(inv=self.inventory, item_to_add=incorrect_ammo)
        with self.assertRaisesRegex(Inventory.InventoryError, "incorrect object type for ammo"):
            InventoryWeaponReloader.reload_weapon(inv=self.inventory, weapon_to_reload=self.inventory.equipped_weapon)

    def test_incorrect_obj_as_inventory_raises_exception(self):
        with self.assertRaisesRegex(Inventory.InventoryError, "incorrect object type for inventory"):
            InventoryWeaponReloader.reload_weapon(inv="not Inventory object", weapon_to_reload="weapon to reload")


class InventoryWeaponUnloaderTests(unittest.TestCase):

    def setUp(self):
        armor = Armor(item_id="armor", tags="armor, test", name="Armor", desc="Test armor.", dmg_res=0, rad_res=10,
                      evasion=2, value=10, weight=2.5)
        weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short, test", name="Gun", desc="Test gun.",
                              damage="2 + 4d6", ammo_type="ammo", clip_size=10, armor_pen=0, accuracy=0, ap_cost=10,
                              st_requirement=1, value=10, weight=2.0)
        ammo = Ammo(item_id="ammo", tags="ammo, stackable, test", name="Ammo", desc="Test ammo.", max_stack=50,
                    current_amount=10, value=1, weight=0.01)
        self.inventory = Inventory(armor=armor, weapon=weapon)
        InventoryItemAdder.add_item(inv=self.inventory, item_to_add=ammo)
        InventoryWeaponReloader.reload_weapon(inv=self.inventory, weapon_to_reload=self.inventory.equipped_weapon)

    def test_unload_equipped_weapon(self):
        self.assertEqual(10, self.inventory.equipped_weapon.current_ammo)
        self.assertEqual(0, len(self.inventory.items))
        InventoryWeaponUnloader.unload_weapon(inv=self.inventory, weapon_to_unload=self.inventory.equipped_weapon,
                                              data_file="test_items_correct.txt")
        self.assertEqual(0, self.inventory.equipped_weapon.current_ammo)
        self.assertEqual(1, len(self.inventory.items))
        self.assertEqual(10, self.inventory.items[0].current_amount)

    def test_unload_not_equipped_weapon(self):
        weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short, test", name="Gun", desc="Test gun.",
                              damage="2 + 4d6", ammo_type="ammo", clip_size=10, armor_pen=0, accuracy=0, ap_cost=10,
                              st_requirement=1, value=10, weight=2.0)
        ammo = Ammo(item_id="ammo", tags="ammo, stackable, test", name="Ammo", desc="Test ammo.", max_stack=50,
                    current_amount=10, value=1, weight=0.01)
        InventoryItemAdder.add_item(inv=self.inventory, item_to_add=weapon)
        InventoryItemAdder.add_item(inv=self.inventory, item_to_add=ammo)
        InventoryWeaponReloader.reload_weapon(inv=self.inventory, weapon_to_reload=self.inventory.items[0])
        self.assertEqual(10, self.inventory.items[0].current_ammo)
        self.assertEqual(1, len(self.inventory.items))
        InventoryWeaponUnloader.unload_weapon(inv=self.inventory, weapon_to_unload=self.inventory.items[0],
                                              data_file="test_items_correct.txt")
        self.assertEqual(0, self.inventory.items[0].current_ammo)
        self.assertEqual(2, len(self.inventory.items))
        self.assertEqual(10, self.inventory.items[1].current_amount)

    def test_unload_weapon_with_same_ammo_type_already_in_inventory(self):
        ammo = Ammo(item_id="ammo", tags="ammo, stackable, test", name="Ammo", desc="Test ammo.", max_stack=50,
                    current_amount=30, value=1, weight=0.01)
        InventoryItemAdder.add_item(inv=self.inventory, item_to_add=ammo)
        self.assertEqual(30, self.inventory.items[0].current_amount)
        InventoryWeaponUnloader.unload_weapon(inv=self.inventory, weapon_to_unload=self.inventory.equipped_weapon,
                                              data_file="test_items_correct.txt")
        self.assertEqual(40, self.inventory.items[0].current_amount)

    def test_unload_empty_weapon_raises_exception(self):
        weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short, test", name="Gun", desc="Test gun.",
                              damage="2 + 4d6", ammo_type="ammo", clip_size=10, armor_pen=0, accuracy=0, ap_cost=10,
                              st_requirement=1, value=10, weight=2.0)
        InventoryItemAdder.add_item(inv=self.inventory, item_to_add=weapon)
        with self.assertRaisesRegex(Inventory.InventoryError, "weapon is already unloaded"):
            InventoryWeaponUnloader.unload_weapon(inv=self.inventory, weapon_to_unload=self.inventory.items[0],
                                                  data_file="test_items_correct.txt")

    def test_unload_weapon_from_outside_inventory_raises_exception(self):
        weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short, test", name="Gun", desc="Test gun.",
                              damage="2 + 4d6", ammo_type="ammo", clip_size=10, armor_pen=0, accuracy=0, ap_cost=10,
                              st_requirement=1, value=10, weight=2.0)
        with self.assertRaisesRegex(Inventory.InventoryError, "no such weapon in inventory"):
            InventoryWeaponUnloader.unload_weapon(inv=self.inventory, weapon_to_unload=weapon,
                                                  data_file="test_items_correct.txt")

    def test_unload_incorrect_weapon_type_raises_exception(self):
        weapon = MeleeWeapon(item_id="melee", tags="weapon, melee, sharp, test", name="Melee", desc="Test melee.",
                             damage="2 + 4d6", effect="bleed_minor", eff_chance="-6 + d10", armor_pen=0, accuracy=0,
                             ap_cost=10, st_requirement=1, value=5, weight=1.0)
        InventoryItemAdder.add_item(inv=self.inventory, item_to_add=weapon)
        with self.assertRaisesRegex(Inventory.InventoryError, "incorrect object type to unload"):
            InventoryWeaponUnloader.unload_weapon(inv=self.inventory, weapon_to_unload=self.inventory.items[0],
                                                  data_file="test_items_correct.txt")

    def test_unload_weapon_fails_to_create_ammo_raises_exception(self):
        with self.assertRaisesRegex(Inventory.InventoryError, "incorrect item ID for ammo: .*"):
            InventoryWeaponUnloader.unload_weapon(inv=self.inventory, weapon_to_unload=self.inventory.equipped_weapon,
                                                  data_file="test_items_incorrect.txt")

    def test_incorrect_obj_as_inventory_raises_exception(self):
        with self.assertRaisesRegex(Inventory.InventoryError, "incorrect object type for inventory"):
            InventoryWeaponUnloader.unload_weapon(inv="not Inventory object", weapon_to_unload="weapon to unload",
                                                  data_file="test_items_correct.txt")


class InventoryItemMoverTests(unittest.TestCase):

    def setUp(self):
        armor = Armor(item_id="armor", tags="armor, test", name="Armor", desc="Test armor.", dmg_res=0, rad_res=10,
                      evasion=2, value=10, weight=2.5)
        weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short, test", name="Gun", desc="Test gun.",
                              damage="2 + 4d6", ammo_type="ammo", clip_size=10, armor_pen=0, accuracy=0, ap_cost=10,
                              st_requirement=1, value=10, weight=2.0)
        ammo = Ammo(item_id="ammo", tags="ammo, stackable, test", name="Ammo", desc="Test ammo.", max_stack=50,
                    current_amount=10, value=1, weight=0.01)
        self.inventory_to_move_to = Inventory(armor=armor, weapon=weapon)
        InventoryItemAdder.add_item(inv=self.inventory_to_move_to, item_to_add=ammo)
        another_armor = Armor(item_id="armor", tags="armor, test", name="Armor", desc="Test armor.", dmg_res=0,
                              rad_res=10, evasion=2, value=10, weight=2.5)
        another_weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short, test", name="Gun", desc="Test gun.",
                                      damage="2 + 4d6", ammo_type="ammo", clip_size=10, armor_pen=0, accuracy=0,
                                      ap_cost=10, st_requirement=1, value=10, weight=2.0)
        additional_weapon = RangedWeapon(item_id="gun", tags="weapon, gun, short, test", name="Gun", desc="Test gun.",
                                         damage="2 + 4d6", ammo_type="ammo", clip_size=10, armor_pen=0, accuracy=0,
                                         ap_cost=10, st_requirement=1, value=10, weight=2.0)
        self.inventory_to_move_from = Inventory(armor=another_armor, weapon=another_weapon)
        InventoryItemAdder.add_item(inv=self.inventory_to_move_from, item_to_add=additional_weapon)

    def test_move_item(self):
        self.assertEqual(1, len(self.inventory_to_move_to.items))
        self.assertEqual(1, len(self.inventory_to_move_from.items))
        item_to_move = self.inventory_to_move_from.items[0]
        InventoryItemMover.move_item(inv_to_move_to=self.inventory_to_move_to,
                                     inv_to_move_from=self.inventory_to_move_from, item_to_move=item_to_move)
        self.assertEqual(2, len(self.inventory_to_move_to.items))
        self.assertEqual(0, len(self.inventory_to_move_from.items))
        self.assertIs(item_to_move, self.inventory_to_move_to.items[1])

    def test_move_same_type_stackable_merges_stacks(self):
        ammo = Ammo(item_id="ammo", tags="ammo, stackable, test", name="Ammo", desc="Test ammo.", max_stack=50,
                    current_amount=20, value=1, weight=0.01)
        InventoryItemAdder.add_item(inv=self.inventory_to_move_from, item_to_add=ammo)
        self.assertEqual(1, len(self.inventory_to_move_to.items))
        self.assertEqual(2, len(self.inventory_to_move_from.items))
        self.assertEqual(10, self.inventory_to_move_to.items[0].current_amount)
        item_to_move = self.inventory_to_move_from.items[1]
        InventoryItemMover.move_item(inv_to_move_to=self.inventory_to_move_to,
                                     inv_to_move_from=self.inventory_to_move_from, item_to_move=item_to_move)
        self.assertEqual(1, len(self.inventory_to_move_to.items))
        self.assertEqual(1, len(self.inventory_to_move_from.items))
        self.assertEqual(30, self.inventory_to_move_to.items[0].current_amount)

    def test_move_same_type_stackable_fills_one_stack_leaving_rest_in_other(self):
        ammo = Ammo(item_id="ammo", tags="ammo, stackable, test", name="Ammo", desc="Test ammo.", max_stack=50,
                    current_amount=45, value=1, weight=0.01)
        InventoryItemAdder.add_item(inv=self.inventory_to_move_from, item_to_add=ammo)
        self.assertEqual(1, len(self.inventory_to_move_to.items))
        self.assertEqual(2, len(self.inventory_to_move_from.items))
        self.assertEqual(10, self.inventory_to_move_to.items[0].current_amount)
        item_to_move = self.inventory_to_move_from.items[1]
        InventoryItemMover.move_item(inv_to_move_to=self.inventory_to_move_to,
                                     inv_to_move_from=self.inventory_to_move_from, item_to_move=item_to_move)
        self.assertEqual(2, len(self.inventory_to_move_to.items))
        self.assertEqual(1, len(self.inventory_to_move_from.items))
        self.assertEqual(50, self.inventory_to_move_to.items[0].current_amount)
        self.assertEqual(5, self.inventory_to_move_to.items[1].current_amount)

    def test_move_equipped_armor(self):
        self.assertEqual(1, len(self.inventory_to_move_to.items))
        self.assertEqual(1, len(self.inventory_to_move_from.items))
        item_to_move = self.inventory_to_move_from.equipped_armor
        InventoryItemMover.move_item(inv_to_move_to=self.inventory_to_move_to,
                                     inv_to_move_from=self.inventory_to_move_from, item_to_move=item_to_move)
        self.assertEqual(2, len(self.inventory_to_move_to.items))
        self.assertEqual(1, len(self.inventory_to_move_from.items))
        self.assertIsNot(item_to_move, self.inventory_to_move_from.equipped_armor)
        self.assertIs(item_to_move, self.inventory_to_move_to.items[1])

    def test_move_equipped_weapon(self):
        self.assertEqual(1, len(self.inventory_to_move_to.items))
        self.assertEqual(1, len(self.inventory_to_move_from.items))
        item_to_move = self.inventory_to_move_from.equipped_weapon
        InventoryItemMover.move_item(inv_to_move_to=self.inventory_to_move_to,
                                     inv_to_move_from=self.inventory_to_move_from, item_to_move=item_to_move)
        self.assertEqual(2, len(self.inventory_to_move_to.items))
        self.assertEqual(1, len(self.inventory_to_move_from.items))
        self.assertIsNot(item_to_move, self.inventory_to_move_from.equipped_weapon)
        self.assertIs(item_to_move, self.inventory_to_move_to.items[1])

    def test_move_default_quipped_armor_raises_exception(self):
        self.assertEqual(1, len(self.inventory_to_move_to.items))
        self.assertEqual(1, len(self.inventory_to_move_from.items))
        InventoryItemUnequipper.unequip_armor(inv=self.inventory_to_move_from)
        item_to_move = self.inventory_to_move_from.equipped_armor
        with self.assertRaisesRegex(Inventory.InventoryError, "can't move default armor"):
            InventoryItemMover.move_item(inv_to_move_to=self.inventory_to_move_to,
                                         inv_to_move_from=self.inventory_to_move_from, item_to_move=item_to_move)

    def test_move_default_equipped_weapon_raises_exception(self):
        self.assertEqual(1, len(self.inventory_to_move_to.items))
        self.assertEqual(1, len(self.inventory_to_move_from.items))
        InventoryItemUnequipper.unequip_weapon(inv=self.inventory_to_move_from)
        item_to_move = self.inventory_to_move_from.equipped_weapon
        with self.assertRaisesRegex(Inventory.InventoryError, "can't move default weapon"):
            InventoryItemMover.move_item(inv_to_move_to=self.inventory_to_move_to,
                                         inv_to_move_from=self.inventory_to_move_from, item_to_move=item_to_move)

    def test_move_item_from_outside_inventory_raises_exception(self):
        item_to_move = self.inventory_to_move_to.items[0]
        with self.assertRaisesRegex(Inventory.InventoryError, "no such item in inventory"):
            InventoryItemMover.move_item(inv_to_move_to=self.inventory_to_move_to,
                                         inv_to_move_from=self.inventory_to_move_from, item_to_move=item_to_move)

    def test_same_obj_as_inventories_raises_exception(self):
        with self.assertRaisesRegex(Inventory.InventoryError, "both inventories reference the same object"):
            InventoryItemMover.move_item(inv_to_move_to=self.inventory_to_move_to,
                                         inv_to_move_from=self.inventory_to_move_to, item_to_move="item to move")

    def test_incorrect_obj_as_inventory_raises_exception(self):
        with self.assertRaisesRegex(Inventory.InventoryError, "incorrect object type for inventory"):
            InventoryItemMover.move_item(inv_to_move_to="not Inventory object",
                                         inv_to_move_from=self.inventory_to_move_from, item_to_move="item to move")
        with self.assertRaisesRegex(Inventory.InventoryError, "incorrect object type for inventory"):
            InventoryItemMover.move_item(inv_to_move_to=self.inventory_to_move_to,
                                         inv_to_move_from="not Inventory object", item_to_move="item to move")


if __name__ == "__main__":
    unittest.main()
