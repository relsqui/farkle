from .stats import Stats

class ScoreType(object):
  points = 0
  dice_used = 0

  def _apply(self, dice_counts):
    raise NotImplementedError

  def apply(self, dice_counts, score):
    total_dice = sum(dice_counts)
    ev_skip = Stats.ev_dice[total_dice]
    ev_apply = self.points + Stats.ev_dice[total_dice - self.dice_used]
    if score == 0 or ev_apply > ev_skip:
      self._apply(dice_counts)

class SixOfAKind(object):
  points = 3000
  dice_used = 6
  def _apply(self, dice_counts):
    if 6 in dice_counts:
      dice_counts[dice_counts.index(6)] = 0
      return True
