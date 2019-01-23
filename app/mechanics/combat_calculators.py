from app.characters.characters import Character, Critter
from app.items.weapons import MeleeWeapon, RangedWeapon
from app.perks.perks import Perk


class CombatCalculatorError(Exception):
    """This exception class exist to unify all errors and exceptions occurring during combat parameters calculations."""
    pass


class DamageFormulaConverter:
    """This class gets standard damage formulas (damage string formatted as A + XdY, with A + being optional if zero)
    and returns them as tuples (A, X, Y) or calculates minimum and maximum potential damage and returns it as tuple
    (min, max).

    The class uses CombatCalculatorError exception, which is raised when provided damage formula strings are incorrect.
    """

    @staticmethod
    def get_damage_tuple(damage_formula):
        """Converts standard damage formula string into tuple.

        :param damage_formula: standard damage formula string
        :return: tuple of damage formula numbers
        """
        damage_tuple = DamageFormulaConverter._convert_damage_formula(damage_formula=damage_formula)
        return damage_tuple

    @staticmethod
    def get_damage_range(damage_formula):
        """Calculates standard damage formula string to tuple of minimum and maximum potential damage.

        :param damage_formula: standard damage formula string
        :return: tuple of minimum and maximum potential damage numbers
        """
        damage_tuple = DamageFormulaConverter._convert_damage_formula(damage_formula=damage_formula)
        damage_range = DamageFormulaConverter._get_damage_range(damage_tuple=damage_tuple)
        return damage_range

    @staticmethod
    def _convert_damage_formula(damage_formula):
        """Converts standard damage formula string into tuple.

        :param damage_formula: standard damage formula string to convert
        :raises CombatCalculatorError: when provided damage formula string is incorrect
        :return: tuple of damage formula numbers
        """
        try:
            damage_formula = damage_formula.split(" + ")
        except AttributeError:
            raise CombatCalculatorError("incorrect string for damage formula")
        if len(damage_formula) == 1:
            base_damage = 0
            damage_roll = DamageFormulaConverter._convert_damage_roll(damage_roll=damage_formula[0])
        elif len(damage_formula) == 2:
            base_damage = damage_formula[0]
            damage_roll = DamageFormulaConverter._convert_damage_roll(damage_roll=damage_formula[1])
        else:
            raise CombatCalculatorError("incorrect string for damage formula")
        damage_tuple = DamageFormulaConverter._get_damage_tuple(base_damage=base_damage, damage_roll=damage_roll)
        return damage_tuple

    @staticmethod
    def _convert_damage_roll(damage_roll):
        """Converts roll part of standard damage formula string into tuple.

        :param damage_roll: roll part of standard damage formula string
        :raises CombatCalculatorError: when provided damage roll string is incorrect
        :return: tuple of damage roll numbers
        """
        damage_roll = damage_roll.split("d")
        if damage_roll[0] == "":
            number_of_rolls = 1
        else:
            try:
                number_of_rolls = int(damage_roll[0])
            except ValueError:
                raise CombatCalculatorError("incorrect string for damage formula")
        try:
            roll = int(damage_roll[1])
        except ValueError:
            raise CombatCalculatorError("incorrect string for damage formula")
        roll_tuple = (number_of_rolls, roll)
        return roll_tuple

    @staticmethod
    def _get_damage_tuple(base_damage, damage_roll):
        """Combines numbers of standard damage formula string into tuple.

        :param base_damage: base damage part of standard formula string
        :param damage_roll: tuple of damage roll numbers
        :raises CombatCalculatorError: when provided base damage string is incorrect
        :return: tuple of damage formula numbers
        """
        try:
            base_damage = int(base_damage)
        except ValueError:
            raise CombatCalculatorError("incorrect string for damage formula")
        damage_tuple = (base_damage,) + damage_roll
        return damage_tuple

    @staticmethod
    def _get_damage_range(damage_tuple):
        """Calculates minimum and maximum potential damage based on tuple of damage formula numbers.

        :param damage_tuple: tuple of damage formula numbers to calculate from
        :return: tuple of minimum and maximum potential damage
        """
        min_damage = damage_tuple[0] + damage_tuple[1]
        max_damage = damage_tuple[0] + damage_tuple[1] * damage_tuple[2]
        damage_range = (min_damage, max_damage)
        return damage_range


