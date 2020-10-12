# How setup Colab for inline rendering of OpenAI Gym's environments

Add [this code](https://raw.githubusercontent.com/FredAmouzgar/python_Exercise/master/Colab_setup/sample_colab_cell.py) to the first cell of your Jupyter notebook. :point_down:


```python
import sys, os
if 'google.colab' in sys.modules and not os.path.exists('.done'):
    !wget -q https://raw.githubusercontent.com/FredAmouzgar/python_Exercise/master/Colab_setup/setup_colab.sh -O- | bash
    !touch .done

# Creating a virtual display to draw game images on.
if type(os.environ.get("DISPLAY")) is not str or len(os.environ.get("DISPLAY")) == 0:
    !bash ../xvfb start
    os.environ['DISPLAY'] = ':1'
```

Here's a sample code:

```python
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
```