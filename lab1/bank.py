import threading
import queue
import time

class Customer:
    def __init__(self, id, arrival_time, service_time):
        self.id = id
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.start_service_time = 0
        self.leave_time = 0
        self.served_by = None
        self.sem = threading.Semaphore(0)

def customer_action(customer, waiting_customers, waiting_customers_mtx, waiting_customers_sem):
    time.sleep(customer.arrival_time)
    waiting_customers_mtx.acquire()
    waiting_customers.put(customer)
    waiting_customers_mtx.release()
    waiting_customers_sem.release()
    customer.sem.acquire()

def teller_action(teller_id, init_time, waiting_customers, waiting_customers_mtx, waiting_customers_sem):
    while True:
        waiting_customers_sem.acquire()
        waiting_customers_mtx.acquire()
        customer = waiting_customers.get()
        waiting_customers_mtx.release()
        customer.start_service_time = round(time.time() - init_time)
        customer.served_by = teller_id
        time.sleep(customer.service_time)
        customer.leave_time = customer.start_service_time + customer.service_time
        customer.sem.release()
        print("顾客{}进入银行时间为{}，开始服务时间为{}，离开银行时间为{}，服务柜员号为{}".format(customer.id, customer.arrival_time, customer.start_service_time, customer.leave_time, customer.served_by))

def read_data():
    customers = []
    with open("lab1/test.txt", "r") as f:
        for line in f:
            fields = line.strip().split()
            customer_id = int(fields[0])
            arrival_time = int(fields[1])
            service_time = int(fields[2])
            customer = Customer(customer_id, arrival_time, service_time)
            customers.append(customer)
    customers.sort(key=lambda x: x.arrival_time)
    return customers

def main():
    customers = read_data()
    num_tellers = 3
    init_time = time.time()
    waiting_customers = queue.Queue()
    waiting_customers_mtx = threading.Lock()
    waiting_customers_sem = threading.Semaphore(0)

    for customer in customers:
        t = threading.Thread(target=customer_action, args=(customer, waiting_customers, waiting_customers_mtx, waiting_customers_sem))
        t.start()

    for i in range(num_tellers):
        t = threading.Thread(target=teller_action, args=(i+1, init_time, waiting_customers, waiting_customers_mtx, waiting_customers_sem))
        t.start()

if __name__ == "__main__":
    main()