import unittest

from app.perks.generic import Perk, CharacterPerk, PlayerTrait, StatusEffect


class PerkTests(unittest.TestCase):

    def test_create_perk_instance_raises_exception(self):
        with self.assertRaisesRegex(TypeError, "Can't instantiate abstract class .* with abstract methods .*"):
            Perk(perk_id="perk", tags="perk, accuracy, test", name="Perk", desc="Test perk.",
                 effects="weapon, gun, short, accuracy, 1; weapon, gun, long, accuracy, -1")


class CharacterPerkTests(unittest.TestCase):

    def setUp(self):
        self.perk = CharacterPerk(perk_id="perk", tags="perk, speed, test", name="Perk", desc="Test perk.",
                                  effects="weapon, short, speed, 1", requirements="attribute, agility, 6")

    def test_property_values(self):
        self.assertEqual("perk", self.perk.perk_id)
        self.assertEqual("perk, speed, test", self.perk.tags)
        self.assertEqual("Perk", self.perk.name)
        self.assertEqual("Test perk.", self.perk.desc)
        self.assertEqual("weapon, short, speed, 1", self.perk.effects)
        self.assertEqual("attribute, agility, 6", self.perk.requirements)

    def test_effects_list_with_multiple_effects(self):
        perk = CharacterPerk(perk_id="perk", tags="perk, speed, test", name="Perk", desc="Test perk.",
                             effects="weapon, short, speed, 1; weapon, shotgun, speed, 1",
                             requirements="attribute, agility, 6")
        correct_effects_list = ["weapon, short, speed, 1", "weapon, shotgun, speed, 1"]
        effects_list = perk.get_effects_list()
        self.assertListEqual(correct_effects_list, effects_list)

    def test_effects_list_with_single_effect(self):
        correct_effects_list = ["weapon, short, speed, 1"]
        effects_list = self.perk.get_effects_list()
        self.assertListEqual(correct_effects_list, effects_list)

    def test_requirements_list_with_multiple_requirements(self):
        perk = CharacterPerk(perk_id="perk", tags="perk, speed, test", name="Perk", desc="Test perk.",
                             effects="weapon, short, speed, 1", requirements="level, 2; attribute, agility, 6")
        correct_requirements_list = ["level, 2", "attribute, agility, 6"]
        requirements_list = perk.get_requirements_list()
        self.assertListEqual(correct_requirements_list, requirements_list)

    def test_requirements_list_with_single_requirement(self):
        correct_requirements_list = ["attribute, agility, 6"]
        requirements_list = self.perk.get_requirements_list()
        self.assertListEqual(correct_requirements_list, requirements_list)

    def test_obj_as_str_representation(self):
        correct_str_print = ("ID: perk, tags: perk, speed, test, name: Perk, description: Test perk., "
                             "effect: weapon, short, speed, 1, requirement: attribute, agility, 6")
        self.assertEqual(correct_str_print, self.perk.__str__())
        perk = CharacterPerk(perk_id="perk", tags="perk, speed, test", name="Perk", desc="Test perk.",
                             effects="weapon, short, speed, 1; weapon, shotgun, speed, 1",
                             requirements="level, 2; attribute, agility, 6")
        correct_str_print = ("ID: perk, tags: perk, speed, test, name: Perk, description: Test perk., "
                             "effects: weapon, short, speed, 1; weapon, shotgun, speed, 1, requirements: level, 2; "
                             "attribute, agility, 6")
        self.assertEqual(correct_str_print, perk.__str__())


