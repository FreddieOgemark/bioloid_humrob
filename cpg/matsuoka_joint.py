import math

class MatsuokaJoint:
    def __init__(self, beta, u0, v1, v2, w21, w12, tu, tv, u1, u2):
        self.beta = beta
        self.u0 = u0
        self.v1 = v1
        self.v2 = v2
        self.w21 = w21
        self.w12 = w12
        self.tu = tu
        self.tv = tv
        self.u1 = u1
        self.u2 = u2
        self.y1 = 0
        self.y2 = 0

    def get_output(self, input1, input2, timestep):
        du1 = 1/self.tu*(-self.u1-self.beta*self.v1+self.w12*self.y2+self.u0+input1)
        du2 = 1/self.tu*(-self.u2-self.beta*self.v2+self.w21*self.y1+self.u0+input2)
        self.u1 = self.u1 + timestep*du1
        self.u2 = self.u2 + timestep*du2
        dv1 = 1/self.tv*(-self.v1+self.y1)
        dv2 = 1/self.tv*(-self.v2+self.y2)
        self.v1 = self.v1 + timestep*dv1
        self.v2 = self.v2 + timestep*dv2
        self.y1 = max(self.u1,0)
        self.y2 = max(self.u2,0)
        y = self.y2 - self.y1
        return y