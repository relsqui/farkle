from farkle.conditional_print import set_print_condition, tare_depth
from farkle.stats import Stats
from farkle.scoring import score_dice

def main():
  set_print_condition(False)
  tare_depth(2)
  print("EV of rolling D dice with P points")
  print("vP D>\t1\t2\t3\t4\t5\t6")
  for points in range(0, 250, 50):
    row = [str(points)] + [""] * 6
    for dice in range(1, 7):
      try:
        ev = Stats.ev_dice(dice, points)
        row[dice] = str(ev)
        # print(f"(recursed {Stats.recursion_counter} times)")
      except RecursionError:
        print("Exceeded stack depth")
        break
    print("\t".join(row))
  cache_size = sum(len(Stats.ev_cache[i]) for i in range(7))
  print(f"final cache size was {cache_size} items")
  # print(Stats.ev_cache)

if __name__ == "__main__":
  main()
