import itertools
import sys

from .scoring import score_dice, dice_to_counts
from .conditional_print import con_print

class Stats(object):
  farkle_chance = {0:1, 1:.67, 2:.44, 3:.28, 4:.16, 5:.8, 6:.2}
  ev_cache = [{}, {}, {}, {}, {}, {}, {}]
  recursion_counter = 0
  temp_recursion_limit = 0

  @classmethod
  def ev_dice(cls, dice_count, score):
    cls.recursion_counter += 1
    if cls.temp_recursion_limit > 0 and cls.recursion_counter > cls.temp_recursion_limit:
      raise RecursionError
    if dice_count == 0:
      con_print("no more dice")
      return 0
    if dice_count == 1:
      con_print("last die")
      # 25 is (100 * 1/6) + (50 * 1/6), the only ways to score with one die
      return 25 + round(-score * 2/3)
    if not cls.ev_cache[dice_count].get(score):
      turn_score_sum = 0
      combo_count = 0
      con_print(f"calculating ev for rolling {dice_count} dice with {score} points")
      for combo in itertools.product([1, 2, 3, 4, 5, 6], repeat=dice_count):
        con_print(f"checking combo {list(combo)}")
        turn_score, extra_dice = score_dice(dice_to_counts(combo), score, cls)
        if turn_score == 0:
          con_print("farkle")
          turn_score = -score
        elif extra_dice > 0:
          con_print(f"checking ev of leftover {extra_dice} dice")
          ev_continue = cls.ev_dice(extra_dice, score + turn_score)
          if ev_continue > turn_score:
            turn_score += ev_continue
        turn_score_sum += turn_score
        combo_count += 1
      cls.ev_cache[dice_count][score] = round(turn_score_sum / combo_count)
    else:
      con_print(f"using cached value for {dice_count} dice and {score} points")
    return cls.ev_cache[dice_count][score]

  @classmethod
  def should_i_bank(cls, dice_count, score):
    con_print(f"considering banking {score} points with {dice_count} dice")
    return score > cls.ev_dice(dice_count, score)
