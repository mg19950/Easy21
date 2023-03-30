import matplotlib.cm as cm
import matplotlib.pyplot as plt
import random
import numpy as np

num_states = 22
num_actions = 2

def get_card(force_black = False):
  num = random.randint(1,10)
  prob = random.randint(1,3)
  if prob == 3 and force_black == False:
    return -1*num
  else:
    return num

def step(s, a):
  player_sum, dealer_sum = s
  if a == 1:
    while dealer_sum < 17:
      dealer_sum += get_card(False)
      if dealer_sum < 1:
        return (player_sum, dealer_sum), 1, 1
    if dealer_sum > 21 or player_sum > dealer_sum:
      return (player_sum, dealer_sum), 1, 1
    elif dealer_sum > player_sum:
      return (player_sum, dealer_sum), -1, 1
    else: 
      return (player_sum, dealer_sum), 0, 1
  elif a == 0:
    player_sum += get_card(False)
    if player_sum > 21 or player_sum < 1:
      return (player_sum, dealer_sum), -1, 1
    return (player_sum, dealer_sum), 0, 0
    