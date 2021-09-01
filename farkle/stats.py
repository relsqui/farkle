import itertools

from .conditional_print import set_print_condition

class Stats(object):
  # base cases, we'll fill in the rest below
  # dict keys are the number of dice rolled
  farkle_chance = {0: 1, 1: 2/3}
  ev_dice = {0: 0, 1: 25}

  @classmethod
  def initialize(self, score_dice, watch=()):
    for n in range(2, 7):
      dice_combos = itertools.product([1, 2, 3, 4, 5, 6], repeat=n)
      combo_count = 6 ** n
      zeroes = 0
      total_ev = 0
      for dice in dice_combos:
        set_print_condition(dice == watch)
        # extra one for index 0, won't be used
        counts = [0] * 7
        for d in dice:
          counts[d] += 1
        score, extra_dice = score_dice(counts, 0)
        if score == 0:
          zeroes += 1
        else:
          # we know we've already generated the stats to do this
          # because we're counting up, and if we didn't farkle,
          # extra_dice must be < n
          if not self.should_i_bank(score, extra_dice):
            score += self.ev_dice[extra_dice]
        total_ev += score
      self.farkle_chance[n] = zeroes / combo_count
      self.ev_dice[n] = total_ev / combo_count

  @classmethod
  def should_i_bank(self, points, dice):
    return points > ((1 - Stats.farkle_chance[dice]) * points) + Stats.ev_dice[dice]
