import random


class RandomRoll:
    """This class contains methods for generating pseudo-random rolls."""

    @staticmethod
    def roll_dice(min_value, max_value):
        """Returns random integer value between specified minimum and maximum (both inclusive).

        :param min_value: minimum random value that can be rolled
        :param max_value: maximum random value that can be rolled
        :raises ValueError: when provided maximum roll value is lower than provided minimum
        :return: random integer between specified minimum and maximum values
        """
        if max_value < min_value:
            raise ValueError("maximum roll value must not be lower than minimum")
        else:
            return random.randint(min_value, max_value)
