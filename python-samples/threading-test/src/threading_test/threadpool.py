from concurrent.futures import ThreadPoolExecutor
from threading import current_thread
from time import sleep


def run():
    print("threadpool")
    num = 5
    futures = []
    with ThreadPoolExecutor(max_workers=3, thread_name_prefix="test_executor") as executor:
        for i in range(num):
            future = executor.submit(slow_work, num=num-i)
            futures.append(future)
        print("全員作業開始")
        for future in futures:
            print(f"{future.result()=}")
        print("全員作業終了")


def slow_work(num: int = 3):
    t = current_thread()
    name = t.getName()
    print(f"作業開始 {num=} {name=}")
    sleep(num)
    print(f"作業終了 {num=} {name=}")
    return num
