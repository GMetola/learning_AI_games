from matplotlib import pyplot as plt
import gym

env = gym.make("MyEnv-v0")
observation, info = env.reset()
hist_TURN_NUMBER = []
hist_reward = []
TURN_NUMBER = 0

for _ in range(3000):
    TURN_NUMBER += 1
    hist_TURN_NUMBER.append(TURN_NUMBER)
    action = env.action_space.sample()
    observation, reward, terminated, info = env.step(action)
    if terminated:
        TURN_NUMBER = 0
        observation, info = env.reset()
        hist_reward.append(reward)

fig, ax = plt.subplots(2)
ax[0].plot(hist_TURN_NUMBER)
ax[1].plot(hist_reward)
plt.show()
env.close()
