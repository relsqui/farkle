from farkle.stats import stats, should_i_bank

def print_thresholds():
  print("Banking score thresholds:")
  print("(if you have x dice to reroll, bank at y points)")
  for n in range(1, 7):
    print(f"{n}:", round(stats.ev_dice[n] / stats.farkle_chance[n]))

def interactive():
  while True:
    print("Enter points pending and dice quantity to reroll:")
    try:
      points, dice = map(int, input().split())
      print("Farkle chance:", round(stats.farkle_chance[dice], 2))
      print("EV of rolling:", round(stats.ev_dice[dice], 2))
      if should_i_bank(points, dice):
        print("You should bank.")
      else:
        print("You should roll.")
    except ValueError:
      print("Sorry, didn't catch that.")
    except (EOFError, KeyboardInterrupt):
      break
    print()

def main():
  print_thresholds()

if __name__ == "__main__":
  main()
