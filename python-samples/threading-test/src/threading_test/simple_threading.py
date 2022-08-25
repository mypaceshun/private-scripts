from threading import Thread, current_thread
from time import sleep


def run():
    print("simple threading")
    num: int = 5
    threads: Thread = [
        Thread(name=f"work{i}", target=slow_work, kwargs={"num": num - i})
        for i in range(num)
    ]
    for t in threads:
        t.start()
    print("全員作業開始")
    for t in threads:
        t.join()
    print("全員作業終了")
    slow_work(num=0)


def slow_work(num: int = 3):
    t = current_thread()
    name = t.getName()
    print(f"作業開始 {num=} {name=}")
    sleep(num)
    print(f"作業終了 {num=} {name=}")
