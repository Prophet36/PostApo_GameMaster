import unittest

from app.characters.characters import Human
from app.mechanics.perk_inventory import PerkInventoryPerkAdder
from app.mechanics.stat_calculators import PerkAttributeCalculator, PerkSkillCalculator, PerkDerivedStatCalculator
from app.mechanics.stat_calculators import CharacterAttributeCalculator, CharacterSkillCalculator
from app.mechanics.stat_calculators import StatCalculatorError
from app.perks.perks import PlayerTrait, StatusEffect


class TestPerkAttributeCalculator(unittest.TestCase):

    def setUp(self):
        self.human = Human(name="Human", tags="human, test", level=1, strength=5, endurance=5, agility=5, perception=5,
                           intelligence=5)
        trait = PlayerTrait(perk_id="trait", tags="trait, attribute, test", name="Trait", desc="Test trait.",
                            effects="attribute, strength, -1; attribute, agility, 1", conflicts="conflicting_trait")
        PerkInventoryPerkAdder.add_perk(perk_inv=self.human.perks, perk_to_add=trait)

    def test_get_attribute_bonus(self):
        attribute_bonus = PerkAttributeCalculator.get_attribute_bonus(perk_inv=self.human.perks, attribute="agility")
        self.assertEqual(1, attribute_bonus)

    def test_get_attribute_malus(self):
        attribute_malus = PerkAttributeCalculator.get_attribute_bonus(perk_inv=self.human.perks, attribute="strength")
        self.assertEqual(-1, attribute_malus)

    def test_get_attribute_bonus_from_multiple_perks(self):
        another_trait = PlayerTrait(perk_id="another_trait", tags="trait, attribute, test", name="Trait",
                                    desc="Test trait.", effects="attribute, strength, 1; attribute, agility, 1",
                                    conflicts="conflicting_trait")
        PerkInventoryPerkAdder.add_perk(perk_inv=self.human.perks, perk_to_add=another_trait)
        strength_bonus = PerkAttributeCalculator.get_attribute_bonus(perk_inv=self.human.perks, attribute="strength")
        agility_bonus = PerkAttributeCalculator.get_attribute_bonus(perk_inv=self.human.perks, attribute="agility")
        self.assertEqual(0, strength_bonus)
        self.assertEqual(2, agility_bonus)

    def test_get_incorrect_attribute_bonus_returns_zero(self):
        attribute_bonus = PerkAttributeCalculator.get_attribute_bonus(perk_inv=self.human.perks, attribute="endurance")
        self.assertEqual(0, attribute_bonus)

    def test_incorrect_obj_as_perk_inventory_raises_exception(self):
        with self.assertRaisesRegex(StatCalculatorError, "incorrect object type for perk inventory"):
            PerkAttributeCalculator.get_attribute_bonus(perk_inv="not PerkInventory object", attribute="strength")


class TestPerkSkillCalculator(unittest.TestCase):

    def setUp(self):
        self.human = Human(name="Human", tags="human, test", level=1, strength=5, endurance=5, agility=5, perception=5,
                           intelligence=5)
        trait = PlayerTrait(perk_id="trait", tags="trait, skill, test", name="Trait", desc="Test trait.",
                            effects="skill, guns, -1; skill, melee, 1", conflicts="conflicting_trait")
        PerkInventoryPerkAdder.add_perk(perk_inv=self.human.perks, perk_to_add=trait)

    def test_get_skill_bonus(self):
        skill_bonus = PerkSkillCalculator.get_skill_bonus(perk_inv=self.human.perks, skill="melee")
        self.assertEqual(1, skill_bonus)

    def test_get_skill_malus(self):
        skill_malus = PerkSkillCalculator.get_skill_bonus(perk_inv=self.human.perks, skill="guns")
        self.assertEqual(-1, skill_malus)

    def test_get_skill_bonus_from_multiple_perks(self):
        another_trait = PlayerTrait(perk_id="another_trait", tags="trait, skill, test", name="Trait",
                                    desc="Test trait.", effects="skill, guns, 1; skill, melee, 1",
                                    conflicts="conflicting_trait")
        PerkInventoryPerkAdder.add_perk(perk_inv=self.human.perks, perk_to_add=another_trait)
        guns_bonus = PerkSkillCalculator.get_skill_bonus(perk_inv=self.human.perks, skill="guns")
        melee_bonus = PerkSkillCalculator.get_skill_bonus(perk_inv=self.human.perks, skill="melee")
        self.assertEqual(0, guns_bonus)
        self.assertEqual(2, melee_bonus)

    def test_get_incorrect_skill_bonus_returns_zero(self):
        skill_bonus = PerkSkillCalculator.get_skill_bonus(perk_inv=self.human.perks, skill="energy")
        self.assertEqual(0, skill_bonus)

    def test_incorrect_obj_as_perk_inventory_raises_exception(self):
        with self.assertRaisesRegex(StatCalculatorError, "incorrect object type for perk inventory"):
            PerkSkillCalculator.get_skill_bonus(perk_inv="not PerkInventory object", skill="guns")


