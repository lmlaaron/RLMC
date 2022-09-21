# simulatot for a simple multi-bank memory controller
# the input are two traces 
# the out put returns the E2E latecny of each packet of each trace

from queue import Queue
import random

class Request:
    def __init__(self, request_id = -1, bank = -1, start_time = 0):
        self.request_id = request_id
        self.bank = bank
        self.start_time = start_time
        self.issue_time = -1
        self.e2e = -1

    def __str__(self):
        return str(self.request_id) + ' ' + str(self.bank) + ' ' + str(self.start_time) + ' ' + str(self.issue_time) + ' ' + str(self.e2e)

    def issue(self,time):
        self.issue_time = time
        self.e2e = time - self.start_time
        #print(self.__str__())

class MCScheduler:
    
    def __init__(self, banks, bank_time, num_banks, time=0):
        self.time = time
        self.banks = banks
        self.bank_time = bank_time
        self.num_banks = num_banks
        self.bank_queue=[]
        for i in range(0, self.num_banks):
            self.bank_queue.append(Queue()) 

    def add(self, request):
        #print('add ' + str(request.bank))
        self.bank_queue[request.bank].put(request)

    def sched(self,time):
        # find a feasible one and scedhule
        self.time = time
        
        for i in range(0, self.num_banks):
            if self.bank_queue[i].empty() != True and self.banks[i] + self.bank_time < time:
                
                return self.bank_queue[i].get()

        return Request()

class MemSimulator:
    
    def __init__(self):
        self.attacker_trace = []
        self.victim_trace = []
        self.bank_time = 4
        self.step_time = 1
        self.num_banks = 4

        self.banks = []
        for i in range(0, self.num_banks):
            self.banks.append(-self.bank_time) # record the time last activated
        
        for i in range(0, 100):
            self.attacker_trace.append(Request('a_'+str(i), random.randint(-1, self.num_banks - 1),i ))
            self.victim_trace.append(Request('v_'+str(i), random.randint(-1, self.num_banks - 1), i))

        for i in self.attacker_trace:
            print(i)

        for i in self.victim_trace:
            print(i)

        self.time = 0

        self.scheduler = MCScheduler(self.banks, self.bank_time, self.num_banks)
        self.sim_time = 500


    def step(self):
        if self.time < len(self.attacker_trace) and self.attacker_trace[self.time].bank != -1: # a real access
            self.scheduler.add(self.attacker_trace[self.time])

        if self.time < len(self.victim_trace) and self.victim_trace[self.time].bank != -1: # a real access
            self.scheduler.add(self.victim_trace[self.time])
   
        cand_request = self.scheduler.sched(self.time)
        
        if cand_request.bank != -1:
        
            if self.banks[cand_request.bank] + self.bank_time < self.time: 
                #print('found candidate ' + str(cand_request))
                self.banks[cand_request.bank] = self.time
                #print(self.time)
                cand_request.issue(self.time)
                print('step ' + str(self.time) + " issued " +str(cand_request))
            else:   # violation
                print(cand_request)
                print("exception")
                exit(-1)

        self.time += 1

    def run(self):
        while self.time < self.sim_time:
            self.step()

        for i in self.attacker_trace:
            print(i)

        for i in self.victim_trace:
            print(i)


if __name__ == "__main__":
    mem_sim = MemSimulator()
    mem_sim.run()

