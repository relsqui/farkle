from .stats import Stats
from .conditional_print import print_condition, set_print_condition, con_print

class ScoreType(object):
  points = None
  dice_used = None

  @classmethod
  def test(cls, dice_counts):
    raise NotImplementedError

  @classmethod
  def apply(cls, dice_counts):
    raise NotImplementedError

  @classmethod
  def should_i_apply(cls, dice_counts):
    total_dice = sum(dice_counts)
    remaining_dice = total_dice - cls.dice_used
    ev_skip = Stats.ev_dice[total_dice]
    ev_apply = ((1 - Stats.farkle_chance[remaining_dice]) * cls.points) + Stats.ev_dice[remaining_dice]
    if ev_apply > ev_skip:
      return True
    else:
      con_print(f"Choosing not to score {cls.__name__}")

  @classmethod
  def test_and_apply(cls, dice_counts, score):
    while cls.test(dice_counts) and (score == 0 or cls.should_i_apply(dice_counts)):
      con_print(f"Scoring {cls.__name__}")
      cls.apply(dice_counts)
      score += cls.points
    return score


class SixOfAKind(ScoreType):
  points = 3000
  dice_used = 6

  @classmethod
  def test(cls, dice_counts):
    return 6 in dice_counts

  @classmethod
  def apply(cls, dice_counts):
    dice_counts[dice_counts.index(6)] = 0


class Straight(ScoreType):
  points = 2500
  dice_used = 6

  @classmethod
  def test(cls, dice_counts):
    return dice_counts == [0, 1, 1, 1, 1, 1, 1]

  @classmethod
  def apply(cls, dice_counts):
    # we want to modify the referenced object here,
    # not reassign the reference
    for i in range(len(dice_counts)):
      dice_counts[i] = 0


class FiveOfAKind(ScoreType):
  points = 2000
  dice_used = 5

  @classmethod
  def test(cls, dice_counts):
    return 5 in dice_counts

  @classmethod
  def apply(cls, dice_counts):
    dice_counts[dice_counts.index(5)] = 0


class ThreePair(ScoreType):
  points = 1500
  dice_used = 6

  @classmethod
  def test(cls, dice_counts):
    return dice_counts.count(2) == 3

  @classmethod
  def apply(cls, dice_counts):
    for _ in range(3):
      dice_counts[dice_counts.index(2)] = 0

class FourOfAKind(ScoreType):
  points = 1000
  dice_used = 4

  @classmethod
  def test(cls, dice_counts):
    return 4 in dice_counts

  @classmethod
  def apply(cls, dice_counts):
    dice_counts[dice_counts.index(4)] = 0


class Triple1(ScoreType):
  points = 1000
  dice_used = 3

  @classmethod
  def test(cls, dice_counts):
    return dice_counts[1] == 3

  @classmethod
  def apply(cls, dice_counts):
    dice_counts[1] = 0


class Triple6(ScoreType):
  points = 600
  dice_used = 3

  @classmethod
  def test(cls, dice_counts):
    return dice_counts[6] == 3

  @classmethod
  def apply(cls, dice_counts):
    dice_counts[6] = 0


class Triple5(ScoreType):
  points = 500
  dice_used = 3

  @classmethod
  def test(cls, dice_counts):
    return dice_counts[5] == 3

  @classmethod
  def apply(cls, dice_counts):
    dice_counts[5] = 0


class Triple4(ScoreType):
  points = 400
  dice_used = 3

  @classmethod
  def test(cls, dice_counts):
    return dice_counts[4] == 3

  @classmethod
  def apply(cls, dice_counts):
    dice_counts[4] = 0


class Triple3(ScoreType):
  points = 300
  dice_used = 3

  @classmethod
  def test(cls, dice_counts):
    return dice_counts[3] == 3

  @classmethod
  def apply(cls, dice_counts):
    dice_counts[3] = 0


class Triple2(ScoreType):
  points = 200
  dice_used = 3

  @classmethod
  def test(cls, dice_counts):
    return dice_counts[2] == 3

  @classmethod
  def apply(cls, dice_counts):
    dice_counts[2] = 0


class One(ScoreType):
  points = 100
  dice_used = 1

  @classmethod
  def test(cls, dice_counts):
    return dice_counts[1] > 0

  @classmethod
  def apply(cls, dice_counts):
    dice_counts[1] -= 1


class Five(ScoreType):
  points = 50
  dice_used = 1

  @classmethod
  def test(cls, dice_counts):
    return dice_counts[5] > 0

  @classmethod
  def apply(cls, dice_counts):
    dice_counts[5] -= 1


score_types = [
  SixOfAKind, Straight, FiveOfAKind, ThreePair, FourOfAKind, Triple1, Triple6,
  Triple5, Triple4, Triple3, Triple2, Triple1, One, Five
]

def score_dice(dice_counts, score):
  con_print("Scoring dice:", counts_to_dice(dice_counts))
  counts = dice_counts.copy()
  for score_type in score_types:
    score = score_type.test_and_apply(counts, score)
  return score, sum(counts)

def counts_to_dice(dice_counts):
  dice = []
  for i in range(1, 7):
    dice += [i] * dice_counts[i]
  return dice
