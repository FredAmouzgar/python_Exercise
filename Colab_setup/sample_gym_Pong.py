## Add this after loading the virtual screen and see its rendering
## Not a perfect solution, though. Better than nothing!
import gym
import matplotlib.pyplot as plt
from time import sleep
from IPython.display import clear_output

env = gym.make("Pong-v0")
env.reset()
done = False
step = 0
while not done:
  new_state,reward,done, _ = env.step(env.action_space.sample())
  step += 1
  if step % 2 == 0:
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.imshow(env.render(mode="rgb_array"))
    plt.show()
    sleep(0.01)
    clear_output(wait=True)
