from app.characters.characters import Character
from app.perks.perks import Perk


class CombatCalculatorError(Exception):
    """This exception class exist to unify all errors and exceptions occurring during combat calculations."""
    pass


class DamageCalculator:
    """This class calculates effective potential damage (base weapon and modified by perks) character's equipped weapon
    does to his opponent.

    The class uses CombatCalculatorError exception, which is raised when specified characters, or their weapons or perks
    are incorrect.
    """

    @staticmethod
    def get_weapon_damage(character, opponent):
        """Calculates effective potential damage based on equipped weapon and active perks.

        :param character: Character derived object to calculate damage for
        :param opponent: Character derived object to calculate damage against
        :raises CombatCalculatorError: when specified characters, or their equipped weapons are incorrect
        :return:
        """
        if not isinstance(character, Character):
            raise CombatCalculatorError("incorrect object type for character")
        if not isinstance(opponent, Character):
            raise CombatCalculatorError("incorrect object type for opponent")
        if character.inventory.equipped_weapon is None:
            raise CombatCalculatorError("no weapon equipped on character: {}".format(character.name))
        base_damage = DamageCalculator._get_base_weapon_damage(character=character)
        base_damage += DamageCalculator._get_weapon_type_damage_bonus(character=character)
        base_damage += DamageCalculator._get_opponent_type_damage_bonus(character=character, opponent=opponent)
        effective_damage = DamageCalculator._get_effective_damage(character=character, effective_base_damage=base_damage)
        return effective_damage

    @staticmethod
    def _get_base_weapon_damage(character):
        """Gets equipped weapon's base damage (without roll), unmodified by any perks.

        :param character: Character derived object to get weapon's base damage for
        :return: equipped weapon's base damage
        """
        damage = character.inventory.equipped_weapon.damage
        if "+" in damage:
            base_damage = int(damage.split(" + ")[0])
        else:
            base_damage = 0
        return base_damage

    @staticmethod
    def _get_weapon_type_damage_bonus(character):
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
    def _get_opponent_type_damage_bonus(character, opponent):
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
        """Gets bonus damage provided by provided perk based on matching tags.

        Bonus is provided when set of tags from perk's effects are a subset of provided tags (for example, weapon tags).

        :param perk: Perk derived object to get bonus damage from
        :param tags: tags to compare set of tags from perk effects to
        :return: bonus damage based on perks with qualifying effects
        """
        bonus_damage = 0
        tags = tags.split(", ")
        effects = perk.get_effects_list()
        for effect in effects:
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
