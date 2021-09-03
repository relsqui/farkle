import itertools
import sys

from .scoring import score_dice, dice_to_counts
from .conditional_print import set_print_condition, if_print

temp = 0

class Stats(object):
  farkle_chance = {0:1, 1:.67, 2:.44, 3:.28, 4:.16, 5:.8, 6:.2}
  ev_cache = [{}, {}, {}, {}, {}, {}, {}]

  @classmethod
  def ev_dice(cls, dice_count, turn_score):
    global temp
    if dice_count == 0:
      return 0
    if not cls.ev_cache[dice_count].get(turn_score):
      part_score_sum = 0
      combo_count = 0
      for combo in itertools.product([1, 2, 3, 4, 5, 6], repeat=dice_count):
        temp += 1
        if temp > 10:
          sys.exit(0)
        print(f"calculating ev for rolling {dice_count} dice with {turn_score} points")
        part_score, extra_dice = score_dice(dice_to_counts(combo), turn_score, cls)
        if part_score == 0:
          part_score_sum -= turn_score
        else:
          ev_continue = cls.ev_dice(extra_dice, turn_score + part_score)
          if ev_continue > turn_score + part_score:
            part_score += ev_continue
          part_score_sum += part_score
        combo_count += 1
      cls.ev_cache[dice_count][turn_score] = part_score_sum / combo_count
    return cls.ev_cache[dice_count][turn_score]

  @classmethod
  def should_i_bank(cls, dice_count, turn_score):
    return turn_score > cls.ev_dice(dice_count, turn_score)
