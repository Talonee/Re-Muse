import threading
import time

# With threading
class reMuse(threading.Thread):
    def __init__(self, threadId, name, count):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        self.count = count

    def run(self):
        # print("Starting: " + self.name + "\n")
        print_time(self.name, 1, self.count)
        # print("Exiting: " + self.name + "\n")


# Without threading
class reMuse2():
    def __init__(self, threadId, name, count):
        self.threadId = threadId
        self.name = name
        self.count = count

    def run(self):
        # print("Starting: " + self.name)
        print_time(self.name, 1, self.count)
        # print("Exiting: " + self.name + "\n")



def print_time(name, delay, count):
    while count:
        time.sleep(delay)
        # print(f"{name} {time.ctime(time.time())} {count}")
        count -= 1



thread1 = reMuse(1, "Search album, artist, title", 25)
thread2 = reMuse(2, "Retrieve cover", 6)
thread3 = reMuse(3, "Get lyrics", 9)

ctime = time.time()
thread1.start()
thread2.start()
thread3.start()
thread1.join()
thread2.join()
thread3.join()
print(f"With threading: {time.time() - ctime:.2f}.")
# print("Done main thread.")





ctime = time.time()
thread1 = reMuse2(1, "Search album, artist, title", 25)
thread2 = reMuse2(2, "Retrieve cover", 6)
thread3 = reMuse2(3, "Get lyrics", 9)

thread1.run()
thread2.run()
thread3.run()
print(f"Without threading: {time.time() - ctime:.2f}.")
