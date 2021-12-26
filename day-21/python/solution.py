
def roll_dice(dice: int):
    new_dice = dice + 1 
    return 1 if new_dice == 101 else new_dice

def apply_roll(last_pos: int, dice_sum: int):
    last_pos -= 1
    last_pos += dice_sum

    last_pos %= 10

    return last_pos + 1

def step(last_pos: int, dice: int):
    d1 = roll_dice(dice)
    d2 = roll_dice(d1)
    d3 = roll_dice(d2)

    new_pos = apply_roll(last_pos, d1 + d2 + d3)

    return new_pos, d3


dice, dice_count = 0, 0
p1_pos, p2_pos = 10, 2
p1_score, p2_score = 0, 0


while True:
    p1_pos, dice = step(p1_pos, dice)
    dice_count += 3
    p1_score += p1_pos

    if p1_score >= 1000:
        winner_score, loser_score = p1_score, p2_score
        break 

    p2_pos, dice = step(p2_pos, dice)
    dice_count += 3
    p2_score += p2_pos
    
    if p2_score >= 1000:
        winner_score, loser_score = p2_score, p1_score
        break
    
print(p1_score, p2_score, dice_count)

print(loser_score * dice_count)