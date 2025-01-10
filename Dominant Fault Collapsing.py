#Dominant Fault Collapsing

def read_netlist(file_path):
    with open(file_path) as f:
        netlist = f.readlines()
    return netlist

def process_netlist(netlist):
    m = [line.split() for line in netlist]
    return m

def get_fanout_list(m):
    return [line for line in m if line[0] == 'FANOUT']

def get_output_nodes(m):
    output_nodes = []
    for line in m:
        if line[0] == 'OUTPUT':
            output_nodes.extend(int(node) for node in line[1:])
    return output_nodes

def categorize_lines(m):
    out_in_fanout_list = []
    gates_list = []
    input_list = []
    for line in m:
        if line[0] in ['FANOUT', 'OUTPUT', 'INPUT']:
            out_in_fanout_list.append(line)
        else:
            gates_list.append(line)
        if line[0] == 'INPUT':
            input_list.extend(int(node) for node in line[1:])
    return gates_list, out_in_fanout_list, input_list

def get_output_wires(gates_list):
    return sorted((int(gate[1]) for gate in gates_list), reverse=True)

def get_unique_wires(m):
    wires = [int(node) for line in m for node in line[1:]]
    return list(set(wires))

def initialize_fault_list(wires_list):
    Fault = [f"sa0_{i+1}" for i in range(len(wires_list))] + [f"sa1_{i+1}" for i in range(len(wires_list))]
    Values_sa = ['Present'] * len(Fault)
    return dict(zip(Fault, Values_sa))

def dominance_fault_collapsing_rules(gate, out1, in1, rem_in):
    fault_to_remove = []
    if gate in ['AND', 'NAND']:
        fault_to_remove.extend([f'sa0_{out1}', f'sa1_{out1}', f'sa0_{in1}'])
    elif gate in ['OR', 'NOR']:
        fault_to_remove.extend([f'sa0_{out1}', f'sa1_{out1}', f'sa1_{in1}'])
    if len(rem_in)!=0:
        for i in rem_in:
            if gate in ['AND', 'NAND']:
                fault_to_remove.extend([f'sa0_{i}'])
            elif gate in ['OR', 'NOR']:
                fault_to_remove.extend([f'sa1_{i}'])
    return fault_to_remove

def find_gate(gates_list, gate_wire):
    for gate in gates_list:
        if int(gate[1]) == gate_wire:
            return gate[0]
    return None

def is_output_of_gate(output_wires, num):
    return int(num) in output_wires

def find_gate_list(gates_list, gate_wire):
    for gate in gates_list:
        if int(gate[1]) == gate_wire:
            return gate
    return None

def find_gate_input(gate):
    return [int(node) for node in gate[2:]]

def is_fanout(fanout_list, num):
    for fanout in fanout_list:
        if int(fanout[1]) == num:
            return True
    return False

def find_fanout(fanout_list, node):
    for fanout in fanout_list:
        if int(fanout[1]) == node:
            return [int(fanout[i]) for i in range(2, len(fanout))]
    return []

def return_in_if_fanout(is_fanout, num1, num2):
    return num1 if is_fanout(num1) else num2

def apply_fault_collapsing(gates_list, output_wires, fanout_list, fault_dict):
    for out in output_wires:
        gate_str = find_gate(gates_list, out)
        gate_in = find_gate_input(find_gate_list(gates_list, out))
        in1 = gate_in[0]
        in2 = gate_in[1]
        rem_in=gate_in[2:]
        in_pref = return_in_if_fanout(lambda num: is_fanout(fanout_list, num), in1, in2)
        fault_to_remove_list = dominance_fault_collapsing_rules(gate_str, out, in_pref, rem_in)
        for fault in fault_to_remove_list:
            fault_dict[fault] = 'Collapsed'
    return fault_dict

def get_collapsed_faults(fault_dict):
    return [key for key, value in fault_dict.items() if value != 'Collapsed']

# Main execution
netlist = read_netlist(input("Enter Netlist File name: ")+'.txt')
m = process_netlist(netlist)
fanout_list = get_fanout_list(m)
output_nodes = get_output_nodes(m)
gates_list, out_in_fanout_list, input_list = categorize_lines(m)
output_wires = get_output_wires(gates_list)
wires_list = get_unique_wires(m)
fault_dict = initialize_fault_list(wires_list)
fault_dict = apply_fault_collapsing(gates_list, output_wires, fanout_list, fault_dict)
collapsed_fault_key_list = get_collapsed_faults(fault_dict)
collapse_ratio=len(collapsed_fault_key_list)/len(fault_dict.keys())

print("Initial Fault List:", list(fault_dict.keys()))
print("Dominant Collapsed Fault List:", collapsed_fault_key_list)
print("Collapse Ratio:", collapse_ratio)
