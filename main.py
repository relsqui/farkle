import sys

from farkle.conditional_print import set_print_condition, tare_depth, if_print
from farkle.stats import Stats
from farkle.scoring import score_dice


def print_ev_tables(full_table=False, f=sys.stdout):
  print_progress = f is not sys.stdout or not full_table
  if_print(full_table, "EV of rolling D dice with P points", file=f)
  if_print(full_table, "P \\ D\t1\t2\t3\t4\t5\t6", file=f)
  threshold = [0] * 7
  for points in range(0, 10050, 50):
    if_print(print_progress, "Testing", points, "... ", end="", file=sys.stderr)
    if_print(full_table, points, end="", file=f)
    for dice in range(1, 7):
      if_print(print_progress, dice, end=" ", file=sys.stderr)
      Stats.recursion_counter = 0
      ev = Stats.ev_dice(dice, points)
      if_print(full_table, f"\t{str(ev)}", end="", file=f)
      if ev > 0:
        threshold[dice] = points
    if_print(full_table, file=f, flush=True)
    if_print(print_progress, file=sys.stderr)
  if_print(full_table, file=f)
  print("Highest score at which it's still worth rolling D dice:", file=f)
  for dice in range(1, 7):
    print(f"{dice}: {threshold[dice]}", file=f)
  print_cache_stats(f=f)

def print_cache_stats(f=sys.stdout):
  cache_size = sum(len(Stats.ev_cache[i]) for i in range(7))
  print(f"Cache size: {cache_size} items. {Stats.cache_hits} hits, {Stats.cache_misses} misses.", file=f)

def main():
  set_print_condition(False)
  tare_depth(2)
  # Stats.temp_recursion_limit = 1000000
  Stats.initialize()
  try:
    with open("evtable.txt", "w") as f:
     print_ev_tables(full_table=True, f=f)
  except RecursionError:
    print("hit recursion limit.")
    print_cache_stats()

if __name__ == "__main__":
  main()
