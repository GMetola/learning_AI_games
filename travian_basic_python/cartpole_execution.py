from matplotlib import pyplot as plt
import gym
env = gym.make("CartPole-v1", render_mode="human")
observation, info = env.reset(seed=42)
hist_count = []
count = 0
for _ in range(10000):
    count += 1
    action = env.action_space.sample()
    observation, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        count = 0
        observation, info = env.reset()
    hist_count.append(count)
plt.plot(hist_count)
plt.show()
env.close()