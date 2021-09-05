from .conditional_print import con_print

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
  def worth_applying(cls, dice_counts, score, stats):
    total_dice = sum(dice_counts)
    remaining_dice = total_dice - cls.dice_used
    ev_skip = stats.ev_dice(total_dice, score)
    ev_apply = stats.ev_dice(remaining_dice, score + cls.points)
    if ev_apply > ev_skip:
      return True
    else:
      con_print(f"Choosing not to score {cls.__name__}")

  @classmethod
  def test_and_apply(cls, dice_counts, turn_score, score, stats):
    part_score = 0
    while cls.test(dice_counts) and (turn_score == 0 or cls.worth_applying(dice_counts, score + turn_score + part_score, stats)):
      cls.apply(dice_counts)
      part_score += cls.points
      con_print(f"Scoring {cls.__name__}, part score is {part_score}")
    return part_score


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
  Triple5, Triple4, Triple3, Triple2, One, Five
]
# since we always apply the first score type we find (if any),
# make sure the first one is the most valuable (in points per dice)
score_types.sort(key=lambda s: s.points/s.dice_used, reverse=True)

def score_dice(dice_counts, score, stats):
  con_print("Scoring dice:", counts_to_dice(dice_counts))
  turn_score = 0
  counts = dice_counts.copy()
  for score_type in score_types:
    turn_score += score_type.test_and_apply(counts, turn_score, score + turn_score, stats)
  con_print(f"got {turn_score} with {sum(counts)} dice left over")
  return turn_score, sum(counts)

def counts_to_dice(dice_counts):
  dice = []
  for i in range(1, 7):
    dice += [i] * dice_counts[i]
  return dice

def dice_to_counts(dice):
  # extra one for index 0, will be ignored
  counts = [0] * 7
  for d in dice:
    counts[d] += 1
  return counts
