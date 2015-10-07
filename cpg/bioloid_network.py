import cpg.matsuoka_joint
import random

class BioloidNetwork:
    def __init__(self, weightList, timestep):
        # we assume that the first 8*8 values in the weight list are weights for the network
        # and the rest are parameters for the cpg
        if len(weightList) != (8*8+10):
            print("Weight list was not of expected length!")
        self.weights = get_weights_from_list(weightList[0:(8*8)], 8, 8)
        self.neighbours = [[1,2,5],[0,2,4],[0,1,3,6,7],[2,4,5,6,7],[1,3,5],[0,3,4],[2,3,7],[2,3,6]]
        self.nodes = self.create_joints()
        self.last_outputs = [1,1,1,1,1,1,1,1]
        self.timestep = timestep

    def create_joints(self):
        joint_list = []
        for i_node in range(len(self.neighbours)):
            beta = 2.5
            u0 = 1.0
            v1 = 0#1.0
            v2 = 0.0
            w21 = -2.0
            w12 = -2.0
            tu = 0.025
            tv = 0.3
            u1 = 0.0
            u2 = 0#1.0
            # Increase speed for knees
            #if i_node in [1,2,3,4]:
                #tu = tu/2
                #tv = tv/2
                                                        # beta, u0,  v1,  v2,  w21,  w12,  tu, tv, u1,  u2
            joint_list.append(cpg.matsuoka_joint.MatsuokaJoint(beta, u0,  v1,  v2,  w21,  w12,  tu, tv, u1,  u2))
            #joint_list.append(cpg.matsuoka_joint.MatsuokaJoint(4*(-1+2*random.random()), 4*(-1+2*random.random()), 4*(-1+2*random.random()), 4*(-1+2*random.random()), 4*(-1+2*random.random()), 4*(-1+2*random.random()), tu, tv, 4*(-1+2*random.random()), 4*(-1+2*random.random())))
        return joint_list

    def get_output(self):
        new_outputs = []
        for i_node in range(len(self.nodes)):
            current_node = self.nodes[i_node]
            current_neighbours = self.neighbours[i_node]
            input1 = 0
            input2 = 0
            for i_neighbour in current_neighbours:
                input1 += self.last_outputs[i_neighbour]*self.weights[i_node][i_neighbour] 
                #input1 += max(self.last_outputs[i_neighbour],0)*self.weights[i_node][i_neighbour] 
                #input2 += min(self.last_outputs[i_neighbour],0)*self.weights[i_node][i_neighbour] 
            new_outputs.append(self.nodes[i_node].get_output(input1,input2,self.timestep))
        #print(new_outputs)
        self.last_outputs = new_outputs
        #print(self.last_outputs)
        return new_outputs

def get_random_weights(a,b):
    weights = []
    for i in range(a):
        innerWeights = []
        for j in range(b):
            innerWeights.append(-1+2*random.random())
        weights.append(innerWeights)
    return weights

def get_weights_from_list(l,w,h):
    weights = []
    index = 0
    for i in range(h):
        row = []
        for j in range(w):
            row.append(l[index])
            index += 1
        weights.append(row)
    return weights

