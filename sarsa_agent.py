from mc_agent import *

def generate_episode_sarsa(lambda_, Q2, N, N_s,policy):
  start_state = (get_card(True), get_card(True))
  action = policy[start_state[0]][start_state[1]]
  E = [[[0.0 for _ in range(num_actions)] for _ in range(num_states)] for _ in range(num_states)]
  next_state, reward, is_terminal = step(start_state, action)
  while is_terminal == 0:
    next_action = policy[next_state[0]][next_state[1]]
    td_error = reward + lambda_*Q2[next_state[0]][next_state[1]][next_action] - Q2[start_state[0]][start_state[1]][action]
    E[start_state[0]][start_state[1]][action] += 1
    N_s[start_state[0]][start_state[1]] += 1
    for i in range(1,22):
      for j in range(1,22):
        for k in range(0,2):
          N[i][j][k] += 1
          alpha = 1.0/N[i][j][k]
          Q2[i][j][k] = Q2[i][j][k] + alpha*td_error*E[i][j][k]
          E[i][j][k] = lambda_*E[i][j][k]
    start_state = next_state
    action = next_action
    next_state, reward, is_terminal = step(start_state, action)

    # epsilon-greedy policy improvement
    for i in range(1,22):
      for j in range(1,22):
        prob = random.random()
        epsilon = N0/(N0 + 1.0*N_s[i][j])
        if prob <= epsilon:
          action = random.randint(0,1)
        else:
          if Q2[i][j][0] > Q2[i][j][1]:
            action = 0
          else:
            action = 1 
        policy[i][j] = action
  mse = 0.0
  for i in range(1,22):
    for j in range(1,22):
      for k in range(0,2):
        mse = mse + np.square(Q[i][j][k] - Q2[i][j][k])
  return mse

def run_sarsa_control():
  lambdas_ = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5,0.6,0.7,0.8,0.9,1]
  mses = []
  for lambda_ in lambdas_:
    Q2 = [[[random.random() for _ in range(num_actions)] for _ in range(num_states)] for _ in range(num_states)]
    N = [[[0.0 for _ in range(num_actions)] for _ in range(num_states)] for _ in range(num_states)]
    N_s = [[0.0 for _ in range(num_states)] for _ in range(num_states)]
    policy = [[0 for _ in range(num_states)] for _ in range(num_states)]
    ms = []
    episodes = []
    for i in range(1000):
      ms.append(generate_episode_sarsa(lambda_,Q2,N,N_s,policy))
      episodes.append(i+1)
    if lambda_ == 0.0 or lambda_ == 1:
      plt.plot(episodes, ms)
      plt.title('Episode Number vs MSE for lambda = %f' % lambda_)
      plt.xlabel('Episode Number')
      plt.ylabel('MSE')
      plt.show()
    mse = 0.0
    for i in range(1,22):
      for j in range(1,22):
        for k in range(0,2):
          mse = mse + np.square(Q[i][j][k] - Q2[i][j][k])
    mses.append(mse)

  plt.plot(lambdas_, mses)
  plt.title('Lambda vs MSE')
  plt.xlabel('lambda')
  plt.ylabel('MSE')
  plt.show()

run_mc_control()
run_sarsa_control()