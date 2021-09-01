import itertools

class Scores(object):
  ONE = 100
  FIVE = 50
  TRIPLE = [0, 1000, 200, 300, 400, 500, 600]
  FOUR_OF = 1000
  FIVE_OF = 2000
  SIX_OF = 3000
  THREE_PAIR = 1500
  STRAIGHT = 2500

def score_dice(dice_counts):
  counts = dice_counts.copy()
  score = 0
  while 6 in counts:
    score += Scores.SIX_OF
    counts[counts.index(6)] = 0
  while counts == [0, 1, 1, 1, 1, 1, 1]:
    score += Scores.STRAIGHT
    counts = [0] * 7
  while 5 in counts:
    score += Scores.FIVE_OF
    counts[counts.index(5)] = 0
  while counts.count(2) >= 3:
    score += Scores.THREE_PAIR
    for _ in range(3):
      counts[counts.index(2)] = 0
  while 4 in counts:
    score += Scores.FOUR_OF
    counts[counts.index(4)] = 0
  while 3 in counts:
    triple_index = counts.index(3)
    score += Scores.TRIPLE[triple_index]
    counts[triple_index] = 0
  score += Scores.ONE * counts[1]
  counts[1] = 0
  score += Scores.FIVE * counts[5]
  counts[5] = 0
  return score, sum(counts)

def should_i_bank(points, dice):
  return points > ((1 - Stats.farkle_chance[dice]) * points) + Stats.ev_dice[dice]

class Stats(object):
  # base cases, we'll fill in the rest below
  # dict keys are the number of dice rolled
  farkle_chance = {0: 1, 1: 2/3}
  ev_dice = {0: 0, 1: 25}

  def __init__(self):
    for n in range(2, 7):
      dice_combos = itertools.product([1, 2, 3, 4, 5, 6], repeat=n)
      combo_count = 6 ** n
      zeroes = 0
      total_ev = 0
      for dice in dice_combos:
        # extra one for index 0, won't be used
        counts = [0] * 7
        for d in dice:
          counts[d] += 1
        score, extra_dice = score_dice(counts)
        if score == 0:
          zeroes += 1
        else:
          # we know we've already generated the stats to do this
          # because we're counting up, and if we didn't farkle,
          # extra_dice must be < n
          if not should_i_bank(score, extra_dice):
            score += self.ev_dice[extra_dice]
        total_ev += score
      self.farkle_chance[n] = zeroes / combo_count
      self.ev_dice[n] = total_ev / combo_count

stats = Stats()