class DamageCalculator:
    """This class calculates effective potential damage (base weapon and modified by perks) character's equipped weapon
    does (with option to calculate damage against specific opponent).

    The class uses CombatCalculatorError exception, which is raised when specified characters, or their weapons or perks
    are incorrect.
    """

    @staticmethod
    def get_weapon_damage(character, opponent=None):
        """Calculates effective potential damage based on equipped weapon and active perks.

        When no opponent character is specified, perks giving bonuses against specific character types will be ignored.

        :param character: Character derived object to calculate damage for
        :param opponent: Character derived object to calculate damage against (defaults to None)
        :raises CombatCalculatorError: when specified characters, or their equipped weapons are incorrect
        :return: effective potential damage
        """
        if not isinstance(character, Character):
            raise CombatCalculatorError("incorrect object type for character")
        if opponent is not None and not isinstance(opponent, Character):
            raise CombatCalculatorError("incorrect object type for opponent")
        if character.inventory.equipped_weapon is None:
            raise CombatCalculatorError("no weapon equipped on character: {}".format(character.name))
        base_damage = DamageCalculator._get_base_weapon_damage(character=character)
        base_damage += DamageCalculator._get_weapon_type_perk_damage_bonus(character=character)
        if opponent is not None:
            base_damage += DamageCalculator._get_opponent_type_perk_damage_bonus(character=character, opponent=opponent)
        effective_damage = DamageCalculator._get_effective_damage(character=character,
                                                                  effective_base_damage=base_damage)
        return effective_damage

    @staticmethod
    def _get_base_weapon_damage(character):
        """Gets equipped weapon's base damage (without roll), unmodified by any perks.

        :param character: Character derived object to get weapon's base damage from
        :return: equipped weapon's base damage
        """
        damage = character.inventory.equipped_weapon.damage
        if "+" in damage:
            base_damage = int(damage.split(" + ")[0])
        else:
            base_damage = 0
        return base_damage

    @staticmethod
    def _get_weapon_type_perk_damage_bonus(character):
        """Calculates bonus damage provided by perks based on type of equipped weapon.

        :param character: Character derived object to calculate bonus damage for
        :return: bonus damage based on weapon type
        """
        bonus_damage = 0
        weapon_tags = character.inventory.equipped_weapon.tags
        for perk in character.perks.perks:
            if not isinstance(perk, Perk):
                raise CombatCalculatorError("incorrect object type for perk")
            if "damage" in perk.tags:
                bonus_damage += DamageCalculator._get_perk_damage_bonus(perk=perk, tags=weapon_tags)
        return bonus_damage

    @staticmethod
    def _get_opponent_type_perk_damage_bonus(character, opponent):
        """Calculates bonus damage provided by perks based on type of opponent.

        :param character: Character derived object to calculate bonus damage for
        :param opponent: Character derived object to calculate bonus damage against
        :return: bonus damage based on opponent type
        """
        bonus_damage = 0
        opponent_tags = opponent.tags
        for perk in character.perks.perks:
            if not isinstance(perk, Perk):
                raise CombatCalculatorError("incorrect object type for perk")
            if "damage" in perk.tags:
                bonus_damage += DamageCalculator._get_perk_damage_bonus(perk=perk, tags=opponent_tags)
        return bonus_damage

    @staticmethod
    def _get_perk_damage_bonus(perk, tags):
        """Gets bonus damage gained by provided perk based on matching tags.

        Bonus is provided when set of tags from perk's effects are a subset of provided tags (for example, weapon tags).

        :param perk: Perk derived object to get bonus damage from
        :param tags: tags to compare set of tags from perk effects to
        :return: bonus damage based on perks with qualifying effects
        """
        bonus_damage = 0
        tags = tags.split(", ")
        effects = perk.get_effects_list()
        for effect in effects:
            if "damage" not in effect:
                continue
            effect = effect.split(", ")
            effect.remove("damage")
            effect_value = int(effect[-1])
            effect.pop(-1)
            if len(effect) > 0 and set(effect) <= set(tags):
                bonus_damage += effect_value
        return bonus_damage

    @staticmethod
    def _get_effective_damage(character, effective_base_damage):
        """Gets effective damage and returns it as standard damage formula.

        :param character: Character derived object to get damage for
        :param effective_base_damage: effective base damage, modified by perks
        :return: effective damage as standard damage formula
        """
        damage_roll = character.inventory.equipped_weapon.damage.split(" + ")[-1]
        effective_damage = str(effective_base_damage) + " + " + damage_roll
        return effective_damage


