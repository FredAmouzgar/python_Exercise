import multiprocessing
from time import sleep, time
import random
import gym
import tensorflow as tf
from tensorflow import keras
import tensorflow_probability as tfp
from queue import Queue


class Learner(multiprocessing.Process):
    def __init__(self, queue):
        super().__init__()
        self.processed_trajectories = 0
        self.queue = queue

    def run(self):
        SLEEP_DURATION = 3
        tolerance = 15
        while True:
            if self.queue.qsize() < 1:
                if tolerance <= 0:
                    print("*** LEARNER: Hit the ZERO TOLERANCE. Exiting ...")
                    break
                tolerance -= 1
                print("* LEARNER: The Queue was empty, waiting for {} sec ...".format(SLEEP_DURATION))
                sleep(SLEEP_DURATION)
                print("* LEARNER: Wait ended")
                continue

            experience = self.queue.get()
            tolerance = 15
            self.processed_trajectories += 1
            print("\rQueue Size from inside Learner:", self.queue.qsize(), end="")
        print("***** Process Learner Ended. Prcessed Trajectories:", self.processed_trajectories)

class Worker(multiprocessing.Process):
    def __init__(self, n, queue, env_name):
        super().__init__()
        self.queue = queue

        self.env = gym.make(env_name).env
        self.w_no = n
        self.state_size = self.env.observation_space.shape[0]
        self.action_size = self.env.action_space.n
        self.model = keras.Sequential([keras.layers.Dense(50, activation="relu", input_shape=(self.state_size,)),
                                       keras.layers.Dense(self.action_size, activation=keras.activations.sigmoid)])
        self.model.load_weights("brain_CartPole-v1.h5")


    def run(self):
        trajectory = []
        s = self.env.reset()
        reward: int = 0
        done = False
        while not done:
            self.env.render()
            s = tf.convert_to_tensor(s.reshape(1, self.state_size), dtype=tf.float32)
            logits = self.model(s)
            action_probs = tfp.distributions.Categorical(probs=logits)
            action = action_probs.sample()
            s_, r, done, _ = self.env.step(action.numpy()[0])
            trajectory.append((self.w_no, s_, r, s, done))
            # self.queue.put((self.w_no, s_, r, s, done))
            reward += r
            s = s_
        for e in trajectory:
            self.queue.put(e, block=True)

        self.env.close()
        print("Process",self.w_no,"Executed. Reward", reward)


def single(episodes=50, env_name="CartPole-v1"):
    env = gym.make(env_name).env
    model = keras.Sequential([keras.layers.Dense(50, activation="relu", input_shape=(env.observation_space.shape[0],)),
                              keras.layers.Dense(env.action_space.n, activation=keras.activations.sigmoid)])
    model.load_weights("brain_CartPole-v1.h5")
    for e in range(episodes):
        print("Episode", e, "---------")
        s = env.reset()
        reward: int = 0
        done = False
        while not done:
            env.render()
            s = tf.convert_to_tensor(s.reshape(1, env.observation_space.shape[0]), dtype=tf.float32)
            logits = model(s)
            action_probs = tfp.distributions.Categorical(probs=logits)
            action = action_probs.sample()
            s_, r, done, _ = env.step(action.numpy()[0])
            reward += r
            s = s_
        print("Reward", reward)
        return


def multi(w_no=5, episodes=250):
    queue = multiprocessing.Queue()
    learner = Learner(queue)
    learner.start()
    for e in range(episodes):
        print("Episode", e, "---------")
        workers = [Worker(i, queue, env_name="CartPole-v1") for i in range(w_no)]
        for worker in workers:
            worker.start()
        for worker in workers:
            worker.join()
    queue.close()
    print("Q closed.")
    learner.join()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    stime = time()
    multi(w_no=20, episodes=3)          # Multi  = 60.331
    # single(episodes=2)        # Single = 71.277
    print(time() - stime)
