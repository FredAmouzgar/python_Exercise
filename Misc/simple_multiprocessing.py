import multiprocessing as mp
from time import sleep
import random


def foo(id, queue):
    data = random.randint(1,1000)
    t = random.randint(1,5)
    #sleep(t)
    print(f"I'm {mp.current_process().name}, I waited for {t} sec. My data is {data}")
    queue.put(data)


if __name__ == "__main__":
    processes = []
    pn = 100
    queue = mp.Queue()
    for i in range(pn):
        p = mp.Process(target=foo, args=(i, queue), name="Worker-"+str(i))
        processes.append(p)
        p.daemon = True
        p.start()

    #_ = [p.join() for p in processes]

    print("Queue size:", queue.qsize())

    total = 0
    for _ in range(queue.qsize()):
        num = queue.get()
        total += num
        print(num)
    print("Sum is", total)
    queue.close()