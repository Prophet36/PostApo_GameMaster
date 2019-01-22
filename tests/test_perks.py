import unittest

from app.perks.perks import Perk, CharacterPerk, PlayerTrait, StatusEffect


class PerkTests(unittest.TestCase):

    def test_create_perk_instance_raises_exception(self):
        with self.assertRaisesRegex(TypeError, "Can't instantiate abstract class .* with abstract methods .*"):
            Perk(perk_id="perk", tags="perk, ap_cost, -1", name="Perk", desc="Test perk.",
                 effects="weapon, short ap_cost, -1")


class CharacterPerkTests(unittest.TestCase):

    def setUp(self):
        self.perk = CharacterPerk(perk_id="perk", tags="perk, ap_cost", name="Perk", desc="Test perk.",
                                  effects="weapon, short, ap_cost, -1", requirements="attribute, agility, 6")

    def test_property_values(self):
        self.assertEqual("perk", self.perk.perk_id)
        self.assertEqual("perk, ap_cost", self.perk.tags)
        self.assertEqual("Perk", self.perk.name)
        self.assertEqual("Test perk.", self.perk.desc)
        self.assertEqual("weapon, short, ap_cost, -1", self.perk.effects)
        self.assertEqual("attribute, agility, 6", self.perk.requirements)

    def test_effects_list_with_multiple_effects(self):
        perk = CharacterPerk(perk_id="perk", tags="perk, ap_cost", name="Perk", desc="Test perk.",
                             effects="weapon, short, ap_cost, -1; weapon, shotgun, ap_cost, -1",
                             requirements="attribute, agility, 6")
        correct_effects_list = ["weapon, short, ap_cost, -1", "weapon, shotgun, ap_cost, -1"]
        effects_list = perk.get_effects_list()
        self.assertListEqual(correct_effects_list, effects_list)

    def test_effects_list_with_single_effect(self):
        correct_effects_list = ["weapon, short, ap_cost, -1"]
        effects_list = self.perk.get_effects_list()
        self.assertListEqual(correct_effects_list, effects_list)

    def test_requirements_list_with_multiple_requirements(self):
        perk = CharacterPerk(perk_id="perk", tags="perk, ap_cost", name="Perk", desc="Test perk.",
                             effects="weapon, short, ap_cost, -1", requirements="level, 2; attribute, agility, 6")
        correct_requirements_list = ["level, 2", "attribute, agility, 6"]
        requirements_list = perk.get_requirements_list()
        self.assertListEqual(correct_requirements_list, requirements_list)

    def test_requirements_list_with_single_requirement(self):
        correct_requirements_list = ["attribute, agility, 6"]
        requirements_list = self.perk.get_requirements_list()
        self.assertListEqual(correct_requirements_list, requirements_list)

    def test_obj_as_str_representation(self):
        correct_str_print = ("ID: perk, tags: perk, ap_cost, name: Perk, description: Test perk.,\n"
                             "effect: weapon, short, ap_cost, -1, requirement: attribute, agility, 6")
        self.assertEqual(correct_str_print, self.perk.__str__())
        perk = CharacterPerk(perk_id="perk", tags="perk, ap_cost", name="Perk", desc="Test perk.",
                             effects="weapon, short, ap_cost, -1; weapon, shotgun, ap_cost, -1",
                             requirements="level, 2; attribute, agility, 6")
        correct_str_print = ("ID: perk, tags: perk, ap_cost, name: Perk, description: Test perk.,\n"
                             "effects: weapon, short, ap_cost, -1; weapon, shotgun, ap_cost, -1, "
                             "requirements: level, 2; attribute, agility, 6")
        self.assertEqual(correct_str_print, perk.__str__())


