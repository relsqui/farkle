from farkle.stats import Stats
from farkle.scoring import score_dice

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
  Stats.print_table()

if __name__ == "__main__":
  main()
