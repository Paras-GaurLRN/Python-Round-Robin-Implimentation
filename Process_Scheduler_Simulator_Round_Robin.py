class Process:
    ...

from typing import NewType
Process = NewType('Process',Process)

IPET : Exception = Exception("Illegal Process ExecTime")
NPA : Exception = Exception("Non-Parentic Addition")

class Process:
    def __init__(Pro : Process , TimeSlice : float , / , Name : str , Parent : Process = None) -> Process:
        if TimeSlice < 0 :
            raise IPET
        Pro.Name : str = Name
        Pro.TimeSlice : float = TimeSlice
        Pro.Parent : Process = Parent
    
    def __str__(Pro : Process) -> str :
        return (f"\nProcess : {Pro.Name}\nExecution Time : {Pro.TimeSlice}\nParent : {Pro.Parent}\n")
    
    def __add__(Pro1 : Process , Pro2 : Process) -> Process :
        '''
        The Inheritence is all from the First Process
        So it is not commutative as names might differ after addition 
        '''
        if ((Pro1.Parent is None) and (Pro2.Parent is None)) or (Pro1.Parent == Pro2.Parent) :
            return Process(Pro1.TimeSlice + Pro2.TimeSlice , Name = Pro1.Name , Parent = Pro1.Parent)
        else:
            raise NPA
    
    def __sub__(Pro1 : Process , Pro2 : Process) -> Process :
        if Pro1.TimeSlice >= Pro2.TimeSlice:
            Pro2.TimeSlice = (-1)*(Pro2.TimeSlice)
            return Pro1.__add__(Pro2)
        else:
            raise IPET

    def __copy__(Pro : Process) -> Process:
        Pro_T : Process = Process(Pro.TimeSlice,Name=Pro.Name,Parent=Pro.Parent)
        return Pro_T

def RoundRobin_Inplace(Quanta : float , Processes : list[Process]) -> dict[int,tuple[str,float]] :
    '''    
    dict : {... , i : (Pro_i , Execution-Duration) , ...}
    '''
    # Initilization
    Schedule_Order : dict[int,tuple[str,float]] = {}
    ind : int = 0
    noprocesses : int = len(Processes)
    ExecTime : float = 0
    
    # Scheduling
    while noprocesses != 0 : # Remove a process after it's execution is complete
    
        Pro_T : Process = Processes[ind % noprocesses]
    
        if Pro_T.TimeSlice < Quanta:
            ExecTime = Pro_T.TimeSlice
            Processes.pop(ind % noprocesses)
            noprocesses -= 1
        
        else:
            ExecTime = Quanta
            Processes[ind % noprocesses].TimeSlice -= Quanta
        if ExecTime != 0:
            Schedule_Order[ind] = (Pro_T.Name,ExecTime)
        ind+=1
    
    return Schedule_Order

def ConveyLister(ProcessesINP : list[Process]) -> list[Process]:
    Processes = [(Pro_T.TimeSlice, Pro_T) for Pro_T in ProcessesINP]
    
    Processes.sort(key=lambda x: x[0])
    
    return [Pro[1] for Pro in Processes]
    
def RoundRobin(Quanta : float , ProcessesINP : list[Process]) -> dict[int,tuple[str,float]] :
    '''
    dict : {... , i : (Pro_i , Execution-Duration) , ...}
    '''

    # Initilization
    Processes : list[Process] = [Pro_T_OG.__copy__() for Pro_T_OG in ProcessesINP]
    Schedule_Order : dict[int,tuple[str,float]] = {}
    ind : int = 0
    noprocesses : int = len(Processes)
    ExecTime : float = 0
    RemovalList : list[Process] = []

    # Scheduling
    while len(Processes) != 0:
        try:
            for Pro_T in Processes:
                if Pro_T.TimeSlice < Quanta:
                    ExecTime = Pro_T.TimeSlice
                    RemovalList += [Pro_T]
                else:
                    ExecTime = Quanta
                    Processes[Processes.index(Pro_T)].TimeSlice -= Quanta
                if ExecTime != 0:
                    Schedule_Order[ind] = (Pro_T.Name,ExecTime)
                ind+=1
    
        finally:
            Processes = [Pro for Pro in Processes if Pro not in RemovalList]
    
    return Schedule_Order


'''
EXAMPLE SHOWCASE
'''
Pro1 = Process(12,Name='Pro1')
Pro2 = Process(3,Name='Pro2')
Pro3 = Process(5,Name='Pro3')
Pro4 = Process(23,Name='Pro4')
prolst2 = [Pro1,Pro2,Pro3,Pro4]

print("\n NOT IN-PLACE \n")
print("\nBEFORE\n")

for Pro_T in prolst2:
    print(str(Pro_T))

print("\nGantt Chart\n")
print(RoundRobin(4,prolst2),'\n')

print("\nGantt Chart WIth Convey Effect Taken Into Account\n")
print(RoundRobin(4,ConveyLister(prolst2)))

print("\nAFTER\n")

for Pro_T in prolst2:
    print(str(Pro_T))

print("\n IN-PLACE \n")
print("\nBEFORE\n")

for Pro_T in prolst2:
    print(str(Pro_T))

print("\nGantt Chart\n")
print(RoundRobin_Inplace(4,prolst2),'\n')

print("\nAFTER\n")

for Pro_T in prolst2:
    print(str(Pro_T))

print("As You Can See, prolst2 is now gone")