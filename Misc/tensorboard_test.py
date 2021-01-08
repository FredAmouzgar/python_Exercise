import tensorflow as tf
import os, time
import numpy as np

root_logdir = os.path.join(os.curdir, "training_logs")


def get_run_logdir(path=root_logdir):
    run_id = "CartPole" + "-DQN-" + time.strftime("run_%Y_%m_%d-%H.%M.%S")
    return os.path.join(root_logdir, run_id)


test_logdir = get_run_logdir()
writer = tf.summary.create_file_writer(test_logdir)

with writer.as_default():
    for step in range(1, 1001):
        #time.sleep(0.5)
        #tf.summary.scalar("reward",np.log(step), step=step)
        tf.summary.scalar("reward", 5 * np.log(step), step=step)

#  Run $ tensorboard --logdir=training_logs
