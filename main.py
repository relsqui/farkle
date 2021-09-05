import sys

from farkle.conditional_print import set_print_condition, tare_depth, if_print
from farkle.stats import Stats
from farkle.scoring import score_dice


def print_ev_tables(full_table=False, f=sys.stdout):
  set_print_condition(False)
  tare_depth(2)
  if_print(full_table, "EV of rolling D dice with P points", file=f)
  if_print(full_table, "P \\ D\t1\t2\t3\t4\t5\t6", file=f)
  threshold = [0] * 7
  for points in range(0, 10050, 50):
    if_print(f is not sys.stdout or not full_table, "Testing", points, "...", file=sys.stderr)
    if_print(full_table, points, end="", file=f)
    for dice in range(1, 7):
      ev = Stats.ev_dice(dice, points)
      if_print(full_table, f"\t{str(ev)}", end="", file=f)
      if ev > 0:
        threshold[dice] = points
    if_print(full_table, file=f)
  if_print(full_table, file=f)
  print("Highest score at which it's still worth rolling D dice:", file=f)
  for dice in range(1, 7):
    print(f"{dice}: {threshold[dice]}", file=f)
  print(file=f)
  cache_size = sum(len(Stats.ev_cache[i]) for i in range(7))
  print(f"final cache size was {cache_size} items, we hit it {Stats.cache_hits} times", file=f)

if __name__ == "__main__":
  print_ev_tables()
