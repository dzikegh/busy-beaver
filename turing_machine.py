import numpy as np

class TuringMachine:
    def __init__(self, machine_code: str, m: int, all_tape: int = 0):
        self.machine_code = machine_code 
        self.m = m # number of symbols
        self.all_tape = all_tape # starting tape symbol
        
        self.n = len(self.machine_code.split("_")) # number of states

        # Check correct format state letter
        letters_states = sorted([letter for state in machine_code.split("_") for letter in state[2::3]])
        last_letter = letters_states[-1] if letters_states[-1] != 'Z' else letters_states[-2]
        
        assert ord(last_letter) - ord('A') + 1 <= self.n ,"""Please name state in alphabetical order, st. the index of the 'last' letter (in the alphabet) is the letter at the index n (with n the number of state of the TM)
            ex. 5-TM must only contain jump instructions from : ['A', 'B', 'C', 'D', 'E', 'Z', '-']"""
        
        # create the Turing Machine 
        self.tm = np.zeros((self.n, self.m, 3), dtype = int)
        for i,state_transition in enumerate(self.machine_code.split("_")):
            transitions = [list(state_transition[i:i+3]) for i in range(0, len(state_transition), 3)]
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
        
        
    def run(self):
        pass

if __name__ == "__main__":
    # Example usage
    #machine_code = "1RB1RZ_0LC0RA_1RA1LB" # 3-states, 2-symbols TM
    machine_code = "1RB1RZ_0LC0RA_1RA---" # 3-states, 2-symbols TM
    #machine_code = "1RB---_1LB1LB" # 2-states, 2-symbols TM
    all_tape = 0
    m = 2
    tm = TuringMachine(machine_code, m, all_tape)
    print(tm)
        