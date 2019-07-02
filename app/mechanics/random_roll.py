import random


class RandomRoll:
    """This class contains methods for generating pseudo-random rolls."""

    @staticmethod
    def roll_dice(min_value, max_value, number_of_rolls=1):
        """Returns random integer value between specified minimum and maximum (both inclusive).

        If number of rolls is specified and is greater than 1, sum of independent random rolls is returned.

        :param min_value: minimum random value that can be rolled
        :param max_value: maximum random value that can be rolled
        :param number_of_rolls: number of random rolls, defaults to 1
        :raises ValueError: when provided maximum roll value is lower than provided minimum or number of rolls is lower
                            than 1
        :return: sum of random integers between specified minimum and maximum values
        """
        if max_value < min_value:
            raise ValueError("maximum roll value must not be lower than minimum")
        if not isinstance(number_of_rolls, int) or number_of_rolls < 1:
            raise ValueError("number of rolls must not be lower than 1")
        total_roll = 0
        for roll in range(number_of_rolls):
            total_roll += random.randint(min_value, max_value)
        return total_roll
