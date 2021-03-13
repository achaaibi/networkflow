from app import run_app
from datetime import datetime, timedelta
import queue
import threading
import time

q = queue.Queue()
start_date = '03-10-2020 00:00:00'
end_date = '05-10-2020 00:00:00'
num_vlan = 130
interval_second = 120
PROCESSNUMBER = 10
start_date = datetime. strptime(start_date, '%d-%m-%Y %H:%M:%S')
end_date = datetime. strptime(end_date, '%d-%m-%Y %H:%M:%S')
interval_second = timedelta(seconds=interval_second)


def worker():
    while True:
        item = q.get()
        if item is None:
            break
        print("Working on " + item["start_date"]+" "+item["start_hour"] + " -> " + item["end_date"] + " " + item["end_hour"])
        run_app(item["start_date"], item["end_date"], item["start_hour"], item["end_hour"],num_vlan)
        q.task_done()


def start_workers(worker_pool=1000):
    threads = []
    for i in range(worker_pool):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)
    return threads


def stop_workers(threads):
    # stop workers
    for i in threads:
        q.put(None)
    for t in threads:
        t.join()


def main():
    workers = start_workers(worker_pool=PROCESSNUMBER)
    start_date_iter = start_date
    while end_date - start_date_iter > timedelta(seconds=0):
        end_date_iter = start_date_iter + interval_second
        #print("add_task"+ start_date_iter.strftime("%d-%m-%Y")+ " - " + end_date_iter.strftime("%d-%m-%Y") + " - " + start_date_iter.strftime("%H-%M-%S") + " - " + end_date_iter.strftime("%H-%M-%S"))
        item = {"start_date": start_date_iter.strftime("%Y-%m-%d"),
                "end_date": end_date_iter.strftime("%Y-%m-%d"),
                "start_hour": start_date_iter.strftime("%H:%M:%S"),
                "end_hour": end_date_iter.strftime("%H:%M:%S")}
        q.put(item)
        start_date_iter = end_date_iter
    q.join()
    stop_workers(workers)


if __name__ == "__main__":
    main()