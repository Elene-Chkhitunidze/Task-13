import json
import threading
import queue
import time

#Task 1


files=['C:/Users/Elene/Desktop/sample1.json','C:/Users/Elene/Desktop/sample2.json', 'C:/Users/Elene/Desktop/sample3.json']

def data(file_name):
    try:
        with open(file_name, 'r') as file:
            result = json.load(file)
            print(f"Parsed data from {file_name}: {result}")

    except Exception as e:
        print(f"Error: {e}")

threads=list()

for i in files:
     thread=threading.Thread(target=data,args=(i,))
     threads.append(thread)
     thread.start()

for thread in threads:
    thread.join()


#Task 2

def process(que):
    name = threading.current_thread().name
    while True:
        try:
            value = que.get(timeout=1)
            if value is None:
                break
            even_odd = "odd" if value % 2 != 0 else "even"
            print(f"Thread {name}: {value} is {even_odd}")
            que.task_done()
        except queue.Empty:
            break

q = queue.Queue()

for i in range(1, 11):
    q.put(i)

threads = []
for i in range(3):
    thread = threading.Thread(target=process, args=(q,), name=f"N-{i+1}")
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print("ყველა ამოცანა შესრულებულია!")

