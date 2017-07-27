from multiprocessing import Process, Lock, Pipe
import random
import time

runTime = 5

def cell_status(lock, T, child):
    count = 0 
    while(count < 5):
        child.send([random.randint(0,100),time.time()])
        lock.release()
        count = count + 1
        time.sleep(0.1)

def check_status(lock_A,lock_B, p_a, p_b):
    count = 0
    while(count < 5):
        # lock this process first
        lock_A.acquire()
        lock_B.acquire()

        # This process will be unlocked after two child processes sent their data
        A = p_a.recv()
        B = p_b.recv()

        print("A is {} and timestamp is {}\n B is {} and timestamp is {}".format(A[0],A[1],B[0],B[1]))
        count = count+1



def runner():
    startTime = time.time()
    T = 0

    # process A
    lock_A = Lock()
    parent_conn_A, child_conn_A = Pipe()
    cell_A = Process(target=cell_status, args=(lock_A, T, child_conn_A))
    
    # process B
    lock_B = Lock()
    parent_conn_B, child_conn_B = Pipe()
    cell_B = Process(target=cell_status, args=(lock_B, T, child_conn_B))

    # Monitor process
    monitor = Process(target=check_status, args=(lock_A, lock_B, parent_conn_A, parent_conn_B))

    # start
    monitor.start()
    time.sleep(1)
    cell_A.start()
    cell_B.start()

    print("finished!")
    # End
    monitor.join()
    cell_A.join()
    cell_B.join()


runner()

