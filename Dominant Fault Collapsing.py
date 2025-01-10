#Finding dominant fault collapsing list and collapsing ratio

class dominant_fault:
    def __init__(self,filename):
        self.filename = filename+'.txt'
        print(filename)

    def read_netlist(self):
        m=[]
        with open(self.filename) as f:
            netlist = f.readlines()
        for i in netlist:
            m.append(i.split())
        return m
    def total_fault_list(self):
        read_netlist=self.read_netlist()
        total_fault_list=[]
        node_points=[]
        for i in read_netlist:
            node_points.append(i[1:])
        node_points=set(int(item) for sublist in node_points for item in sublist)
        node_points=list(node_points)
        node_points.sort()
        for i in node_points:
            total_fault_list.append("sa0_"+str(i))
            total_fault_list.append("sa1_"+str(i))
        return total_fault_list

    def fanout_and_pi_list(self):
        read_netlist=self.read_netlist()
        fanout_list=[]
        fan_out_indep=[]
        pi_list=[]
        pi_indep_list=[]
        gate_in_list=[]
        gate_out_list=[]
        final_fault_list=self.total_fault_list()
        for i in read_netlist:
            if i[0]=="INPUT":
                pi_list.append(i[1:])
            elif i[0]=="FANOUT":
                fanout_list.append(i[1:])
            elif i[0] in ("NAND", "NOT", "AND", "OR", "NOR"):
                gate_out_list.append(int(i[1]))
                gate_in_list.append(i[2:])
        fanout_list=set(int(item) for sublist in fanout_list for item in sublist)
        fanout_list=list(fanout_list)
        print(gate_in_list)
        
        pi_list=set(int(item) for sublist in pi_list for item in sublist)
        pi_list=list(pi_list)
        gate_in_list=set(int(item1) for sublist1 in gate_in_list for item1 in sublist1)
        gate_in_list=list(gate_in_list)
        print(pi_list,fanout_list,gate_out_list,gate_in_list)
        for i in fanout_list:
            if (i not in gate_out_list) and (i not in gate_in_list):
                fan_out_indep.append(i)
            if i in gate_out_list:
                fanout_list.remove(i)

        fanout_list=[item for item in fanout_list if item not in fan_out_indep]
        
        for i in pi_list:
            if (i not in gate_in_list):
                pi_indep_list.append(i)
                pi_list.remove(i)
        
        pi_indep_list=set(pi_indep_list+fan_out_indep)
        
        #This contains primary inputs and fanouts which is not connected to gates
        #fanout_list contains only fanouts independent of fanouts which is connected gates
        pi_indep_list=list(pi_indep_list)
        pi_list=set(pi_list+fanout_list)
        pi_list=list(pi_list)
        print(pi_indep_list,pi_list,gate_in_list,gate_out_list)
        return pi_indep_list,pi_list,gate_in_list,gate_out_list
    
    def dominant_fault_collapsing(self):
        read_netlist=self.read_netlist()
        final_fault_list=[]
        pi_indep_list,pi_list,gate_in_list,gate_out_list=self.fanout_and_pi_list()
        for i in pi_indep_list:
            final_fault_list.append("sa0_"+str(i))
            final_fault_list.append("sa1_"+str(i))
        for i in read_netlist:
            for j in i[2:]:
                if int(j) in pi_list:
                    if (i[0]=="NAND") or (i[0]=="AND"):
                        for k in i[2:]:
                            
                            if k==i[2] and int(k) not in gate_out_list:
                                final_fault_list.append("sa1_"+k)
                                final_fault_list.append("sa0_"+k)
                            elif k!=i[2] and int(k) not in gate_out_list:
                                final_fault_list.append("sa1_"+k)
                    elif (i[0]=="NOR") or (i[0]=="OR"):
                        for k in i[2:]:
                            
                            if k==i[2] and int(k) not in gate_out_list:
                                final_fault_list.append("sa1_"+k)
                                final_fault_list.append("sa0_"+k)
                            elif k!=i[2] and int(k) not in gate_out_list:
                                final_fault_list.append("sa0_"+k)
                    elif (i[0]=="NOT"):
                        for k in i[2:]:
                        
                            if k==i[2] and int(k) not in gate_out_list:
                                final_fault_list.append("sa1_"+k)
                                final_fault_list.append("sa0_"+k)
                    break
            
        return final_fault_list

        
obj=dominant_fault(input("Enter file name: "))
print("Total Fault list: ",obj.total_fault_list())
print("Dominant Fault Collapsed list: ",obj.dominant_fault_collapsing())
print("Dominant Fault Collapsing ratio: ",(len(obj.dominant_fault_collapsing())/len(obj.total_fault_list())))