class AccuracyCalculator:
    """This class calculates effective accuracy (from weapon, stats and modified by perks) the character has when
    attacking with equipped weapon (with option to calculate accuracy against specific opponent).


    The class uses CombatCalculatorError exception, which is raised when specified characters, or their weapons or perks
    are incorrect.
    """

    @staticmethod
    def get_weapon_accuracy(character, opponent=None):
        """Calculates effective accuracy based on equipped weapon and active perks.

        When no opponent character is specified, perks giving bonuses against specific character types will be ignored.

        :param character: Character derived object to calculate accuracy for
        :param opponent: Character derived object to calculate accuracy against
        :raises CombatCalculatorError: when specified characters, or their equipped weapons are incorrect
        :return: effective accuracy
        """
        if not isinstance(character, Character):
            raise CombatCalculatorError("incorrect object type for character")
        if opponent is not None and not isinstance(opponent, Character):
            raise CombatCalculatorError("incorrect object type for opponent")
        if character.inventory.equipped_weapon is None:
            raise CombatCalculatorError("no weapon equipped on character: {}".format(character.name))
        effective_accuracy = AccuracyCalculator._get_weapon_accuracy(character=character)
        effective_accuracy += AccuracyCalculator._get_character_stat_accuracy(character=character)
        effective_accuracy += AccuracyCalculator._get_weapon_type_perk_accuracy_bonus(character=character)
        if opponent is not None:
            effective_accuracy += AccuracyCalculator._get_opponent_type_perk_accuracy_bonus(character=character,
                                                                                            opponent=opponent)
        return effective_accuracy

    @staticmethod
    def _get_weapon_accuracy(character):
        """Gets weapon's inherent accuracy.

        :param character: Character derived object to get equipped weapon's accuracy from
        :return: equipped weapon's accuracy
        """
        accuracy = character.inventory.equipped_weapon.accuracy
        return accuracy

    @staticmethod
    def _get_character_stat_accuracy(character):
        """Gets accuracy from character's stats (attribute and respective skill).

        :param character: Character derived object to get stats for
        :raises CombatCalculatorError: when equipped weapon is incorrect
        :return: accuracy based on character's stats
        """
        weapon = character.inventory.equipped_weapon
        if isinstance(character, Critter):
            return AccuracyCalculator._get_critter_accuracy(critter=character)
        if isinstance(weapon, MeleeWeapon):
            return AccuracyCalculator._get_melee_accuracy(character=character)
        elif isinstance(weapon, RangedWeapon):
            if "gun" in weapon.tags:
                return AccuracyCalculator._get_guns_accuracy(character=character)
            elif "energy" in weapon.tags:
                return AccuracyCalculator._get_energy_accuracy(character=character)
            else:
                raise CombatCalculatorError("incorrect weapon type: {} for character: {}".format(weapon.name,
                                                                                                 character.name))
        else:
            raise CombatCalculatorError("incorrect object type for weapon for character: {}".format(character.name))

    @staticmethod
    def _get_critter_accuracy(critter):
        """Gets accuracy based on critter's stats.

        Critters don't have skills, so their accuracy depends solely on attributes.

        :param critter: Critter object to get stats for
        :return: accuracy based on critter's stats
        """
        accuracy = critter.perception
        return accuracy

    @staticmethod
    def _get_melee_accuracy(character):
        """Gets accuracy for melee weapons based on character's stats.

        :param character: Character derived object to get stats for
        :return: accuracy based on character's stats
        """
        accuracy = character.perception + character.melee
        return accuracy

    @staticmethod
    def _get_guns_accuracy(character):
        """Gets accuracy for guns based on character's stats.

        :param character: Character derived object to get stats for
        :return: accuracy based on character's stats
        """
        accuracy = character.perception + character.guns
        return accuracy

    @staticmethod
    def _get_energy_accuracy(character):
        """Gets accuracy for energy weapons based on character's stats.

        :param character: Character derived object to get stats for
        :return: accuracy based on character's stats
        """
        accuracy = character.perception + character.energy
        return accuracy

    @staticmethod
    def _get_weapon_type_perk_accuracy_bonus(character):
        """Calculates bonus accuracy provided by perks based on type of equipped weapon.

        :param character: Character derived object to calculate bonus accuracy for
        :return: bonus accuracy based on weapon type
        """
        bonus_accuracy = 0
        weapon_tags = character.inventory.equipped_weapon.tags
        for perk in character.perks.perks:
            if not isinstance(perk, Perk):
                raise CombatCalculatorError("incorrect object type for perk")
            if "accuracy" in perk.tags:
                bonus_accuracy += AccuracyCalculator._get_perk_accuracy_bonus(perk=perk, tags=weapon_tags)
        return bonus_accuracy

    @staticmethod
    def _get_opponent_type_perk_accuracy_bonus(character, opponent):
        """Calculates bonus accuracy provided by perks based on type of opponent.

        :param character: Character derived object to calculate bonus accuracy for
        :param opponent: Character derived object to calculate bonus accuracy against
        :return: bonus accuracy based on opponent type
        """
        bonus_accuracy = 0
        opponent_tags = opponent.tags
        for perk in character.perks.perks:
            if not isinstance(perk, Perk):
                raise CombatCalculatorError("incorrect object type for perk")
            if "accuracy" in perk.tags:
                bonus_accuracy += AccuracyCalculator._get_perk_accuracy_bonus(perk=perk, tags=opponent_tags)
        return bonus_accuracy

    @staticmethod
    def _get_perk_accuracy_bonus(perk, tags):
        """Gets bonus accuracy gained by provided perk based on matching tags.

        Bonus is provided when set of tags from perk's effects are a subset of provided tags (for example, weapon tags).

        :param perk: Perk derived object to get bonus accuracy from
        :param tags: tags to compare set of tags from perk effects to
        :return: bonus accuracy based on perks with qualifying effects
        """
        bonus_accuracy = 0
        tags = tags.split(", ")
        effects = perk.get_effects_list()
        for effect in effects:
            if "accuracy" not in effect:
                continue
            effect = effect.split(", ")
            effect.remove("accuracy")
            effect_value = int(effect[-1])
            effect.pop(-1)
            if len(effect) > 0 and set(effect) <= set(tags):
                bonus_accuracy += effect_value
        return bonus_accuracy


