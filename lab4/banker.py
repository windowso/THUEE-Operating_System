class Banker:
    def __init__(self, available, allocation, need):
        self.available = available
        self.allocation = allocation
        self.need = need
        self.n_processes = len(allocation)
        self.n_resources = len(allocation[0])

    def is_safe(self):
        work = self.available[:]
        finish = [False] * self.n_processes
        while True:
            found = False
            for i in range(self.n_processes):
                if not finish[i] and all(self.need[i][j] <= work[j] for j in range(self.n_resources)):
                    for j in range(self.n_resources):
                        work[j] += self.allocation[i][j]
                    finish[i] = True
                    found = True
                    print("In safe check: process {} is finished.".format(i))
            if not found:
                break
        return all(finish)

    def request(self, process_id, request_vector):
        if any(request_vector[i] > self.need[process_id][i] for i in range(self.n_resources)):
            return (False, "requesting more resources than needed.")
        if any(request_vector[i] > self.available[i] for i in range(self.n_resources)):
            return (False, "not enough resources.")
        for i in range(self.n_resources):
            self.available[i] -= request_vector[i]
            self.allocation[process_id][i] += request_vector[i]
            self.need[process_id][i] -= request_vector[i]
        safe = self.is_safe()
        if not safe:
            for i in range(self.n_resources):
                self.available[i] += request_vector[i]
                self.allocation[process_id][i] -= request_vector[i]
                self.need[process_id][i] += request_vector[i]
        return (safe, "banker is safe." if safe else "banker is unsafe.")
    
def test(request_data, banker):
    result = banker.request(*request_data)
    print("If process {} requests {}, {} So request is {}".format(request_data[0], request_data[1], result[1], "granted." if result[0] else "denied."))
    print("Available Vector: {}".format(banker.available))
    print("Allocation Matrix:\n{}".format("\n".join(str(row) for row in banker.allocation)))
    print("Need Matrix:\n{}".format("\n".join(str(row) for row in banker.need)), end = "\n\n")

if __name__ == "__main__":
    available = [3, 3, 2]
    allocation = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]
    need = [
        [7, 4, 3],
        [1, 2, 2],
        [6, 0, 0],
        [0, 1, 1],
        [4, 3, 1]
    ]
    banker = Banker(available, allocation, need)
    test((0, [0, 4, 0]), banker)
    test((3, (1, 1, 1)), banker)
    test((4, [0, 3, 0]), banker)
    test((1, [1, 0, 2]), banker)

    available = []
    allocation = [[]]
    need = [[]]
    banker1 = Banker(available, allocation, need)
    test((0, []), banker1)
