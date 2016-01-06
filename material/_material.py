

class Material(object):
    def __init__(self, epsilon_r, mu_r):
        self.epsilon = 8.8541878176e-12*epsilon_r
        self.mu = 1.2566370614359172e-6*mu_r
        self.speed_of_light = 1.0 / (self.epsilon*self.mu)**0.5 / 1.0e6
        self.eta = (self.mu/self.epsilon)**0.5
