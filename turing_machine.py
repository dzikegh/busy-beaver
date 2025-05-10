import signal
from collections import deque
from typing import Optional, Tuple

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
import numpy as np

class TuringMachine:
    def __init__(self, machine_code: str, m: int, all_tape: int = 0):
        self.machine_code = machine_code 
        self.m = m # number of symbols
        self.all_tape = all_tape # starting tape symbol
        
        self.n = len(self.machine_code.split("_")) # number of states

        # Check correct format state letter
        letters_states: list = sorted([letter for state in machine_code.split("_") for letter in state[2::3]])
        last_letter: str = letters_states[-1] if letters_states[-1] != 'Z' else letters_states[-2]
        
        assert ord(last_letter) - ord('A') + 1 <= self.n ,"""Please name state in alphabetical order, st. the index of the 'last' letter (in the alphabet) is the letter at the index n (with n the number of state of the TM)
            ex. 5-TM must only contain jump instructions from : ['A', 'B', 'C', 'D', 'E', 'Z', '-']"""
        
        # create the Turing Machine 
        self.tm = np.zeros((self.n, self.m, 3), dtype = int)
        for i,state_transitions in enumerate(self.machine_code.split("_")):
            transitions = [list(state_transitions[i:i+3]) for i in range(0, len(state_transitions), 3)]
            for trans_idx, transition in enumerate(transitions):
                # undefined state
                if transition == ['-','-','-']: 
                    transitions[trans_idx] = [0,0,0]
                    continue

                # write instruction
                if transition[0] not in [str(i) for i in range(0,self.m)]:
                    raise ValueError(f"Incorrect Machine Code format: Transition got wrong write instruction in state {i}")
                transitions[trans_idx][0] = int(transition[0])
                
                # moving instruction
                if transition[1] not in ['R','L']:
                    raise ValueError(f"Incorrect Machine Code format: Transition got wrong moving instruction in state {i}")
                transitions[trans_idx][1] = 0 if transition[1]=='R' else 1

                # jump instruction
                if  ord(transition[2]) - ord('A') < 0 or ord(transition[2]) - ord('A') > ord('Z') - ord('A'): # jump instruction is not a state (because not a capital letter)
                    raise ValueError(f"Incorrect Machine Code format: Transition got wrong jump instruction in state {i}, Not a capital letter")
                if transition[2] == 'Z': # halt
                    transitions[trans_idx][2] = 0
                else:
                    transitions[trans_idx][2] = ord(transition[2]) - ord('A') + 1
            
            self.tm[i] = transitions       
        
    def __repr__(self):
        string = f"TM code: {self.machine_code}\nComputer readable TM:\n"
        for state in self.tm.tolist():
            string += f"{state}\n"
        return string

    @staticmethod
    def handler_time_limit(signum, frame):
        raise Exception("Time limit Reached. Machine status: HOLDOUT")
    
    #@staticmethod
    def plot_time_space_diagram(self, steps_tape_state: list):
        steps_tape_state.reverse() # upside down 
        last_tape_length = len(steps_tape_state[0][0])

        time_space_diagram = np.zeros((len(steps_tape_state),last_tape_length))
        time_space_diagram[0] = steps_tape_state[0][0]

        delta: int = 0
        for step in range(1,len(steps_tape_state)):
            tape, head_position, visited_cells = steps_tape_state[step]
            _, previous_head_position, previous_visited_cells = steps_tape_state[step-1]
            if (
                (head_position == 0 and visited_cells < previous_visited_cells) or 
                (head_position < previous_head_position and visited_cells < previous_visited_cells)
                ):
                delta += 1 

            time_space_diagram[step,delta:] = tape

        time_space_diagram = np.flip(time_space_diagram, axis=0)
        time_space_diagram = np.pad(time_space_diagram, ((1,0),(10,10)), constant_values=(0, 0))
        plt.figure()    
        plt.title(f"Space-time Diagram for machine: {self.machine_code}")
        plt.imshow(time_space_diagram,cmap='grey')
        plt.axis('off')
        plt.show()


    # for a time limit: https://stackoverflow.com/questions/492519/timeout-on-a-function-call#494273
    def run(self, space_limit: int = None, time_limit: int = None, space_time_diagram: bool = False, **kargs) -> Optional[Tuple[str, Optional[Tuple[int, int]]]]:
        """
        Run the Turing Machine:
        args:
            - space_limit (int): number of maximal at least visited once cells
            - time_limit (int): Timer, amount of time before we stop the machine 
            - space_time_diagram (bool): show the Space-time diagram
        kargs:
            - max_iter (int): number of iteration to plot in the space time diagram (default = 1000)
        returns:
            - status (str): 'HALT' or 'HOLDOUT' machine status.
            - if the TM halts, (score (int), steps (int)): score of the TM (number of cells visited) and number of steps taken
        
        TODO: Save tape state/machine state to continue computation during next phase 
        """
        max_iter = kargs.get('max_iter', 10)

        if space_time_diagram: 
            steps_tape_state: list = []

        print(f"Running machine: {self.machine_code}")
        signal.signal(signal.SIGALRM, TuringMachine.handler_time_limit)
        signal.alarm(time_limit) #set Timer Alarm OS level (UNIX only)
        try:
            # Initial parameter
            tape = deque([self.all_tape], maxlen=space_limit)
            visited_cells: int  = 0 # length of the tape i.e the cells that have been visited by the TM
            steps: int  = 0

            head_position: int  = 0
            current_state: int  = 1 # always start in A state
            
            while visited_cells <= space_limit:
                if current_state == 0:
                    score: int = sum(list(tape))
                    print(f"The Machine as Halted: steps {steps}, score {score}")
                    return("HALT", score, steps)
                
                # read cell
                symbol_read = tape[head_position]
                transition = self.tm[current_state - 1][symbol_read]
                # write symbol
                tape[head_position] = transition[0]
                # move 
                if transition[1] == 0: # right
                    head_position += 1
                    if head_position > visited_cells:
                        tape.append(self.all_tape) 
                        visited_cells += 1
                else: # left
                    if head_position == 0:
                        tape.appendleft(self.all_tape) # head_position stays at 0
                        visited_cells += 1
                    else:
                        head_position -= 1
                steps += 1   
                current_state = transition[2] # jump to next state

                if space_time_diagram:
                    steps_tape_state.append((np.array(tape), head_position, visited_cells))
                    if steps == max_iter or current_state == 0:
                        print(f"steps={steps}, current_state={current_state}")
                        self.plot_time_space_diagram(steps_tape_state)

            signal.alarm(0)
            print("Space limit Reached. Machine status: HOLDOUT")
            return("HOLDOUT")

        except Exception as exc:
            print(exc)
            signal.alarm(0)
            return("HOLDOUT")
           

if __name__ == "__main__":
    # Example usage
    machine_code = "1RB---_1LB0RB" # 2-states, 2-symbols TM | Translated Cycler
    #machine_code = "1RB0RB_1LA1RZ" # 2-states, 2-symbols TM | Halting 
    #machine_code = "1RB0RB_0LA---" # 2-states, 2-symbols TM | Cycler
    
    all_tape = 0
    m = 2
    tm = TuringMachine(machine_code, m, all_tape)
    #print(tm)
    tm.run(space_limit=50, time_limit=500, space_time_diagram=True, max_iter = 20)