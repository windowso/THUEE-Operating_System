import random
import queue
import threading
import time

def quick_sort(arr, left, right):
    if left < right:
        pivot = partition(arr, left, right)
        quick_sort(arr, left, pivot - 1)
        quick_sort(arr, pivot + 1, right)

def partition(arr, left, right):
    pivot = arr[left]
    low = left
    high = right
    while low < high:
        while low < high and arr[high] >= pivot:
            high -= 1
        arr[low] = arr[high]
        while low < high and arr[low] < pivot:
            low += 1
        arr[high] = arr[low]
    arr[low] = pivot
    return low

def worker(segments, arr):
    while True:
        try:
            segment = segments.get(timeout=1)
        except queue.Empty:
            break
        left, right = segment
        if right - left + 1 >= 1000:
            pivot = partition(arr, left, right)
            segments.put((left, pivot - 1))
            segments.put((pivot + 1, right))
        else:
            quick_sort(arr, left, right)

def main():
    arr = [random.randint(0, 1000000) for _ in range(1000000)]
    arr_copy = arr.copy()
    start_time = time.time()
    quick_sort(arr_copy, 0, len(arr_copy) - 1)
    end_time = time.time()
    print("Single Thread sorting Time: " + str(end_time - start_time))
    with open("lab2/input.txt", "w") as f:
        for i in arr:
            f.write(str(i) + "\n")
    start_time = time.time()
    segments = queue.Queue()
    segments.put((0, len(arr) - 1))
    threads = []
    for _ in range(20):
        thread = threading.Thread(target=worker, args=(segments, arr))
        threads.append(thread)
        thread.start()
    created_time = time.time()
    print("Multi Thread creation Time: " + str(created_time - start_time))
    for thread in threads:
        thread.join()
    end_time = time.time()
    print("Multi Thread sorting Time: " + str(end_time - created_time - 1))
    print("Total Time: " + str(end_time - start_time - 1))
    sorted = all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))
    print("Sorted: " + str(sorted))
    with open("lab2/output.txt", "w") as f:
        for i in arr:
            f.write(str(i) + "\n")

if __name__ == '__main__':
    main()