class PlayerTraitTests(unittest.TestCase):

    def setUp(self):
        self.trait = PlayerTrait(perk_id="trait", tags="trait, attribute", name="Trait", desc="Test trait.",
                                 effects="attribute, strength, -1; attribute, agility, 1",
                                 conflicts="conflicting_trait")

    def test_property_values(self):
        self.assertEqual("trait", self.trait.perk_id)
        self.assertEqual("trait, attribute", self.trait.tags)
        self.assertEqual("Trait", self.trait.name)
        self.assertEqual("Test trait.", self.trait.desc)
        self.assertEqual("attribute, strength, -1; attribute, agility, 1", self.trait.effects)
        self.assertEqual("conflicting_trait", self.trait.conflicts)

    def test_effects_list(self):
        correct_effects_list = ["attribute, strength, -1", "attribute, agility, 1"]
        effects_list = self.trait.get_effects_list()
        self.assertListEqual(correct_effects_list, effects_list)

    def test_conflicts_list_with_multiple_conflicts(self):
        trait = PlayerTrait(perk_id="trait", tags="trait, attribute", name="Trait", desc="Test trait.",
                            effects="attribute, strength, -1, attribute, agility, 1",
                            conflicts="conflicting_trait, another_conflicting_trait")
        correct_conflicts_list = ["conflicting_trait", "another_conflicting_trait"]
        conflicts_list = trait.get_conflicts_list()
        self.assertListEqual(correct_conflicts_list, conflicts_list)

    def test_conflicts_list_with_single_conflict(self):
        correct_conflicts_list = ["conflicting_trait"]
        conflicts_list = self.trait.get_conflicts_list()
        self.assertListEqual(correct_conflicts_list, conflicts_list)

    def test_obj_as_str_representation(self):
        correct_str_print = ("ID: trait, tags: trait, attribute, name: Trait, description: Test trait.,\n"
                             "effects: attribute, strength, -1; attribute, agility, 1, conflict: conflicting_trait")
        self.assertEqual(correct_str_print, self.trait.__str__())
        trait = PlayerTrait(perk_id="trait", tags="trait, attribute", name="Trait", desc="Test trait.",
                            effects="attribute, strength, -1; attribute, agility, 1",
                            conflicts="conflicting_trait, another_conflicting_trait")
        correct_str_print = ("ID: trait, tags: trait, attribute, name: Trait, description: Test trait.,\n"
                             "effects: attribute, strength, -1; attribute, agility, 1, conflicts: conflicting_trait, "
                             "another_conflicting_trait")
        self.assertEqual(correct_str_print, trait.__str__())


class StatusEffectTests(unittest.TestCase):

    def setUp(self):
        self.status_effect = StatusEffect(perk_id="status_effect", tags="status effect, evasion", name="Status Effect",
                                          desc="Test status effect.", effects="evasion, 1", duration=1)

    def test_property_values(self):
        self.assertEqual("status_effect", self.status_effect.perk_id)
        self.assertEqual("status effect, evasion", self.status_effect.tags)
        self.assertEqual("Status Effect", self.status_effect.name)
        self.assertEqual("Test status effect.", self.status_effect.desc)
        self.assertEqual("evasion, 1", self.status_effect.effects)
        self.assertEqual(1, self.status_effect.duration)

    def test_effects_list_with_multiple_effects(self):
        status_effect = StatusEffect(perk_id="status_effect", tags="status effect, evasion", name="Status Effect",
                                     desc="Test status effect.", effects="evasion, 1; ap_cost, -1", duration=1)
        correct_effects_list = ["evasion, 1", "ap_cost, -1"]
        effects_list = status_effect.get_effects_list()
        self.assertListEqual(correct_effects_list, effects_list)

    def test_effects_list_with_single_effect(self):
        correct_effects_list = ["evasion, 1"]
        effects_list = self.status_effect.get_effects_list()
        self.assertListEqual(correct_effects_list, effects_list)

    def test_lower_duration(self):
        self.assertEqual(1, self.status_effect.duration)
        self.status_effect.lower_duration()
        self.assertEqual(0, self.status_effect.duration)

    def test_lower_duration_to_zero_does_not_lower_it_further(self):
        self.assertEqual(1, self.status_effect.duration)
        self.status_effect.lower_duration()
        self.assertEqual(0, self.status_effect.duration)
        self.status_effect.lower_duration()
        self.assertEqual(0, self.status_effect.duration)

    def test_lower_negative_duration_does_not_lower_it_further(self):
        status_effect = StatusEffect(perk_id="status_effect", tags="status effect, evasion", name="Status Effect",
                                     desc="Test status effect.", effects="evasion, 1", duration=-1)
        self.assertEqual(-1, status_effect.duration)
        self.status_effect.lower_duration()
        self.assertEqual(-1, status_effect.duration)

    def test_obj_as_str_representation(self):
        correct_str_print = ("ID: status_effect, tags: status effect, evasion, name: Status Effect, "
                             "description: Test status effect.,\neffect: evasion, 1, duration: 1 turn")
        self.assertEqual(correct_str_print, self.status_effect.__str__())
        status_effect = StatusEffect(perk_id="status_effect", tags="status effect, evasion", name="Status Effect",
                                     desc="Test status effect.", effects="evasion, 1; ap_cost, -1", duration=2)
        correct_str_print = ("ID: status_effect, tags: status effect, evasion, name: Status Effect, "
                             "description: Test status effect.,\neffects: evasion, 1; ap_cost, -1, duration: 2 turns")
        self.assertEqual(correct_str_print, status_effect.__str__())
        status_effect = StatusEffect(perk_id="status_effect", tags="status effect, evasion", name="Status Effect",
                                     desc="Test status effect.", effects="evasion, 1", duration=-1)
        correct_str_print = ("ID: status_effect, tags: status effect, evasion, name: Status Effect, "
                             "description: Test status effect.,\neffect: evasion, 1, duration: permanent")
        self.assertEqual(correct_str_print, status_effect.__str__())


if __name__ == "__main__":
    unittest.main()
