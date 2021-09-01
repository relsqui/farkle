from farkle.stats import Stats
from farkle.scoring import score_dice

def print_thresholds():
  print("Banking score thresholds:")
  print("(if you have x dice to reroll, bank at y points)")
  for n in range(1, 7):
    print(f"{n}:", round(Stats.ev_dice[n] / Stats.farkle_chance[n]))

def print_evs():
  print("Expected point values of rolling x dice:")
  for n in range(1, 7):
    print(f"{n}:", round(Stats.ev_dice[n]))

def interactive():
  while True:
    print("Enter points pending and number of dice available to reroll:")
    try:
      points, dice = map(int, input().split())
      print("Farkle chance:", round(Stats.farkle_chance[dice], 2))
      print("EV of rolling:", round(Stats.ev_dice[dice], 2))
      if Stats.should_i_bank(points, dice):
        print("You should bank.")
      else:
        print("You should roll.")
    except ValueError:
      print("Sorry, didn't catch that. Try two space-separated numbers, or Ctrl-C to exit.")
    except (EOFError, KeyboardInterrupt):
      break

def main():
  Stats.initialize(score_dice)
  print_thresholds()
  print()
  print_evs()

if __name__ == "__main__":
  main()
