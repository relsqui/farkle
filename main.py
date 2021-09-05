import sys
import time

from farkle.stats import Stats
from farkle.scoring import score_dice


def print_cache_stats(file=sys.stdout):
  cache_size = sum(len(Stats.ev_cache[i]) for i in range(7))
  cache_rate = round(Stats.cache_hits * 100 / (Stats.cache_hits + Stats.cache_misses), 2)
  print(f"Cache size: {cache_size} items. {cache_rate}% hit rate.\n"
        f"({Stats.cache_hits} hits, {Stats.cache_misses} misses.)", file=file)

def calculate_zero_ev(start_file=None, generation=0, log_handle=sys.stderr):
  if start_file:
    try:
      Stats.load_file(start_file)
      print(f"Loaded stats from {start_file}.", file=log_handle)
    except FileNotFoundError:
      print(f"Couldn't find file {start_file}.", file=log_handle)
  updated_zeroes = Stats.initialize_bases()
  while updated_zeroes > 0:
    print(f"Generation {generation} ({updated_zeroes} zeroes updated):", file=log_handle)
    filename = f"ev_zero_{generation}.txt"
    # empty the cache to recalculate from new base values
    for dice in range(2, 7):
      Stats.ev_cache[dice] = {}
    print(f"Initializing (started {time.asctime()}) ...")
    Stats.initialize(verbose=False)
    Stats.dump_file(filename)
    print(f"Dumped to {filename}.")
    print_cache_stats()
    generation += 1
    updated_zeroes = Stats.initialize_bases()
  print(f"Stabilized in {generation} generations!", file=log_handle)

def print_thresholds():
  threshold = {}
  for dice in range(1, 7):
    for points in range(0, 10050, 50):
      threshold[dice] = points
      if Stats.ev_cache[dice][points] <= 0:
        break
  print("Lowest score you should bank with, by number of dice available to roll:")
  print(threshold)

def main():
  Stats.load_file("latest.stats")
  print_thresholds()

if __name__ == "__main__":
  main()