class PlayerTraitTests(unittest.TestCase):

    def setUp(self):
        self.trait = PlayerTrait(perk_id="trait", tags="trait, attribute, test", name="Trait", desc="Test trait.",
                                 effects="attribute, strength, -1; attribute, agility, 1", conflicts="opposing_trait")

    def test_property_values(self):
        self.assertEqual("trait", self.trait.perk_id)
        self.assertEqual("trait, attribute, test", self.trait.tags)
        self.assertEqual("Trait", self.trait.name)
        self.assertEqual("Test trait.", self.trait.desc)
        self.assertEqual("attribute, strength, -1; attribute, agility, 1", self.trait.effects)
        self.assertEqual("opposing_trait", self.trait.conflicts)

    def test_effects_list(self):
        correct_effects_list = ["attribute, strength, -1", "attribute, agility, 1"]
        effects_list = self.trait.get_effects_list()
        self.assertListEqual(correct_effects_list, effects_list)

    def test_conflicts_list_with_multiple_conflicts(self):
        trait = PlayerTrait(perk_id="trait", tags="trait, attribute, test", name="Trait", desc="Test trait.",
                            effects="attribute, strength, -1, attribute, agility, 1",
                            conflicts="opposing_trait, another_opposing_trait")
        correct_conflicts_list = ["opposing_trait", "another_opposing_trait"]
        conflicts_list = trait.get_conflicts_list()
        self.assertListEqual(correct_conflicts_list, conflicts_list)

    def test_conflicts_list_with_single_conflict(self):
        correct_conflicts_list = ["opposing_trait"]
        conflicts_list = self.trait.get_conflicts_list()
        self.assertListEqual(correct_conflicts_list, conflicts_list)

    def test_obj_as_str_representation(self):
        correct_str_print = ("ID: trait, tags: trait, attribute, test, name: Trait, description: Test trait., "
                             "effects: attribute, strength, -1; attribute, agility, 1, conflict: opposing_trait")
        self.assertEqual(correct_str_print, self.trait.__str__())
        trait = PlayerTrait(perk_id="trait", tags="trait, attribute, test", name="Trait", desc="Test trait.",
                            effects="attribute, strength, -1; attribute, agility, 1",
                            conflicts="opposing_trait, another_opposing_trait")
        correct_str_print = ("ID: trait, tags: trait, attribute, test, name: Trait, description: Test trait., "
                             "effects: attribute, strength, -1; attribute, agility, 1, conflicts: opposing_trait, "
                             "another_opposing_trait")
        self.assertEqual(correct_str_print, trait.__str__())


class StatusEffectTests(unittest.TestCase):

    def setUp(self):
        self.status_effect = StatusEffect(perk_id="status_effect", tags="status effect, attribute, test",
                                          name="Status Effect", desc="Test status effect.",
                                          effects="attribute, strength, 1", duration=1)

    def test_property_values(self):
        self.assertEqual("status_effect", self.status_effect.perk_id)
        self.assertEqual("status effect, attribute, test", self.status_effect.tags)
        self.assertEqual("Status Effect", self.status_effect.name)
        self.assertEqual("Test status effect.", self.status_effect.desc)
        self.assertEqual("attribute, strength, 1", self.status_effect.effects)
        self.assertEqual(1, self.status_effect.duration)

    def test_effects_list_with_multiple_effects(self):
        status_effect = StatusEffect(perk_id="status_effect", tags="status effect, attribute, test",
                                     name="Status Effect", desc="Test perk.",
                                     effects="attribute, strength, 1; attribute, endurance, 1",
                                     duration=1)
        correct_effects_list = ["attribute, strength, 1", "attribute, endurance, 1"]
        effects_list = status_effect.get_effects_list()
        self.assertListEqual(correct_effects_list, effects_list)

    def test_effects_list_with_single_effect(self):
        correct_effects_list = ["attribute, strength, 1"]
        effects_list = self.status_effect.get_effects_list()
        self.assertListEqual(correct_effects_list, effects_list)

    def test_obj_as_str_representation(self):
        correct_str_print = ("ID: status_effect, tags: status effect, attribute, test, name: Status Effect, "
                             "description: Test status effect., effect: attribute, strength, 1, duration: 1 turn")
        self.assertEqual(correct_str_print, self.status_effect.__str__())
        status_effect = StatusEffect(perk_id="status_effect", tags="status effect, attribute, test",
                                     name="Status Effect", desc="Test status effect.", effects="attribute, strength, 1",
                                     duration=2)
        correct_str_print = ("ID: status_effect, tags: status effect, attribute, test, name: Status Effect, "
                             "description: Test status effect., effect: attribute, strength, 1, duration: 2 turns")
        self.assertEqual(correct_str_print, status_effect.__str__())
        status_effect = StatusEffect(perk_id="status_effect", tags="status effect, attribute, test",
                                     name="Status Effect", desc="Test status effect.", effects="attribute, strength, 1",
                                     duration=-1)
        correct_str_print = ("ID: status_effect, tags: status effect, attribute, test, name: Status Effect, "
                             "description: Test status effect., effect: attribute, strength, 1, duration: permanent")
        self.assertEqual(correct_str_print, status_effect.__str__())


if __name__ == "__main__":
    unittest.main()