class TestPerkDerivedStatCalculator(unittest.TestCase):

    def setUp(self):
        self.human = Human(name="Human", tags="human, test", level=1, strength=5, endurance=5, agility=5, perception=5,
                           intelligence=5)
        status_effect = StatusEffect(perk_id="status_effect", tags="status effect, evasion, test", name="Status Effect",
                                     desc="Test status effect.", effects="evasion, 1", duration=1)
        PerkInventoryPerkAdder.add_perk(perk_inv=self.human.perks, perk_to_add=status_effect)

    def test_get_stat_bonus(self):
        stat_bonus = PerkDerivedStatCalculator.get_stat_bonus(perk_inv=self.human.perks, stat="evasion")
        self.assertEqual(1, stat_bonus)

    def test_get_stat_malus(self):
        another_status_effect = StatusEffect(perk_id="another_status_effect", tags="status effect, evasion, test",
                                             name="Status Effect", desc="Test status effect.",
                                             effects="action_points, -1", duration=1)
        PerkInventoryPerkAdder.add_perk(perk_inv=self.human.perks, perk_to_add=another_status_effect)
        stat_malus = PerkDerivedStatCalculator.get_stat_bonus(perk_inv=self.human.perks, stat="action_points")
        self.assertEqual(-1, stat_malus)

    def test_get_stat_bonus_from_multiple_perks(self):
        another_status_effect = StatusEffect(perk_id="another_status_effect", tags="status effect, evasion, test",
                                             name="Status Effect", desc="Test status effect.", effects="evasion, 1",
                                             duration=1)
        PerkInventoryPerkAdder.add_perk(perk_inv=self.human.perks, perk_to_add=another_status_effect)
        evasion_bonus = PerkDerivedStatCalculator.get_stat_bonus(perk_inv=self.human.perks, stat="evasion")
        self.assertEqual(2, evasion_bonus)

    def test_get_incorrect_stat_bonus_returns_zero(self):
        stat_bonus = PerkDerivedStatCalculator.get_stat_bonus(perk_inv=self.human.perks, stat="health_bonus")
        self.assertEqual(0, stat_bonus)

    def test_incorrect_obj_as_perk_inventory_raises_exception(self):
        with self.assertRaisesRegex(StatCalculatorError, "incorrect object type for perk inventory"):
            PerkDerivedStatCalculator.get_stat_bonus(perk_inv="not PerkInventory object", stat="evasion")


class TestCharacterAttributeCalculator(unittest.TestCase):

    def setUp(self):
        self.human = Human(name="Human", tags="human, test", level=1, strength=5, endurance=5, agility=5, perception=5,
                           intelligence=5)

    def test_get_character_attributes(self):
        self.assertEqual(5, CharacterAttributeCalculator.get_strength(character=self.human))
        self.assertEqual(5, CharacterAttributeCalculator.get_endurance(character=self.human))
        self.assertEqual(5, CharacterAttributeCalculator.get_agility(character=self.human))
        self.assertEqual(5, CharacterAttributeCalculator.get_perception(character=self.human))
        self.assertEqual(5, CharacterAttributeCalculator.get_intelligence(character=self.human))

    def test_get_character_attributes_with_perk_bonuses(self):
        trait = PlayerTrait(perk_id="trait", tags="trait, attribute, test", name="Trait", desc="Test trait.",
                            effects="attribute, strength, -1; attribute, agility, 1", conflicts="conflicting_trait")
        PerkInventoryPerkAdder.add_perk(perk_inv=self.human.perks, perk_to_add=trait)
        self.assertEqual(4, CharacterAttributeCalculator.get_strength(character=self.human))
        self.assertEqual(6, CharacterAttributeCalculator.get_agility(character=self.human))

    def test_incorrect_obj_as_character_raises_exception(self):
        with self.assertRaisesRegex(StatCalculatorError, "incorrect object type for character"):
            CharacterAttributeCalculator.get_strength(character="not Character derived object")


class TestCharacterSkillCalculator(unittest.TestCase):

    def setUp(self):
        self.human = Human(name="Human", tags="human, test", level=1, strength=5, endurance=5, agility=5, perception=5,
                           intelligence=5)

    def test_get_character_skills(self):
        self.assertEqual(1, CharacterSkillCalculator.get_guns(character=self.human))
        self.assertEqual(1, CharacterSkillCalculator.get_energy(character=self.human))
        self.assertEqual(1, CharacterSkillCalculator.get_melee(character=self.human))
        self.assertEqual(1, CharacterSkillCalculator.get_sneak(character=self.human))
        self.assertEqual(1, CharacterSkillCalculator.get_security(character=self.human))
        self.assertEqual(1, CharacterSkillCalculator.get_mechanics(character=self.human))
        self.assertEqual(1, CharacterSkillCalculator.get_survival(character=self.human))
        self.assertEqual(1, CharacterSkillCalculator.get_medicine(character=self.human))

    def test_get_character_skills_with_perk_bonuses(self):
        trait = PlayerTrait(perk_id="trait", tags="trait, skill, test", name="Trait", desc="Test trait.",
                            effects="skill, guns, -1; skill, melee, 1", conflicts="conflicting_trait")
        PerkInventoryPerkAdder.add_perk(perk_inv=self.human.perks, perk_to_add=trait)
        self.assertEqual(0, CharacterSkillCalculator.get_guns(character=self.human))
        self.assertEqual(2, CharacterSkillCalculator.get_melee(character=self.human))

    def test_incorrect_obj_as_character_raises_exception(self):
        with self.assertRaisesRegex(StatCalculatorError, "incorrect object type for character"):
            CharacterSkillCalculator.get_guns(character="not Character derived object")


if __name__ == "__main__":
    unittest.main()
