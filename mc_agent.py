from easy21_environment import *

Q = [[[0.0 for _ in range(num_actions)] for _ in range(num_states)] for _ in range(num_states)]
N = [[[0.0 for _ in range(num_actions)] for _ in range(num_states)] for _ in range(num_states)]
N_s = [[0.0 for _ in range(num_states)] for _ in range(num_states)]
V = [[0.0 for _ in range(num_states)] for _ in range(num_states)]
N0 = 100.0
policy = [[0 for _ in range(num_states)] for _ in range(num_states)]

def generate_episode():
  states = []
  episode_return = 0
  start_state = (get_card(True), get_card(True))
  action = policy[start_state[0]][start_state[1]]
  states.append((start_state, action))
  next_state, episode_return, is_terminal = step(start_state, action)
  while is_terminal == 0:
    action = policy[next_state[0]][next_state[1]]
    states.append((next_state, action))
    next_state, episode_return, is_terminal = step(next_state, action)
  

  for state in states:
    N[state[0][0]][state[0][1]][state[1]] += 1
    N_s[state[0][0]][state[0][1]] += 1
    alpha = 1.0/N[state[0][0]][state[0][1]][state[1]]
    Q[state[0][0]][state[0][1]][state[1]] = Q[state[0][0]][state[0][1]][state[1]] + alpha*(episode_return - Q[state[0][0]][state[0][1]][state[1]])


  for i in range(1,22):
    for j in range(1,22):
      prob = random.random()
      epsilon = N0/(N0 + 1.0*N_s[i][j])
      if prob <= epsilon:
        action = random.randint(0,1)
      else:
        if Q[i][j][0] > Q[i][j][1]:
          action = 0
        else:
          action = 1 
      policy[i][j] = action

def run_mc_control():
  for i in range(50000):
    generate_episode()
  
  for i in range(0,22):
    for j in range(0,22):
      V[i][j] = Q[i][j][0] if Q[i][j][0] > Q[i][j][1] else Q[i][j][1]


  fig = plt.figure()
  ax = fig.add_subplot(111,projection ='3d')
  X = [i for i in range(0,22)]
  Y = [i for i in range(0,22)]

  surf = ax.plot_surface(X,Y,np.array(V),cmap=cm.bwr,antialiased=False)
  plt.title('value function after %d episodes' % 50000)
  ax.set_xlabel('Dealer showing')
  ax.set_ylabel('Player sum')
  ax.set_zlabel('V(s)')
  plt.show()
  

run_mc_control()