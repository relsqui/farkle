import itertools
import sys
import time

from .scoring import score_dice, dice_to_counts
from .conditional_print import con_print, if_print


def round50(i):
  return round(i/50) * 50

class Stats(object):
  ev_cache = [{}, {}, {}, {}, {}, {}, {}]
  cache_hits = 0
  cache_misses = 0
  recursion_counter = 0
  temp_recursion_limit = 0

  @classmethod
  def initialize(cls, verbose=False):
    if len(cls.ev_cache[0]) < 7 or len(cls.ev_cache[1]) < 7:
      if_print(verbose, "Initializing base cases.", file=sys.stderr)
      cls.initialize_bases()
    if_print(verbose, "Starting cache build, this will take a while.", file=sys.stderr)
    for dice in range(1, 7):
      for points in range(0, 10050, 50):
        if_print(verbose, f"Evaluating {dice} dice at {points} points ...", end="", file=sys.stderr)
        # discard the result, we're caching them in the method
        cls.ev_dice(dice, points)
        if_print(verbose, f"done. ({time.asctime()})", timestamp=False, file=sys.stderr)
    if_print(verbose, "Initialized!", file=sys.stderr)

  @classmethod
  def initialize_bases(cls):
    updated = 0
    for points in range(0, 10050, 50):
      ev_zero = cls.ev_cache[6].get(points, 0)
      if cls.ev_cache[0].get(points) is None or cls.ev_cache[0][points] != ev_zero:
        updated += 1
      cls.ev_cache[0][points] = ev_zero
      cls.ev_cache[1][points] = round(ev_zero/3) + round((-points) * 2/3)
    return updated

  @classmethod
  def dump_file(cls, filename):
    with open(filename, "w") as f:
      print("#Points\t1\t2\t3\t4\t5\t6 dice", file=f)
      for points in range(0, 10050, 50):
        row = [str(points)]
        for dice in range(1, 7):
          row.append(str(cls.ev_cache[dice][points]))
        print("\t".join(row), file=f)

  @classmethod
  def load_file(cls, filename, verbose=False):
    with open(filename) as f:
      if_print(verbose, f"Loading stats from {filename}.", file=sys.stderr)
      for line in f:
        line = line.strip()
        if line == "" or line[0] == "#":
          continue
        evs = list(map(int, line.split()))
        points = evs.pop(0)
        if_print(verbose, points, evs, file=sys.stderr)
        for i in range(1, 7):
          cls.ev_cache[i][points] = evs[i-1]
        cls.ev_cache[0][points] = cls.ev_cache[6][points]

  @classmethod
  def ev_dice(cls, dice_count, score):
    # real scores are always multiples of 50
    # keep the precise one for doing math with, but
    # use a rounded version for cache keys
    rscore = round50(score)
    cls.recursion_counter += 1
    if cls.temp_recursion_limit > 0 and cls.recursion_counter > cls.temp_recursion_limit:
      raise RecursionError
    if score > 10000:
      # don't roll more dice when you can bank and win
      con_print("max score reached")
      return 0
    if dice_count == 0:
      con_print("hot dice!")
    if cls.ev_cache[dice_count].get(rscore) is None:
      cls.cache_misses += 1
      turn_score_sum = 0
      combo_count = 0
      con_print(f"calculating ev for rolling {dice_count} dice with {score} points")
      for combo in itertools.product([1, 2, 3, 4, 5, 6], repeat=dice_count):
        con_print(f"checking combo {list(combo)}")
        turn_score, extra_dice = score_dice(combo, score, cls)
        if turn_score == 0:
          con_print("farkle")
          turn_score = -score
        else:
          con_print(f"checking ev of leftover {extra_dice} dice")
          ev_continue = cls.ev_dice(extra_dice, score + turn_score)
          if ev_continue > 0:
            con_print(f"worth rolling, adding {ev_continue} to turn score")
            turn_score += ev_continue
          else:
            con_print("not worth rolling")
        turn_score_sum += turn_score
        combo_count += 1
      cls.ev_cache[dice_count][rscore] = round(turn_score_sum / combo_count)
    else:
      cls.cache_hits += 1
      con_print(f"using cached value for {dice_count} dice and {score} points")
    return cls.ev_cache[dice_count][rscore]

  @classmethod
  def should_i_bank(cls, dice_count, score):
    con_print(f"considering banking {score} points with {dice_count} dice")
    return cls.ev_dice(dice_count, score) > 0
