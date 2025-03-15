import random

class GameLogic:
    @staticmethod
    def generate_numbers(level):
        """Generate random numbers based on difficulty level."""
        ranges = {
            'easy': (1, 3),
            'medium': (3, 6),
            'hard': (6, 9),
            'full': (1, 9)
        }
        min_num, max_num = ranges[level]
        return random.randint(min_num, max_num), random.randint(min_num, max_num)

    @staticmethod
    def check_answer(num1, num2, answer):
        """Check if the answer is correct."""
        return num1 * num2 == answer
