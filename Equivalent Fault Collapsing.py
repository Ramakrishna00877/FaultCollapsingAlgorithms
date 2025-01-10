#Finding equivalent fault collapsing list and collapsing ratio

class equivalent_fault:
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
    
    def equivalent_fault_collapsing(self):
        read_netlist=self.read_netlist()
        final_fault_list=self.total_fault_list()
        for i in read_netlist:
            if (i[0]=="NAND") or (i[0]=="AND"):
                for j in i[2:]:
                    final_fault_list.remove("sa0_"+j)
            elif (i[0]=="NOR") or (i[0]=="OR"):
                for j in i[2:]:
                    final_fault_list.remove("sa1_"+j)
            elif i[0]==("NOT"):
                for j in i[2:]:
                    final_fault_list.remove("sa0_"+j)
                    final_fault_list.remove("sa1_"+j)
                    
        return final_fault_list

        
obj=equivalent_fault("Netlist3")
print("Total Fault list: ",obj.total_fault_list())
print("Equivalent Fault Collapsed list: ",obj.equivalent_fault_collapsing())
print("Equivalent Fault Collapsing ratio: ",(len(obj.equivalent_fault_collapsing())/len(obj.total_fault_list())))

