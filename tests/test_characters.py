import unittest

from app.characters.characters import Character, Human, Player, Critter
from app.config.game_config import get_health_bonus_human, get_health_bonus_player
from app.mechanics.inventory import Inventory
from app.mechanics.perk_inventory import PerkInventory


class CharacterTests(unittest.TestCase):

    def test_create_character_instance_raises_exception(self):
        with self.assertRaisesRegex(TypeError, "Can't instantiate abstract class .* with abstract methods .*"):
            Character(name="Character", tags="character, test", level=1, strength=5, endurance=5, agility=5,
                      perception=5, intelligence=5)


class HumanTests(unittest.TestCase):

    def setUp(self):
        self.human = Human(name="Human", tags="human, test", level=1, strength=5, endurance=5, agility=5, perception=5,
                           intelligence=5)

    def test_property_values(self):
        self.assertEqual("Human", self.human.name)
        self.assertEqual("human, test", self.human.tags)
        self.assertEqual(1, self.human.level)
        self.assertEqual(5, self.human.strength)
        self.assertEqual(5, self.human.endurance)
        self.assertEqual(5, self.human.agility)
        self.assertEqual(5, self.human.perception)
        self.assertEqual(5, self.human.intelligence)
        self.assertEqual(1, self.human.guns)
        self.assertEqual(1, self.human.energy)
        self.assertEqual(1, self.human.melee)
        self.assertEqual(1, self.human.sneak)
        self.assertEqual(1, self.human.security)
        self.assertEqual(1, self.human.mechanics)
        self.assertEqual(1, self.human.survival)
        self.assertEqual(1, self.human.medicine)
        self.assertEqual(0, self.human.health)
        health_bonus = get_health_bonus_human()
        self.assertEqual(health_bonus, self.human.health_bonus)
        self.assertEqual(0, self.human.action_points)
        self.assertIsInstance(self.human.inventory, Inventory)
        self.assertIsInstance(self.human.perks, PerkInventory)

    def test_obj_as_str_representation(self):
        correct_str_print = ("name: Human, tags: human, test, level: 1,\nstrength: 5, endurance: 5, agility: 5, "
                             "perception: 5, intelligence: 5,\nguns: 1, energy weapons: 1, melee weapons: 1,\n"
                             "sneak: 1, security: 1, mechanics: 1, survival: 1, medicine: 1")
        self.assertEqual(correct_str_print, self.human.__str__())


class PlayerTests(unittest.TestCase):
    
    def setUp(self):
        self.player = Player(name="Player", tags="human, player, test", level=1, strength=5, endurance=5, agility=5,
                             perception=5, intelligence=5, experience=500)
    
    def test_property_values(self):
        self.assertEqual("Player", self.player.name)
        self.assertEqual("human, player, test", self.player.tags)
        self.assertEqual(1, self.player.level)
        self.assertEqual(5, self.player.strength)
        self.assertEqual(5, self.player.endurance)
        self.assertEqual(5, self.player.agility)
        self.assertEqual(5, self.player.perception)
        self.assertEqual(5, self.player.intelligence)
        self.assertEqual(1, self.player.guns)
        self.assertEqual(1, self.player.energy)
        self.assertEqual(1, self.player.melee)
        self.assertEqual(1, self.player.sneak)
        self.assertEqual(1, self.player.security)
        self.assertEqual(1, self.player.mechanics)
        self.assertEqual(1, self.player.survival)
        self.assertEqual(1, self.player.medicine)
        self.assertEqual(0, self.player.health)
        health_bonus = get_health_bonus_player()
        self.assertEqual(health_bonus, self.player.health_bonus)
        self.assertEqual(0, self.player.action_points)
        self.assertEqual(500, self.player.experience)
        self.assertIsInstance(self.player.inventory, Inventory)
        self.assertIsInstance(self.player.perks, PerkInventory)

    def test_obj_as_str_representation(self):
        correct_str_print = ("name: Player, tags: human, player, test, level: 1, experience: 500,\nstrength: 5, "
                             "endurance: 5, agility: 5, perception: 5, intelligence: 5,\nguns: 1, energy weapons: 1, "
                             "melee weapons: 1,\nsneak: 1, security: 1, mechanics: 1, survival: 1, medicine: 1")
        self.assertEqual(correct_str_print, self.player.__str__())


class CritterTests(unittest.TestCase):

    def setUp(self):
        self.critter = Critter(name="Critter", tags="critter, test", level=1, strength=5, endurance=5, agility=5,
                               perception=5, intelligence=5, health_bonus=10, exp_award=10)

    def test_property_values(self):
        self.assertEqual("Critter", self.critter.name)
        self.assertEqual("critter, test", self.critter.tags)
        self.assertEqual(1, self.critter.level)
        self.assertEqual(5, self.critter.strength)
        self.assertEqual(5, self.critter.endurance)
        self.assertEqual(5, self.critter.agility)
        self.assertEqual(5, self.critter.perception)
        self.assertEqual(5, self.critter.intelligence)
        self.assertEqual(0, self.critter.health)
        self.assertEqual(10, self.critter.health_bonus)
        self.assertEqual(0, self.critter.action_points)
        self.assertEqual(10, self.critter.experience_award)
        self.assertIsInstance(self.critter.inventory, Inventory)
        self.assertIsInstance(self.critter.perks, PerkInventory)

    def test_obj_as_str_representation(self):
        correct_str_print = ("name: Critter, tags: critter, test, level: 1,\nstrength: 5, endurance: 5, "
                             "agility: 5, perception: 5, intelligence: 5,\nexperience award: 10")
        self.assertEqual(correct_str_print, self.critter.__str__())


if __name__ == "__main__":
    unittest.main()
