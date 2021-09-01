import itertools

from .conditional_print import set_print_condition, if_print

class Stats(object):
  # base cases, we'll fill in the rest below
  # dict keys are the number of dice rolled
  farkle_chance = {0: 1, 1: 2/3}
  ev_dice = {0: 0, 1: 25}
  threshold = {}

  @classmethod
  def initialize(cls, *args, verbose=False, **kwargs):
    # the ev of 0 should actually be the ev of 6, because of hot dice,
    # but we don't know what that is yet. so start with ev[0] = 0,
    # then update it repeatedly until it stops changing
    while round(cls.ev_dice[0]) != round(cls.ev_dice.get(6, -1)):
      cls.ev_dice[0] = cls.ev_dice.get(6, 0)
      if_print(verbose, f"Recalculating with ev[0]={cls.ev_dice[0]}")
      cls.calculate_ev(*args, **kwargs)
    if_print(verbose, "Stabilized.")
    if_print(verbose)
    for n in range(1, 7):
      cls.threshold[n] = round(Stats.ev_dice[n] / Stats.farkle_chance[n])

  @classmethod
  def calculate_ev(cls, score_dice, watch=()):
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
          if not cls.should_i_bank(score, extra_dice):
            score += cls.ev_dice[extra_dice]
        total_ev += score
      cls.farkle_chance[n] = zeroes / combo_count
      cls.ev_dice[n] = total_ev / combo_count

  @classmethod
  def should_i_bank(cls, points, dice):
    return points > ((1 - Stats.farkle_chance[dice]) * points) + Stats.ev_dice[dice]

  @classmethod
  def print_table(cls):
    print("Dice\tBank@\tEV\tFarkle%")
    for i in range(1, 7):
      print(f"{i}\t{cls.threshold[i]}\t{round(cls.ev_dice[i])}\t{round(cls.farkle_chance[i]*100)}")