class DamageResistanceCalculator:
    """This class calculates effective damage resistance (base armor and modified by perks) character has (with option
    to calculate damage resistance against specific opponent).

    The class uses CombatCalculatorError exception, which is raised when specified characters, or their armor or perks
    are incorrect.
    """

    @staticmethod
    def get_damage_resistance(character, opponent=None):
        """Calculates effective damage resistance based on equipped armor and active perks.

        When no opponent character is specified, perks giving bonuses against specific character types will be ignored.

        :param character: Character derived object to calculate damage resistance for
        :param opponent: Character derived object to calculate damage resistance against (defaults to None)
        :raises CombatCalculatorError: when specified characters, or equipped armor are incorrect
        :return: effective damage resistance
        """
        if not isinstance(character, Character):
            raise CombatCalculatorError("incorrect object type for character")
        if opponent is not None and not isinstance(opponent, Character):
            raise CombatCalculatorError("incorrect object type for opponent")
        if character.inventory.equipped_armor is None:
            raise CombatCalculatorError("no armor equipped on character: {}".format(character.name))
        effective_dmg_res = DamageResistanceCalculator._get_armor_dmg_res(character=character)
        effective_dmg_res += DamageResistanceCalculator._get_generic_perk_dmg_res_bonus(character=character)
        if opponent is not None:
            effective_dmg_res += DamageResistanceCalculator._get_opponent_type_perk_dmg_res_bonus(character=character,
                                                                                                  opponent=opponent)
        return effective_dmg_res

    @staticmethod
    def _get_armor_dmg_res(character):
        """Gets armor's inherent damage resistance.

        :param character: Character derived object to get equipped armor's damage resistance from
        :return: equipped armor's damage resistance
        """
        dmg_res = character.inventory.equipped_armor.dmg_res
        return dmg_res

    @staticmethod
    def _get_generic_perk_dmg_res_bonus(character):
        """Calculates bonus damage resistance provided by generic perks.

        :param character: Character derived object to calculate bonus damage resistance for
        :return: bonus damage resistance
        """
        bonus_dmg_res = 0
        for perk in character.perks.perks:
            if not isinstance(perk, Perk):
                raise CombatCalculatorError("incorrect object type for perk")
            if "dmg_res" in perk.tags:
                bonus_dmg_res += DamageResistanceCalculator._get_perk_dmg_res_bonus(perk=perk, tags="armor")
        return bonus_dmg_res

    @staticmethod
    def _get_opponent_type_perk_dmg_res_bonus(character, opponent):
        """Calculates bonus damage resistance provided by perks based on type of opponent.

        :param character: Character derived object to calculate bonus damage resistance for
        :param opponent: Character derived object to calculate bonus damage resistance against
        :return: bonus damage resistance based on opponent type
        """
        bonus_dmg_res = 0
        opponent_tags = opponent.tags
        for perk in character.perks.perks:
            if not isinstance(perk, Perk):
                raise CombatCalculatorError("incorrect object type for perk")
            if "dmg_res" in perk.tags:
                bonus_dmg_res += DamageResistanceCalculator._get_perk_dmg_res_bonus(perk=perk, tags=opponent_tags)
        return bonus_dmg_res

    @staticmethod
    def _get_perk_dmg_res_bonus(perk, tags):
        """Gets bonus damage resistance gained by provided perk (based on matching tags).

        Bonus is provided when set of tags from perk's effects are a subset of provided tags (for example, opponent
        tags).

        :param perk: Perk derived object to get bonus damage resistance from
        :param tags: tags to compare set of tags from perk effects to
        :return: bonus damage resistance based on perks with qualifying effects
        """
        bonus_dmg_res = 0
        tags = tags.split(", ")
        effects = perk.get_effects_list()
        for effect in effects:
            if "dmg_res" not in effect:
                continue
            effect = effect.split(", ")
            effect.remove("dmg_res")
            effect_value = int(effect[-1])
            effect.pop(-1)
            if len(effect) > 0 and set(effect) <= set(tags):
                bonus_dmg_res += effect_value
        return bonus_dmg_res
