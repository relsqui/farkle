from farkle.conditional_print import set_print_condition, tare_depth
from farkle.stats import Stats
from farkle.scoring import score_dice

def main():
  set_print_condition(False)
  tare_depth(2)
  print("EV of rolling D dice with P points")
  print("P \\ D\t1\t2\t3\t4\t5\t6")
  for points in range(0, 550, 50):
    print(points, end="")
    for dice in range(1, 7):
      try:
        ev = Stats.ev_dice(dice, points)
        print(f"\t{str(ev)}", end="")
      except RecursionError:
        print("Exceeded stack depth")
        break
    print()
  cache_size = sum(len(Stats.ev_cache[i]) for i in range(7))
  print(f"final cache size was {cache_size} items, we hit it {Stats.cache_hits} times")
  # print(Stats.ev_cache)

if __name__ == "__main__":
  main()
