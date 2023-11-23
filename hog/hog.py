"""The Game of Hog."""

from typing import Final, Callable, TypeAlias, ParamSpec
from dice import Dice
from dice import six_sided, make_test_dice
from ucb import main, trace, interact

GOAL: Final[int] = 100  # The goal of Hog is to score 100 points.
UpdateMethod: TypeAlias = Callable[[int, int, int, Dice], int]
Strategy: TypeAlias = Callable[[int, int], int]

######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls: int, dice: Dice = six_sided) -> int:
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    Args:
        num_rolls: The number of dice rolls that will be made.
        dice: A function that simulates a single dice roll outcome.

    Returns:
        The sum of the outcomes, or 1 if any of the outcomes is 1.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert isinstance(num_rolls, int), 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    results = [dice() for _ in range(num_rolls)]
    if 1 in results:
        return 1
    return sum(results)
    # END PROBLEM 1


def boar_brawl(player_score: int, opponent_score: int) -> int:
    """Return the points scored by rolling 0 dice according to Boar Brawl.

    Args:
        player_score: The total score of the current player.
        opponent_score: The total score of the other player.

    Returns:
        The points scored by rolling 0 dice.
    """
    # BEGIN PROBLEM 2
    return max(1, 3 * abs(opponent_score // 10 % 10 - player_score % 10))
    # END PROBLEM 2


def take_turn(num_rolls: int, player_score: int, opponent_score: int, dice: Dice = six_sided) -> int:
    """Return the points scored on a turn rolling NUM_ROLLS dice when the
    player has PLAYER_SCORE points and the opponent has OPPONENT_SCORE points.

    Args:
        num_rolls: The number of dice rolls that will be made.
        player_score: The total score of the current player.
        opponent_score: The total score of the other player.
        dice: A function that simulates a single dice roll outcome.

    Returns:
        The points scored on the turn.
    """
    # Leave these assert statements here; they help check for errors.
    assert isinstance(num_rolls, int), 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    # BEGIN PROBLEM 3
    if num_rolls == 0:
        return boar_brawl(player_score, opponent_score)
    return roll_dice(num_rolls, dice)
    # END PROBLEM 3


def simple_update(num_rolls: int, player_score: int, opponent_score: int,
                  dice: Dice = six_sided) -> int:
    """Return the total score of a player who starts their turn with
    PLAYER_SCORE and then rolls NUM_ROLLS DICE, ignoring Sus Fuss.

    Args:
        num_rolls: The number of dice rolls that will be made.
        player_score: The total score of the current player.
        opponent_score: The total score of the other player.
        dice: A function that simulates a single dice roll outcome.

    Returns:
        The total score of the player after the turn.
    """
    score = player_score + take_turn(num_rolls, player_score, opponent_score, dice)
    return score


def is_prime(n: int) -> bool:
    """Return whether N is prime."""
    if n == 1:
        return False
    k = 2
    while k < n:
        if n % k == 0:
            return False
        k += 1
    return True


def num_factors(n: int) -> int:
    """Return the number of factors of N, including 1 and N itself."""
    # BEGIN PROBLEM 4
    factor_num = 1
    prime_factor = 1
    while n > 1:
        prime_factor += 1
        while prime_factor <= n and not is_prime(prime_factor):
            prime_factor += 1
        if prime_factor > n:
            break
        current_exp = 0
        while n % prime_factor == 0:
            n //= prime_factor
            current_exp += 1
        factor_num *= current_exp + 1
    return factor_num
    # END PROBLEM 4


def sus_points(score: int) -> int:
    """Return the new score of a player taking into account the Sus Fuss rule.

    Args:
        score: The current score of the player.

    Returns:
        The new score of the player after applying the Sus Fuss rule.
    """
    # BEGIN PROBLEM 4
    if num_factors(score) in [3, 4]:
        while not is_prime(score):
            score += 1
    return score
    # END PROBLEM 4


def sus_update(num_rolls: int, player_score: int, opponent_score: int,
               dice: Dice = six_sided) -> int:
    """Return the total score of a player who starts their turn with
    PLAYER_SCORE and then rolls NUM_ROLLS DICE, *including* Sus Fuss.

    Args:
        num_rolls: The number of dice rolls that will be made.
        player_score: The total score of the current player.
        opponent_score: The total score of the other player.
        dice: A function that simulates a single dice roll outcome.

    Returns:
        The total score of the player after the turn.
    """
    # BEGIN PROBLEM 4
    points = take_turn(num_rolls, player_score, opponent_score, dice)
    return sus_points(player_score + points)
    # END PROBLEM 4


def always_roll_5(score: int, opponent_score: int) -> int:
    """A strategy of always rolling 5 dice, regardless of the player's score or
    the opponent's score.
    """
    return 5


def play(strategy0: Strategy, strategy1: Strategy, update: UpdateMethod,
         score0: int = 0, score1: int = 0,
         dice: Dice = six_sided, goal: int = GOAL) -> tuple[int, int]:
    """Simulate a game and return the final scores of both players, with
    Player 0's score first and Player 1's score second.

    E.g., play(always_roll_5, always_roll_5, sus_update) simulates a game in
    which both players always choose to roll 5 dice on every turn and the Sus
    Fuss rule is in effect.

    A strategy function, such as always_roll_5, takes the current player's
    score and their opponent's score and returns the number of dice the current
    player chooses to roll.

    An update function, such as sus_update or simple_update, takes the number
    of dice to roll, the current player's score, the opponent's score, and the
    dice function used to simulate rolling dice. It returns the updated score
    of the current player after they take their turn.

    Args:
        strategy0: The strategy for player0.
        strategy1: The strategy for player1.
        update: The update function (used for both players).
        score0: Starting score for Player 0
        score1: Starting score for Player 1
        dice: A function of zero arguments that simulates a dice roll.
        goal: The game ends and someone wins when this score is reached.

    Returns:
        The final scores for both players in a tuple.
    """
    who = 0  # Who is about to take a turn, 0 (first) or 1 (second)
    # BEGIN PROBLEM 5
    scores = [score0, score1]
    strategies = [strategy0, strategy1]
    while scores[0] < goal and scores[1] < goal:
        num_rolls = strategies[who](scores[who], scores[1 - who])
        scores[who] = update(num_rolls, scores[who], scores[1 - who], dice)
        who = 1 - who
    score0, score1 = scores
    # END PROBLEM 5
    return score0, score1


#######################
# Phase 2: Strategies #
#######################


def always_roll(n: int) -> Strategy:
    """Return a player strategy that always rolls N dice.

    A player strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(3)
    >>> strategy(0, 0)
    3
    >>> strategy(99, 99)
    3
    """
    assert n >= 0 and n <= 10
    # BEGIN PROBLEM 6
    "*** YOUR CODE HERE ***"
    return lambda score, opponent_score: n
    # END PROBLEM 6


def catch_up(score: int, opponent_score: int) -> int:
    """A player strategy that always rolls 5 dice unless the opponent
    has a higher score, in which case 6 dice are rolled.

    >>> catch_up(9, 4)
    5
    >>> strategy(17, 18)
    6
    """
    if score < opponent_score:
        return 6  # Roll one more to catch up
    else:
        return 5


def is_always_roll(strategy: Strategy, goal: int = GOAL) -> bool:
    """Return whether STRATEGY always chooses the same number of dice to roll
    given a game that goes to GOAL points.

    >>> is_always_roll(always_roll_5)
    True
    >>> is_always_roll(always_roll(3))
    True
    >>> is_always_roll(catch_up)
    False
    """
    # BEGIN PROBLEM 7
    "*** YOUR CODE HERE ***"
    res = strategy(0, 0)
    return all(strategy(i, j) == res for i in range(goal) for j in range(goal))
    # END PROBLEM 7


_P = ParamSpec('_P')

def make_averaged(original_function: Callable[_P, float],
                  samples_count: int = 1000) -> Callable[_P, float]:
    """Return a function that returns the average value of ORIGINAL_FUNCTION
    called SAMPLES_COUNT times.

    To implement this function, you will have to use *args syntax.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(roll_dice, 40)
    >>> averaged_dice(1, dice)  # The avg of 10 4's, 10 2's, 10 5's, and 10 1's
    3.0
    """
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    def averaged(*args: _P.args, **kwargs: _P.kwargs) -> float:
        results = (original_function(*args, **kwargs) for _ in range(samples_count))
        res = sum(results)
        return res / samples_count
    return averaged
    # END PROBLEM 8


def max_scoring_num_rolls(dice=six_sided, samples_count=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn score
    by calling roll_dice with the provided DICE a total of SAMPLES_COUNT times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    # END PROBLEM 9


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1, sus_update)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(6)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    six_sided_max = max_scoring_num_rolls(six_sided)
    print('Max scoring num rolls for six-sided dice:', six_sided_max)

    print('always_roll(6) win rate:', average_win_rate(always_roll(6))) # near 0.5
    print('catch_up win rate:', average_win_rate(catch_up))
    print('always_roll(3) win rate:', average_win_rate(always_roll(3)))
    print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    print('boar_strategy win rate:', average_win_rate(boar_strategy))
    print('sus_strategy win rate:', average_win_rate(sus_strategy))
    print('final_strategy win rate:', average_win_rate(final_strategy))
    "*** You may add additional experiments as you wish ***"



def boar_strategy(score, opponent_score, threshold=11, num_rolls=6):
    """This strategy returns 0 dice if Boar Brawl gives at least THRESHOLD
    points, and returns NUM_ROLLS otherwise. Ignore score and Sus Fuss.
    """
    # BEGIN PROBLEM 10
    return num_rolls  # Remove this line once implemented.
    # END PROBLEM 10


def sus_strategy(score, opponent_score, threshold=11, num_rolls=6):
    """This strategy returns 0 dice when your score would increase by at least threshold."""
    # BEGIN PROBLEM 11
    return num_rolls  # Remove this line once implemented.
    # END PROBLEM 11


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN PROBLEM 12
    return 6  # Remove this line once implemented.
    # END PROBLEM 12


##########################
# Command Line Interface #
##########################

# NOTE: The function in this section does not need to be changed. It uses
# features of Python not yet covered in the course.

@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()